import DataManager as DataManager


class AbstractModule:
    def __init__(self, host, db_name, user, pwd, port):
        self._pdm = DataManager.PostgresDataManager()
        self._pdm.connect(host, db_name, user, pwd, port)
        self._status = ""
        self._prefix = 'trout_'
        self._schemaID = ''
        self._caseID = ''
        self._variantID = ''
        self._valid_srs_list = ['urn:ogc:def:crs:OGC:1.3:CRS84']
        self._valid_gml_type = {'BUILDINGS':'building', 'DISTRICT':'district', 'SPACES':'space' }

    def _create_schema_request(self, request):
        return """  SET SCHEMA '{}';
                    {}""".format(self._schemaID, request)

    def set_schema_id(self, case_id, variant_id):
        base_schema_id = case_id if variant_id is '' or variant_id is None or variant_id is 'null' else case_id + "_" + variant_id
        self._schemaID = self._prefix + base_schema_id

