#coding:utf8
import json
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import mysql_helper
mylog = mysql_helper.mylog


class BaseHandler(tornado.web.RequestHandler):

    def get(self):
        self.write_to_client('get for base handler')

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers","Content-Type, Content-Length, Authorization, Accept, X-Requested-With, X-File-Name, yourHeaderFeild")
        self.set_header("Access-Control-Allow-Methods", " POST, GET, OPTIONS, HEAD")
        self.set_header("X-Powered-By","3.2.1")
        self.set_header("Content-Type","application/x-www-form-urlencoded")

    def post(self):
        self.write_to_client('post for base handler')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def write_to_client(self, message):
        self.write(json.dumps(message))
        self.set_header("Content-Type", "application/json")


class LoginHandler(BaseHandler):

    def get(self):
        message = {"code": 1, "msg": 'test for login', "data": ""}
        self.write_to_client(message)

    def post(self):
        data = self.request.body
        self.process(data)

    def process(self, data):
        mvmh = None
        try:
            mvmh = mysql_helper.ModelVerifyMySQLHelper()
            mylog.info('param for /api/user/login : %s' % str(data))
            data = json.loads(data)
            name = data.get('userName','')
            passwd = data.get('password','')
            if name=='' or passwd=='':
                raise AssertionError('user name or password is empty')
            passwd = mysql_helper.str_sha256(passwd)
            result = mvmh.user_validate(name,passwd)
            if not result is None:
                message = {"code": 1, "msg": "success", "data": {"userInfo":result}}
            else:
                message = {"code": 0, "msg":'fail to validate user name and password ', "data": ""}
        except Exception as e:
            message = {"code": 0, "msg": str(e), "data": ""}
        if mvmh:
            mylog.info('respon for /api/user/login : %s' % str(message))
            del mvmh
        self.write_to_client(message)

class UserLogoutHandler(BaseHandler):

    def get(self):
        message = {"code": 1, "msg": 'test for login', "data": ""}
        self.write_to_client(message)

    def post(self):
        data = self.request.body
        self.process(data)

    def process(self, data):
        mvmh = None
        try:
            mvmh = mysql_helper.ModelVerifyMySQLHelper()
            mylog.info('param for /api/user/logout : %s' % str(data))
            data = json.loads(data)
            token = data.get('token','')
            if token=='':
                raise AssertionError('token is empty')
            token = mvmh.user_validate_token(token)
            if token is None:
                message = {"code": 0, "msg": "token error", "data": ''}
            else:
                user_name = token['userName']
                result = mvmh.user_logout(user_name)
                if result:
                    mylog.info('success logout')
                    message = {"code": 1, "msg": 'success logout', "data": ""}
                else:
                    mylog.error('error logout')
                    message = {"code": 0, "msg": 'error logout', "data": ""}
        except Exception as e:
            mylog.error('error logout %s'%str(e))
            message = {"code": 0, "msg": str(e), "data": ""}
        if mvmh:
            mylog.info('respon for /api/user/logout : %s' % str(message))
            del mvmh
        self.write_to_client(message)

class UserPasswordHandler(BaseHandler):

    def get(self):
        message = {"status": 1, "message": 'test for user password', "data": ""}
        self.write_to_client(message)

    def post(self):
        data = self.request.body
        self.process(data)

    def process(self, data):
        mvmh = None
        try:
            mvmh = mysql_helper.ModelVerifyMySQLHelper()
            mylog.info('param for /api/user/password : %s' % str(data))
            data = json.loads(data)
            token = data.get('token', '')
            if token == '':
                raise AssertionError('token is empty')
            token = mvmh.user_validate_token(token)
            if token is None:
                message = {"code": 0, "msg": "token error", "data": ''}
            else:
                user_name = token['userName']
                old_password = data.get('oldPassword','')
                if old_password=='':
                    raise AssertionError('old password is empty')
                old_password = mysql_helper.str_sha256(old_password)
                new_password = data.get('newPassword','')
                if new_password=='':
                    raise AssertionError('new password is empty')
                new_password = mysql_helper.str_sha256(new_password)
                result = mvmh.user_change_password(user_name,old_password,new_password)
                if not result :
                    message = {"code": 0, "msg": "error change password in sql", "data": ''}
                else:
                    message = {"code": 1, "msg": "success change password", "data": ''}
        except Exception as e:
            message = {"code": 0, "msg": str(e), "data": ""}
        if mvmh:
            mylog.info('respon for /api/user/password : %s' % str(message))
            del mvmh
        self.write_to_client(message)

