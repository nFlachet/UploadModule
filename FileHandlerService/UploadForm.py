import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from Scripts.UploadScript import UploadScript
from tornado.options import define, options


class Upload(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self):
        (case_id, variant_id, user_id) = self.get_argument("session").split("$")
        self.database['case_id'] = case_id
        if variant_id == 'undefined':
            self.database['variant_id'] = None
        else:
            self.database['variant_id'] = variant_id
        self.database['user_id'] = user_id
        self.render("fileuploadform.html", statusText="")

    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print "file name is", fileinfo['filename']

        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]

        UploaderScript = UploadScript(fileinfo['body'], extn, self.database['case_id'], self.database['variant_id'])

        self.render("fileuploadform.html", statusText=UploaderScript.getStatus())



# application = tornado.web.Application([
#         (r"/", Userform),
#         (r"/upload", Upload),
#         ], debug=True)
#
#
# if __name__ == "__main__":
#     application.listen(8888)
#     tornado.ioloop.IOLoop.instance().start()


define("port", default=8888, help="run on the given port", type=int)

def main():
    mydatabase = dict()
    application = tornado.web.Application([
        (r"/", Upload, dict(database=mydatabase)),
    ], debug=False)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
