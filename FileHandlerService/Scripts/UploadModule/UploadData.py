import json
import os
import logging

import AbstractModule as am
import CsvLoader


class UploadModule(am.AbstractModule):
    def __init__(self, host, db_name, user, pwd, port, case_id, variant_id):
        am.AbstractModule.__init__(self, host, db_name, user, pwd, port)
        self.set_schema_id(case_id, variant_id)
        self._gml_table = ''
        self._json_dict = {}

    def upload_data(self, file, extension):
        if extension.upper() == ".JSON" or extension.upper() == ".GEOJSON":
            self._json_dict = json.loads(file)
        elif extension.upper() == ".CSV":
             self._json_dict = CsvLoader.loadAsJson(file)

        if not self._json_dict:
            self._status += "Can't convert data into right json format"
        else:
            if self._check_case_variant():
                self._parse_features()

        logging.debug(self._status)
        return self._status

    def _check_case_variant(self):
        if not self._pdm.check_if_schema_exists(self._schemaID):
            self._status += "Failed - schema for case and variant doesn't exist"
            return False
        return True

    def print_json(self):
        print self._json_dict
        logging.info(self._json_dict)

    def _create_feature_if_necessary(self, feature_id, key_id):
        req = self._create_schema_request("""INSERT INTO {} ({}) VALUES ('{}'); """.format(self._gml_table, key_id, feature_id))
        logging.debug(req)
        self._pdm.execute_request(req)
        self._pdm.commit_transactions()

    def _create_insert_feature_request(self, properties, feature_id, key_id):
        self._create_feature_if_necessary(feature_id, key_id)
        if not self._update_feature(feature_id, properties, key_id):
            return False
        return True

    def _update_feature(self, gml_id, properties, key_id):
        req = "UPDATE {} SET ".format(self._gml_table)
        firstPass = True
        for property_key, property_value in properties.iteritems():
            # todo check conversion properly
            if property_key != 'objectID' and property_value is not '':
                if not firstPass:
                    req += ", "
                else:
                    firstPass = False

                req += "{}='{}'".format(property_key, property_value.replace(',','.'))

        if not firstPass:
            req += " WHERE {}='{}';".format(key_id, gml_id)
            embedded_req = self._create_schema_request(req)

            logging.debug(embedded_req)
            if not self._pdm.execute_request(embedded_req):
                self._status = "Failed - can't update element"
                return False

        return True

    def _check_srs(self):
        return True
#         srs = self._json_dict.get('crs', None)
#         if srs is None or srs not in self.valid_srs_list:
#             self.status = "Failed - wrong srs. Only wgs84 is supported right now"
#             return False
#         else:
#             return True

    """ Parse properties and convert it as an insert request"""
    def _parse_features(self):
        ftype = self._json_dict.get('type', None)
        if ftype != 'FeatureCollection':
            self._status = "Failed - not feature collection in geoJSON"
            return False

        gml_type = self._json_dict.get('gml_type', None)
        if not gml_type:
            self._status = "Failed - not gml type defined in geoJSON"
            return False

        self._gml_table = self._valid_gml_type.get(gml_type.upper(), None)
        if not self._gml_table:
            self._status = "Failed - gml type is not a valid one"
            return False

        features_list = self._json_dict.get('features', [])
        for feature in features_list:
            properties = feature.get('properties', None)
            if properties is None:
                self._status += "Failed - At least one feature has no properties (at least objectID is mandatory)"
                return False

            key_id = self._gml_table.lower() + '_id'
            feature_id = properties.get('objectID', None)
            if not feature_id:
                self._status = "Failed - no objectID"
                return False

            if not self._create_insert_feature_request(properties, feature_id, key_id):
                self._status = "Failed - can't update feature"
                self._pdm.rollback_transactions()
                return False

            geometry = feature.get('geometry', None)
            if geometry is not None:
                if not self._update_feature_geometry( json.dumps(geometry), feature_id, key_id):
                    self._status = "Failed - can't upload geometry"
                    self._pdm.rollback_transactions()
                    return False

            self._pdm.commit_transactions()

        self._status = "Success"
        return True

    def _update_feature_geometry(self, geometry, feature_id, key_id):
        based_req = """UPDATE {}.{} SET lod0footprint=( ST_AsText(ST_GeomFromGeoJSON('{}') ) ) WHERE {}='{}';"""\
            .format(self._schemaID, self._gml_table, geometry, key_id, feature_id)

        geom_req = """ SET SCHEMA 'public';  {}""".format(based_req)

        logging.debug(geom_req)
        if not self._pdm.execute_request(geom_req):
            self._status = "Failed - can't update geometry element"
            return False

        return True
