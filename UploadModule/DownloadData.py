import UploadModule.AbstractModule as am

import sys
import os
import logging


class DownloadModule(am.AbstractModule):

    def download_data(self, dirname):
        if not self._pdm.check_if_schema_exists(self._schemaID):
            self._status += "Failed - schema for case and variant doesn't exist"
        else:
            for key, value in self._valid_gml_type.iteritems():
                filename = dirname + os.sep + value +".csv".replace(os.sep, '/')
                self._download_table(key, value, filename)

        logging.debug(self._status)
        return self._status

    def _download_table(self, type, table_name, filename):
        schema_table = "{}.{}".format(self._schemaID, table_name)

        with open(filename, mode='w') as f:
            f.write('Case_ID;' + self._caseID + ';\n')
            f.write('Variant_ID;' + self._variantID + ';\n')
            f.write('Type;' + type + ';\n')

        if not self._pdm.copy_to_csv_file(filename, schema_table):
            self._status += "Failed - can't save table \n".format(table_name)
