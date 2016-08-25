import psycopg2
import sys
import logging


class PostgresDataManager:
    def __init__(self):
        self.conn = None
        self.isConnected = False

    def __del__(self):
        if self.isConnected:
            self.conn.close()

    def connect(self, host, db_name, user, password, port):
        self.isConnected = False
        try:
            self.conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password, port=port)
            self.isConnected = True
            logging.info("database is connected")
        except psycopg2.Error as e:
            print "I am unable to connect to the database"
            print e.pgerror
            print e.diag.message_detail
            logging.error("Unable to connect {} {}".format(e.pgerror, e.diag.message_detail))
            logging.error("Unable to connect db {}, user {}, host {}, port {}".format(db_name, user, host, port))
            sys.exit(1)

    def is_connected(self):
        return self.isConnected

    def execute_request(self, request):
        if self.isConnected:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(request)
                except:
                    return False
        return True

    def commit_transactions(self):
        self.conn.commit()

    def rollback_transactions(self):
        self.conn.rollback()

    def get_data_value(self, request, cast):
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                raw_data = cur.fetchone()
                data = raw_data[0] if type(raw_data) is tuple else raw_data
                if data is not None:
                    if cast is not None:
                        return cast(data)
                    else:
                        return data
        return 0

    def get_data_list_values(self, request):
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                return cur.fetchall()
        return []

    def create_schema(self, schema_id, from_schema_id='public'):
        request = """SELECT clone_schema('{}','{}', TRUE);""".format(from_schema_id, schema_id)
        if self.execute_request(request):
            self.commit_transactions()
            return "Success - schema created"
        else:
            self.rollback_transactions()
            return "Failed - can't create schema"

    def delete_schema(self, schema_id):
        request = """SELECT drop_schemas('{}');""".format(schema_id)
        if self.execute_request(request):
            self.commit_transactions()
            return "Success - schema deleted"
        else:
            self.rollback_transactions()
            return "Failed - can't delete schema"

    def check_if_schema_exists(self, schema_id):
        request = """SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{}';""".format(schema_id);
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                raw_data = cur.fetchone()
                data = raw_data[0] if type(raw_data) is tuple else raw_data
                if data is not None:
                    return True
        return False

    def copy_to_csv_file(self, outputfile, table_name):
        if self.isConnected:
            with open(outputfile, mode='a') as f:
                with self.conn.cursor() as cur:
                    cur.copy_to(f, table_name, sep=';')
            return True

        return False
