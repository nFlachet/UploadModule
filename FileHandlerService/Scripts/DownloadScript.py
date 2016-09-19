import UploadModule.DownloadData as DownloadData

import os
import sys
import getopt
import logging


def main(argv=None):

    logging.basicConfig(filename='DownloadModule.log', level=logging.DEBUG)
    logging.FileHandler('DownloadModule.log', mode='w')

    host = '10.9.10.183'
    db_name = 'Warsaw'
    user = 'tournaire'
    password = 'olivier'
    port = '5432'

    dirname = '.'
    case_id = '57b428a6cef25a0a0d6681ac'
    variant_id = ''

    try:
        logging.info("currents args are: {}".format(sys.argv[1:]))
        opts, args = getopt.getopt(sys.argv[1:], "h:d:u:P:p:f:c:v:", ["host=", "dbname=", "user=", "password", "port=", "dirname=", "case=", "variant="])
    except getopt.GetoptError:
        logging.warning('run DownloadScript.py -h <host> -d <database name> -u <user> -P <password> -p <port> -f <dirname> -c <case> -v <variant>')
        logging.warning('or DownloadScript.py --host <host> --dbname <database name> --user <user> --password <password> --port <port> --dirname <dirname>, --case <case> --variant <variant>')
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
        elif opt in ('-f', '--dirname'):
            dirname = arg
        elif opt in ('-c', '--case'):
            case_id = arg
        elif opt in ('-v', '--variant'):
            variant_id = arg

    downloader = DownloadData.DownloadModule(host, db_name, user, password, port)
    downloader.set_schema_id(case_id, variant_id)
    downloader.download_data( os.path.abspath(dirname) )
    logging.info('finished')

if __name__ == "__main__":
    main()