class AdminEditUserHandler(BaseHandler):

    def get(self):
        message = {"status": 1, "message": 'test for admin edit user', "data": ""}
        self.write_to_client(message)

    def post(self):
        data = self.request.body
        self.process(data)

    def process(self, data):
        mvmh = None
        try:
            mvmh = mysql_helper.ModelVerifyMySQLHelper()
            mylog.info('param for /api/admin/editUser : %s' % str(data))
            data = json.loads(data)
            token = data.get('token', '')
            if token == '':
                raise AssertionError('token is empty')
            token = mvmh.user_validate_token(token)
            if token is None:
                mylog.warning('token error')
                message = {"code": 0, "msg": "toekn error", "data": ''}
            else:
                mylog.info('token pass')
                if token['roleType'] == 'admin':
                    mylog.info('token admin')
                    user_id = data.get('userId','')
                    user_name = data.get('userName','')
                    password = data.get('password','')
                    total_space = data.get('totalSpace','')
                    role_type = data.get('roleType','user')
                    status = data.get('status','')
                    if user_id == '':
                        if total_space =='':
                            total_space=500
                        total_space = int(total_space)
                        if user_name=='' or password=='':
                            raise AssertionError('user name or password is empty')
                        password = mysql_helper.str_sha256(password)
                        new_user = mvmh.admin_create_user(user_name,password,role_type,total_space)
                        if not new_user is None:
                            message = {"code": 1, "msg": "success create user", "data": new_user}
                        else:
                            message = {"code": 0, "msg": "fail create user", "data": ''}
                    else:
                        user_id = int(user_id)
                        #if not ((password=='' and total_space=='') or (password=='' and status=='') or (total_space=='' and status=='')):
                        if (password != '' or total_space != '') and (password != '' or status != '') and (
                                total_space != '' or status != ''):
                            raise AssertionError('password,total space,status only need one param(other two should be empty) when editing user')
                        if password=='' and total_space=='' and status=='':
                            raise AssertionError('password,total space,status can not be empty at the same time when editing user')
                        if not password == '':
                            password = mysql_helper.str_sha256(password)
                            password_result = mvmh.admin_reset_password(user_id,password)
                            if password_result:
                                mylog.info("success reset password ")
                                message = {"code": 1, "msg": "success reset password ", "data": ''}
                            else:
                                mylog.error("error reset password in sql ")
                                message = {"code": 0, "msg": "error reset password in sql ", "data": ''}
                        if not total_space =='':
                            total_space = float(total_space)
                            total_space_result = mvmh.admin_reset_space(user_id,total_space)
                            if total_space_result:
                                mylog.info("success reset space to %.0f MB "%total_space)
                                message = {"code": 1, "msg": "success reset space", "data": total_space}
                            else:
                                mylog.error("error reset space in sql")
                                message = {"code": 0, "msg": "error reset space in sql", "data":'' }
                        if not status == '':
                            status_result = mvmh.admin_reset_status(user_id,status)
                            if status_result:
                                mylog.info("success reset status")
                                message = {"code": 1, "msg": "success reset status", "data": status}
                            else:
                                mylog.error("error reset status in sql")
                                message = {"code": 0, "msg": "error reset status in sql", "data": ''}
                else:
                    mylog.error('need admin')
                    message = {"code": 0, "msg": "need admin", "data": ''}
        except Exception as e:
            message = {"code": 0, "msg": str(e), "data": ""}
        if mvmh:
            mylog.info('respon for /api/admin/editUser : %s' % str(message))
            del mvmh
        self.write_to_client(message)

class AdminListUserHandler(BaseHandler):
    def get(self):
        message = {"status": 1, "message": 'test for get model', "data": ""}
        self.write_to_client(message)

    def post(self):
        data = self.request.body
        self.process(data)

    def process(self, data):
        mvmh = None
        try:
            mvmh = mysql_helper.ModelVerifyMySQLHelper()
            mylog.info('param for /api/admin/listUser : %s' % str(data))
            data = json.loads(data)
            token = data.get('token', '')
            if token == '':
                raise AssertionError('token is empty')
            token = mvmh.user_validate_token(token)
            if token is None:
                mylog.warning('token error')
                message = {"code": 0, "msg": "toekn error", "data": ''}
            else:
                mylog.info('token pass')
                if token['roleType'] == 'admin':
                    mylog.info('token admin')
                    user_name_key = data.get('userNameKey','')
                    role_type = data.get('roleType','')
                    status = data.get('status','')
                    page_size = data.get('pageSize',0)
                    page_index = data.get('pageIndex',0)
                    if page_index==0 or page_index==0:
                        raise AssertionError('page index or page size =0')
                    user_list = mvmh.admin_list_users(status,user_name_key,role_type,page_size,page_index)
                    if user_list is None:
                        mylog.error('error search in sql')
                        message = {"code": 0, "msg": "error search in sql", "data": ''}
                    else:
                        mylog.info("success search in sql")
                        message = {"code": 1, "msg": "success search in sql", "data":user_list}
                else:
                    mylog.error('need admin')
                    message = {"code": 0, "msg": "need admin", "data": ''}
        except Exception as e:
            message = {"code": 0, "msg": str(e), "data": ""}
        if mvmh:
            mylog.info('respon for /api/admin/editUser : %s' % str(message))
            del mvmh
        self.write_to_client(message)

def web():

    tornado.options.parse_command_line()
    url = [(r'/api',BaseHandler),(r'/api/user/login',LoginHandler),(r'/api/user/password',UserPasswordHandler),
           (r'/api/admin/editUser',AdminEditUserHandler),(r'/api/admin/listUser',AdminListUserHandler),
           (r'/api/user/logout',UserLogoutHandler),]
    application = tornado.web.Application(handlers=url)
    http_server = tornado.httpserver.HTTPServer(application)
    mvmh = mysql_helper.ModelVerifyMySQLHelper()
    port = mvmh.config.getPort()
    host = mvmh.config.getHost()
    del mvmh
    http_server.listen(port)

    print("server is running at {0}:{1}".format(host,port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    web()