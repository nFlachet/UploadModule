import UploadModule.UploadData as UploadData

import sys
import getopt
import logging


class UploadScript:
    def __init__(self, file, extension, case_id, variant_id):
        logging.basicConfig(filename='UploadModule.log', level=logging.DEBUG)
        logging.FileHandler('UploadModule.log', mode='w')

        host = '10.9.10.183'
        db_name = 'Warsaw'
        user = 'tournaire'
        password = 'olivier'
        port = '5432'

        #host = 'vps17642.public.cloudvps.com'
        #db_name = 'Warsaw'
        #user = 'postgres'
        #password = 'x0mxaJc69J9KAlFNsaDt'
        #port = '5443'

        try:
            logging.info("currents args are: {}".format(sys.argv[1:]))
            opts, args = getopt.getopt(sys.argv[1:], "h:d:u:P:p:f:", ["host=", "dbname=", "user=", "password", "port=", "filename="])
        except getopt.GetoptError:
            logging.warning('run UploadScript.py -h <host> -d <database name> -u <user> -P <password> -p <port> -f <filename> ')
            logging.warning('or UploadScript.py --host <host> --dbname <database name> --user <user> --password <password> --port <port> --filename <filename>')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--host'):
                host = arg
            elif opt in ('-d', '--dbname'):
                db_name = arg
            elif opt in ('-u', '--user'):
                user = arg
            elif opt in ('-P', '--password'):
                password = arg
            elif opt in ('-p', '--port'):
                port = arg
            elif opt in ('-f', '--filename'):
                filename = arg

        logging.info("Starting UploadModule.")

        uploader = UploadData.UploadModule(host, db_name, user, password, port, case_id, variant_id)
        self._status = uploader.upload_data(file, extension)
        logging.info('finished')

    def getStatus(self):
        return self._status
