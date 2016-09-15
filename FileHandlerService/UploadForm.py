import tornado.web
import os
from Scripts.UploadScript import UploadScript


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


application = tornado.web.Application([
        (r"/", Userform),
        (r"/upload", Upload),
        ], debug=True)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()