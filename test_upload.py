# coding: utf-8
import tornado.ioloop
import tornado.web
import shutil
import os
import json


class FileUploadHandler(tornado.web.RequestHandler):


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers","Content-Type, Content-Length, Authorization, Accept, X-Requested-With, X-File-Name, yourHeaderFeild")
        self.set_header("Access-Control-Allow-Methods", " POST, GET, OPTIONS, HEAD,PUT,DELETE")
        self.set_header("X-Powered-By","3.2.1")
        self.set_header("Content-Type","application/x-www-form-urlencoded")

    def get(self):
        pass

    def post(self):
        ret = {'result': 'OK'}
        upload_path = os.path.join(os.path.dirname(__file__), 'files')  # 文件的暂存路径
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据

        # if not file_metas:
        #     ret['result'] = 'Invalid Args'
        #     return ret
        print '==========request files============'
        print self.request.files
        print '==========request body======'
        print self.request.body

        print type(self.request.body)
        print '=========request headers======='
        #print file_metas
        print self.request.headers
        print '=========request arguments======='
        print self.request.arguments
        print '==========request body arguments======'
        print self.request.body_arguments
        print '================'
        for key in self.request.body_arguments:
            print key
            print self.request.body_arguments[key]
            print type(self.request.body_arguments[key])

        user_name = self.get_argument('password','laowang')
        print user_name,' <--------- password '

        dd = self.request.body
        dd = json.loads(dd)
        print type(dd)
        print dd.get('userName','123')
        print dd.get('password','123')
        #


        # print self.request.arguments['usename']
        #
        # print self.request.body['usename']
        # data = self.request.body
        # data = json.loads(data)
        # print data['username']
        # print '================'

        for file_upload in self.request.files:
            print type(self.request.files)
            print '===========file_upload==========='
            print file_upload
            print self.request.files[file_upload]
            print type(self.request.files[file_upload])
            print len(self.request.files[file_upload])
            for upload_file in self.request.files[file_upload]:
                file_path = os.path.join(upload_path, upload_file['filename'])
                with open(file_path, 'wb') as up:
                    up.write(upload_file['body'])
                    # OR do other thing

        self.write(json.dumps(ret))
        self.set_header("Content-Type", "application/json")


app = tornado.web.Application([
    (r'/api/file', FileUploadHandler),
])

if __name__ == '__main__':
    app.listen(8080)
    print 'start'
    tornado.ioloop.IOLoop.instance().start()