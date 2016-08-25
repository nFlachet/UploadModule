class AbstractModule:
    def __init__(self, postgresDataManager, schema_id):
        self.schemaID = schema_id
        self._pdm = postgresDataManager
        self.responseData = {}

    def create_schema_request(self, request):
        return """  SET SCHEMA '{}';
                    {}""".format(self.schemaID, request)