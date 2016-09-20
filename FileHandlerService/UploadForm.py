import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from Scripts.UploadScript import UploadScript
from tornado.options import define, options


class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")


class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print "file name is", fileinfo['filename']

        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]

        UploadScript(fileinfo['body'], extn)

        print "finished upload"
        self.render("fileuploadform.html")


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
    application = tornado.web.Application([
        (r"/", Userform),
        (r"/upload", Upload),
    ], debug=False)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
