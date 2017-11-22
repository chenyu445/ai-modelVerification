#coding:utf-8
import MySQLdb as mdb
import time
import base64
import hashlib
import datetime
import csv
import os
from Utils import conf,LogUtils
from qiniu import Auth

base_name = os.path.basename(__file__)
name = base_name.split('.')[0]
mylog = LogUtils.MyLog(os.path.join('/tmp', name) + '.log')

save_path = os.path.abspath(__file__)
save_path = save_path[:-len(save_path.split(os.sep)[-1])]


def str_sha256(passwd):
    sha256 = hashlib.sha256()
    sha256.update(passwd)
    return sha256.hexdigest()

def get_file_size(file_path):
    #mb
    fsize = os.path.getsize(file_path)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)

def get_token(name,passwd):
    head = time.strftime('%Y-%m-%d-%H-%M-%S')
    sstr = '{"name":%s,"passwd":%s,"time":%s}'%(name,passwd,head)
    return base64.b64encode(sstr)


def next_day_str(date_str):
    start = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start = start + datetime.timedelta(days=1)
    start = start.strftime('%Y-%m-%d')
    return start

def today_str(date_str):
    start = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    start = start.strftime('%Y-%m-%d')
    return start

def md5_for_file(file_path, block_size=2**20):
    f = open(file_path,'rb')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()

class ModelVerifyMySQLHelper():

    def __init__(self,baseName=None,enableQiniu=False):
        conf_name = 'config.conf'
        root_path = os.path.dirname(__file__)
        conf_path = os.path.join(root_path, 'Utils')
        self.conf_path = os.path.join(conf_path, conf_name)
        self.config = conf.Config(self.conf_path)
        self.save_path = 'save'
        self.total_space = 500
        self.conn = None
        self.cur = None
        try:
            self.baseName, self.host, self.user, self.passwd, self.port = self.config.getDataBaseInfo()
            self.conn = mdb.connect(host=self.host, user=self.user, passwd=self.passwd,charset='utf8', port=int(self.port))
            self.cur = self.conn.cursor()
            if enableQiniu:
                self.accessKey = self.config.getQiNiuAccessKey()
                self.secretKey = self.config.getQiNiuSecretKey()
                if self.accessKey and self.secretKey:
                    self.q = Auth(self.accessKey,self.secretKey)
                    if self.q is None:
                        mylog.error('init qiuniu key error')
                        raise AssertionError('init qiuniu key error')
                    else:
                        mylog.info('init qiniu key success')
                else:
                    mylog.error('init qiuniu key error')
                    raise AssertionError('init qiuniu key error')
            if baseName is None:
                self.conn.select_db(self.baseName)
            self.init  = True
            mylog.info('success init dataBasemManager')
        except Exception as e:
            self.init = False
            mylog.warning('fail to init dataBasemManager : %s'%str(e))

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        mylog.info('dataBaseManager id : %s'%str(id(self)))
        mylog.info('del dataBaseManager')

    def createDb(self):

        user_sql = 'create table if not exists user(user_id int PRIMARY KEY auto_increment,' \
                     'user_name varchar(32) not NULL unique key,' \
                     'password varchar(200) not NULL,' \
                     'last_login datetime not NULL,' \
                     'status varchar(32) not null,' \
                     'role_type varchar(32) not null,' \
                     'password_status varchar(32) not null,' \
                     'total_space int not null,' \
                     'used_space int not null,' \
                     'token varchar(200),' \
                     'favorite_model_id int,' \
                     'create_time  datetime DEFAULT CURRENT_TIMESTAMP, ' \
                     'update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) character set = utf8'

        model_sql = 'create table if not exists model(model_id int PRIMARY KEY auto_increment,' \
                     'model_name varchar(200) not NULL unique key,' \
                     'newest_version_name varchar(32) not null,' \
                     'model_logo varchar(200),' \
                     'model_desc varchar(2000),' \
                     'create_time  datetime DEFAULT CURRENT_TIMESTAMP, ' \
                     'update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) character set = utf8'

        model_detail_sql = 'create table if not exists model_detail(model_detail_id int PRIMARY KEY auto_increment,' \
                           'model_id int not null,' \
                           'model_name varchar(200) not null,' \
                           'model_version_name varchar(200) not null,' \
                           'model_size int not null,' \
                           'create_time  datetime DEFAULT CURRENT_TIMESTAMP, ' \
                           'update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) character set = utf8'

        upload_file_sql = 'create table if not exists upload_file(upload_file_id int PRIMARY KEY auto_increment,' \
                          'upload_file_name varchar(200) not NULL ,' \
                          'model_id int not null,' \
                          'model_detail_id int not null, ' \
                          'modified_name varchar(200) not null,' \
                          'upload_file_md5 varchar(32) not null,' \
                          'uploader varchar(32) not null, ' \
                          'upload_file_size int not null, ' \
                          'status varchar(32) not null,' \
                          'visable varchar(32),' \
                          'count int not null,' \
                          'create_time  datetime DEFAULT CURRENT_TIMESTAMP, ' \
                          'update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) character set = utf8'

        validate_task_sql = 'create table if not exists validate_task(validate_task_id int PRIMARY KEY auto_increment,' \
                            'model_name varchar(200) not null,' \
                            'model_version_name varchar(200) not null,' \
                            'upload_file_id int not NULL,' \
                            'validate_start_time datetime not null,' \
                            'validate_time_cost int not null) character set = utf8'

        validate_detail_sql = 'create table if not exists validate_detail(validate_detail_id int PRIMARY KEY auto_increment,' \
                              'validate_task_id int not NULL,' \
                              'upload_file_id int not null,' \
                              'validate_data varchar(2000) not null) character set = utf8'

        if self.init:
            try:
                self.cur.execute('create database if not exists %s' % self.baseName)
                self.conn.select_db(self.baseName)
                self.cur.execute(user_sql)
                self.cur.execute(model_sql)
                self.cur.execute(model_detail_sql)
                self.cur.execute(upload_file_sql)
                self.cur.execute(validate_task_sql)
                self.cur.execute(validate_detail_sql)
                self.conn.commit()
                mylog.info('success creating database %s'%self.baseName)
            except Exception as e:
                mylog.error('fail to create database %s   : %s' % (self.baseName,str(e)))


    def admin_create_user(self,name,password,role_type='user',total_space=500):
        flag = None
        try:
            # if role_type=='admin':
            #     total_space = 0
            values = [name,password,role_type,total_space]
            create_user_sql = 'insert user(user_name,password,role_type,total_space,' \
                              'last_login,status,used_space,password_status) ' \
                              'values(%s,%s,%s,%s,now(),"inuse",0,"new")'
            self.cur.execute(create_user_sql,values)
            flag = self.help_get_user_info_by_name(name)
            self.conn.commit()
            mylog.info('success insert user %s'%name)
        except Exception as e:
            mylog.error('error create user %s   :%s'%(name,str(e)))
        return flag

    def help_get_user_info_by_name(self,user_name):
        user_info = None
        try:
            user_validate_sql = 'select user_id,user_name,last_login,status,role_type,password_status,' \
                                'total_space,used_space from user where user_name=%s'
            self.cur.execute(user_validate_sql, [user_name])
            results = self.cur.fetchall()
            if len(results) == 1:
                last_login = results[0][2]
                last_login = last_login.strftime('%Y-%m-%d %H:%M:%S')
                user_info = {'userId': results[0][0], 'userName': results[0][1], 'lastLogin': last_login,
                             'status': results[0][3], 'roleType': results[0][4], 'passwordStatus': results[0][5],
                             'totalSpace': results[0][6], 'usedSpace': results[0][7]}
                mylog.info('success validate user and passwd')
            else:
                mylog.error('fail to find user and passwd in sql')
        except Exception as e:
            mylog.error('fail to validate user and passwd %s' % str(e))
        return user_info




    def user_validate(self,user,password):
        user_info= None
        try:
            user_validate_sql = 'select user_id,user_name,last_login,status,role_type,password_status,' \
                                'total_space,used_space from user where user_name=%s and password=%s'
            self.cur.execute(user_validate_sql, [user,password])
            results = self.cur.fetchall()
            if len(results)==1:
                token = get_token(user,password)
                update_token_sql = 'update user set token=%s  where user_name=%s'
                self.cur.execute(update_token_sql,[token,user])
                update_last_login_sql = 'update user set last_login=now()  where user_name=%s'
                self.cur.execute(update_last_login_sql, [user])
                self.conn.commit()
                last_login = results[0][2]
                last_login = last_login.strftime('%Y-%m-%d %H:%M:%S')
                user_info = {'userId':results[0][0],'userName':results[0][1],'lastLogin':last_login,
                            'status':results[0][3],'roleType':results[0][4],'passwordStatus':results[0][5],
                            'totalSpace':results[0][6],'usedSpace':results[0][7],'token':token}
                mylog.info('success validate user and passwd')
            else:
                mylog.error('fail to find user and passwd in sql')
        except Exception as e:
            mylog.error('fail to validate user and passwd %s' % str(e))
        return user_info

    def user_logout(self,user_name):
        result = False
        try:
            logout_sql = 'update user set token=%s where user_name=%s'
            self.cur.execute(logout_sql,[None,user_name])
            self.conn.commit
            result = True
            mylog.info('success logout user_id : %s'%str(user_name))
        except Exception as e:
            mylog.error('error logout %s'%str(e))
        return result

    def user_change_password(self,user,old_password,new_password):
        result = False
        try:
            select_user_sql = 'select * from user where user_name=%s and password=%s'
            self.cur.execute(select_user_sql,[user,old_password])
            results = self.cur.fetchall()
            if len(results) == 1:
                mylog.info(' user and password pairs')
                reset_password_sql = 'update user set password=%s where user_name=%s'
                self.cur.execute(reset_password_sql,[new_password,user])
                self.conn.commit()
                result = True
                mylog.info('success reset password')
        except Exception as e:
            mylog.error('error reset password : %s'%str(e))
        return result


    def user_delete_file(self,file_id,user_name):
        result = False
        try:
            select_file_sql = 'select modified_name from upload_file where file_id=%s and uploader=%s'
            self.cur.execute(select_file_sql,[file_id,user_name])
            modified_name = self.cur.fetchall()[0][0]
            user_save_path = os.path.join(save_path,user_name)
            file_save_path = os.path.join(user_save_path,modified_name)
            if os.path.exists(file_save_path):
                os.remove(file_save_path)
            delete_file_sql = 'update upload_file set visable="invisable" where file_id=%s and uploader=%s'
            self.cur.execute(delete_file_sql,[file_id,user_name])
            self.conn.commit()
            result = True
            mylog.info('success delete file ')
        except Exception as e:
            mylog.error('fail to delete file : %s'%str(e))
        return  result


    def user_validate_token(self,token):

        #通过token查询数据库，返回唯一值则判断时间是否超时,是否启用，通过后返回用户名和roletype
        result = None
        try:
            user_validate_sql = 'select last_login,status,user_name,role_type from user where token=%s'
            self.cur.execute(user_validate_sql, [token])
            results = self.cur.fetchall()
            if len(results) == 1:
                tokenTime = results[0][0]
                delta = datetime.timedelta(minutes=60*24)
                serverTime = datetime.datetime.now()
                if tokenTime > serverTime-delta:
                    status = results[0][1]
                    if status=='inuse':
                        result = {'userName':results[0][2],"roleType":results[0][3]}
                        mylog.info('success validating user %s by token' %results[0][2])
                    else:
                        mylog.error('user %s not inuse at the moment' % results[0][2])
                else:
                    mylog.error('token out of time')
            else:
                mylog.error('can not find token in sql')
        except Exception as e:
            mylog.error('fail to validate by token : %s'%str(e))
        return result

    def admin_reset_password(self,user_id,password):
        #need change password_status
        result = False
        try:
            reset_password_sql = 'update user set password=%s where user_id=%s'
            self.cur.execute(reset_password_sql, [passwd, user_id])
            mylog.info('success reset user_id %s password' % (user_id))
            reset_password_status_sql = 'update user set password_status="new" where user_id=%s'
            self.cur.execute(reset_password_status_sql,[user_id])
            self.conn.commit()
            mylog.info('success reset user_id %s password status' % (user_id))
            result = True
        except Exception as e:
            mylog.error('fail to reset password  %s ' % str(e))
        return result

    def admin_reset_space(self,user_id,total_space):
        result = False
        try:
            reset_space_sql = 'update user set total_space=%s where user_id=%s'
            self.cur.execute(reset_space_sql, [total_space,user_id])
            self.conn.commit()
            mylog.info('success reset user_id %s total space to %s MB' %(user_id,total_space))
            result = True
        except Exception as e:
            mylog.error('fail to reset status  %s ' % str(e))
        return result

    def admin_reset_status(self,user_id,status):
        result = False
        try:
            reset_status_sql = 'update user set status=%s where user_id=%s'
            self.cur.execute(reset_status_sql, [status,user_id])
            self.conn.commit()
            mylog.info('success reset user_id %s to status : %s' %(user_id,status))
            result = True
        except Exception as e:
            mylog.error('fail to reset status  %s ' % str(e))
        return result

#select * from user where create_time<'2017-09-27' and create_time>'2017-09-26';
#select * from user where user_name like '%王%' limit 0,5;
#update user set password='new' where user_id=1;


    def admin_list_users(self,status,user_name_key,role_type,page_size,page_index):
        user_list = None
        try:
            start = page_size*(page_index-1)
            list_user_sql_head = 'select user_id,user_name,last_login,status,role_type,' \
                                 'password_status,total_space,used_space from user where user_id>0 '
            list_user_sql_tail= ' limit %s,%s'
            values = []
            if not status=='':
                list_user_sql_head +=' and status=%s '
                values.append(status)
            if not user_name_key == '':
                list_user_sql_head += ' and user_name like %s '
                values.append('%'+user_name_key+"%")
            if not role_type == '':
                list_user_sql_head += ' and role_type=%s '
                values.append(role_type)
            list_user_sql_head += list_user_sql_tail
            values.append(start)
            values.append(page_size)
            mylog.info('total sql : %s'%list_user_sql_head)
            mylog.info('total values : %s'%values)
            self.cur.execute(list_user_sql_head, values)
            users = self.cur.fetchall()
            user_list = []
            for user in users:
                last_login = user[2]
                last_login = last_login.strftime('%Y-%m-%d %H:%M:%S')
                user_info = {'userId':user[0],'userName':user[1],'lastLogin':last_login,
                            'status':user[3],'roleType':user[4],'passwordStatus':user[5],
                            'totalSpace':user[6],'usedSpace':user[7]}
                user_list.append(user_info)
            mylog.info('success get user list')
        except Exception as e:
            mylog.error('fail to get user list : %s' % str(e))
        return user_list

    # def admin_select_users(self,model_name_key,page_size,page_index):
    #     user_list = []
    #     try:
    #         start = page_size*(page_index-1)
    #         select_user_sql = 'select user_id,user_name,last_login,status,role_type,password_status,total_space,free_space from user where user_name like %s limit %s,%s'
    #         self.cur.execute(select_user_sql, ['%'+model_name_key+'%',start, page_size])
    #         users = self.cur.fetchall()
    #         for user in users:
    #             user_info = {'userId':user[0],'userName':user[1],'lastLogin':user[2],
    #                         'status':user[3],'roleType':user[4],'passwordStatus':user[5],
    #                         'totalSpace':user[6],'freeSpace':user[7]}
    #             user_list.append(user_info)
    #         mylog.info('success select user list')
    #     except Exception as e:
    #         mylog.error('fail to select user list : %s' % str(e))
    #     return user_list


    def user_list_models(self,user_name,role_type,page_size,page_index):
        #根据权限返回modelid modelname newestversion uploadfilecount（所有的和用户自己的），需要加入模型的最新3个版本
        model_list = []
        try:
            start = page_size*(page_index-1)
            list_model_sql = 'select model_id,model_name,newest_version_name from model limit %s,%s'
            self.cur.execute(list_model_sql, [start, page_size])
            models = self.cur.fetchall()
            for model in models:
                if role_type=='admin':
                    select_all_user_sql = 'select count(*) from upload_file where model_id=%s'
                    upload_file_count = self.cur.execute(select_all_user_sql,[model[0]])
                else:
                    select_file_count_sql = 'select count(*) from upload_file where model_id=%s and uploader=%s'
                    upload_file_count = self.cur.execute(select_file_count_sql,[model[0],user_name])
                model_info = {'modelId': model[0], 'modelName': model[1], 'newestVersionName': model[2],
                                  'uploadFileCount': upload_file_count}
                model_list.append(model_info)
            mylog.info('success get model list')
        except Exception as e:
            mylog.error('fail to get model list : %s' % str(e))
        return model_list

    def user_select_models(self,user_name,role_type,model_name_key,page_size,page_index):
        # 根据权限返回modelid modelname newestversion uploadfilecount（所有的和用户自己的），加入关键字搜索
        model_list = []
        try:
            start = page_size*(page_index-1)
            select_model_sql = 'select model_id,model_name,newest_version_name ' \
                               'from model where model_name like %s limit %s,%s'
            self.cur.execute(select_model_sql, ['%'+model_name_key+'%',start, page_size])
            models = self.cur.fetchall()
            for model in models:
                if role_type=='admin':
                    select_all_user_sql = 'select count(*) from upload_file where model_id=%s'
                    upload_file_count = self.cur.execute(select_all_user_sql,[model[0]])
                else:
                    select_file_count_sql = 'select count(*) from upload_file where model_id=%s and uploader=%s'
                    upload_file_count = self.cur.execute(select_file_count_sql,[model[0],user_name])
                model_info = {'modelId': model[0], 'modelName': model[1], 'newestVersionName': model[2],
                                  'uploadFileCount': upload_file_count}
                model_list.append(model_info)
            mylog.info('success select model list')
        except Exception as e:
            mylog.error('fail to select model list : %s' % str(e))
        return model_list

    def admin_upload_model(self,model_name,model_version_name,model_size,model_logo=None,model_desc=None):
        #先加入model表，然后加入model detail表，
        result = False
        try:
            upload_model_sql = 'select model_id,model_name from model where model_name=%s'
            self.cur.execute(upload_model_sql,[model_name])
            models = self.cur.fetchall()
            if len(models) == 0:
                insert_model_sql = 'insert model(model_name,newest_version_name,' \
                                   'model_logo,model_desc) values(%s,%s,%s,%s)'
                self.cur.execute(insert_model_sql,[model_name,model_version_name,model_logo,model_desc])
                select_model_sql = 'select model_id from model where model_name=%s'
                self.cur.execute(select_model_sql,[model_name])
                model_id = self.cur.fetchall()[0][0]
                insert_model_detail_sql = 'insert model_detail(model_id,model_name,model_version_name,model_size)' \
                                          ' values(%s,%s,%s,%s)'
                self.cur.execute(insert_model_detail_sql,[model_id,model_name,model_version_name,model_size])
                self.conn.commit()
                result = True
                mylog.info('model %s success uploaded'%model_name)
            else:
                mylog.warning('model %s already uploaded ,please change to update api'%model_name)
        except Exception as e:
            mylog.error('model %s fail to upload : %s'%(model_name,str(e)))
        return result

    def admin_update_model(self,model_name,model_version_name,model_size):
        result = False
        try:
            update_model_sql = 'select model_id,model_name from model where model_name=%s'
            self.cur.execute(update_model_sql,[model_name])
            models = self.cur.fetchall()
            if len(models) == 0:
                mylog.warning('model %s not uploaded ,please change to upload api' % model_name)
            else:
                update_model_sql = 'select model_id,model_name from model where model_name=%s and model_version_name=%s'
                results = self.cur.execute(update_model_sql, [model_name,model_version_name])
                if results > 0:
                    mylog.warning('model version  %s : %s exists '%(model_name,model_version_name))
                else:
                    model_id = models[0][0]
                    update_model_sql = 'update model set newest_version_name=%s where model_name=%s'
                    self.cur.execute(update_model_sql,[model_version_name,model_name])
                    insert_model_detail_sql = 'insert model_detail(model_id,model_name,model_version_name,model_size)' \
                                              ' values(%s,%s,%s,%s)'
                    self.cur.execute(insert_model_detail_sql, [model_id, model_name, model_version_name, model_size])
                    self.conn.commit()
                    mylog.info('success to update model %s to %s'%(model_name,model_version_name))
                    result = True
        except Exception as e:
            mylog.error('fail to update model %s'%str(e))
        return result

    def user_select_file_by_model(self,user_name,role_type,file_name_key,upload_time_start,upload_time_end,model_id,page_size,page_index):
        upload_files_package = None
        try:
            start = page_size * (page_index - 1)
            select_file_sql_head = ' select upload_file_id,upload_file_name,upload_file_size,' \
                                   'create_time,status,visable,uploader,count from uplaod_file where model_id=%s '
            select_file_sql_tail = 'limit %s,%s'
            values = [model_id]
            if not file_name_key=='':
                select_file_sql_head +=' and upload_file_name like %s '
                values.append('%'+file_name_key+'%')
            if not upload_time_start=='':
                select_file_sql_head +=' and create_time>%s '
                values.append(upload_time_start)
            if not file_name_key=='':
                select_file_sql_head +=' and create_time<%s '
                values.append(next_day_str(upload_time_end))
            #管理员可以带其他人的用户名，普通用户只能且必须带自己的用户名，这一点在http服务中进行限制
            if not user_name == '':
                select_file_sql_head +=' and uploader=%s '
                values.append(user_name)
            select_file_sql_head +=select_file_sql_tail
            values.append(start)
            values.append(page_size)
            mylog.info('total select file sql is %s' % select_file_sql_head)
            mylog.info('total select file sql values is %s' % str(values))
            self.cur.execute(select_file_sql_head,values)
            upload_files = self.cur.fetchall()
            upload_file_list = []
            for upload_file in upload_files:
                if role_type == 'user' and upload_file[5]=='invisable':
                    continue
                upload_time = upload_file[3]
                upload_time = upload_time.strftime('%Y-%m-%d %H:%M:%S')
                file_info = {'fileId':upload_file[0],' fileName':upload_file[1],'fileSize':upload_file[2],
                             'uploadTime':upload_time,'status':upload_file[4],'uploader':upload_file[6],'fileCount':upload_file[7]}
                upload_file_list.append(file_info)
            upload_files_package = {'totalCOunt':len(upload_file_list),'fileInfo':upload_file_list}
            mylog.info('success select files')
        except Exception as e:
            mylog.error('error select upload file : %s '%str(e))
        return upload_files_package

    def user_check_space(self,user_name,ori_file_name,file_size):
        check = False
        try:
            select_user_space_sql = 'select used_space,total_space from user where user_name=%s'
            self.cur.execute(select_user_space_sql,[user_name])
            user_space = self.cur.fetchall()[0]
            if file_size+user_space[0] < user_space[1]:
                check = True
                mylog.info('space is enough for user %s to upload %s'%(user_name,ori_file_name))
            else:
                check = False
                mylog.warning('space is not enough for user %s to upload %s' % (user_name, ori_file_name))
        except Exception as e:
            mylog.error('error when check space for user %s : %s'%(user_name,str(e)))
        return check


    def user_insert_file(self,user_name,model_detail_id,ori_file_name,file_name,file_size):
        #文件上传(后)header里有大小信息，也可以自己读文件拿，文件名命名为用户名/MD5+初始后缀的形式
        #调用此方法前，文件应该已经由客户端上传到验证服务器,默认存储位置在files文件夹下用户名文件夹下 'files/user_name/*****.zip/jgp',zip包不解压，并按上述规则改名
        #此方法流程：1 检验md5是否在数据库中（限定用户+md5），在则直接结束流程
              #     2 不在，则向数据库中写入相关信息，然后传入七牛云（没有加密流程，所以覆盖无所谓）
             # 涉及到的表 写入upload_file 更新model model detail两张表的upload file count
        pass

    def user_run(self,user_name,file_id,model_version_id):
        pass



def test_create_users():


    dbm = ModelVerifyMySQLHelper('nnn')
    dbm.createDb()
    passwd = 'password'
    passwd = str_sha256(passwd)
    passwd = str_sha256(passwd)
    for i in range(20):
        name = '老王%04d'%(i+1)
        dbm.admin_create_user(name=name,password=passwd,role_type='user')
    name = '老王'
    dbm.admin_create_user(name,passwd,role_type='admin')
    del dbm

def test_user_count():
    print save_path
    mvmh = ModelVerifyMySQLHelper()
    test_sql = 'select count(*) from user where user_id>10'
    test_sql2 = 'select max(user_id) from user where user_id<10'
    test_sql3 = 'select * from user'
    test_sql4 = 'select * from user where user_id>40'
    result = mvmh.cur.execute(test_sql)
    print result
    print type(result)
    result = mvmh.cur.fetchall()
    print result
    print type(result)
    result2 = mvmh.cur.execute(test_sql2)
    print result2
    print type(result2)
    result2 = mvmh.cur.fetchall()[0][0]
    print result2
    print type(result2)
    result2 = mvmh.cur.execute(test_sql3)
    print result2
    print type(result2)
    result2 = mvmh.cur.execute(test_sql4)
    print result2
    print type(result2)
    print result2==0
    del mvmh

def test_insert():
    dbm = ModelVerifyMySQLHelper()
    passwd = 'password'
    passwd = str_sha256(passwd)
    passwd = str_sha256(passwd)
    name = '老王54353'
    name ='aaa'
    create_user_sql = 'insert user(user_name,password,role_type,total_space,' \
                      'last_login,status,used_space,password_status,favorite_model_id) ' \
                      'values(%s,%s,"admin",500,now(),"inuse",0,"new",%s)'
    values = [name,passwd,None]
    dbm.cur.execute(create_user_sql, values)
    result = dbm.cur.fetchall()
    dbm.conn.commit()
    del dbm
    print result


if __name__ == '__main__':

    # dbm = ModelVerifyMySQLHelper()
    # # dbm.createDb()
    # # passwd = 'password'
    # # passwd = str_sha256(passwd)
    # # passwd = str_sha256(passwd)
    # # for i in range(20):
    # #     name = '老王%04d'%(i+1)
    # #     dbm.admin_create_user(name=name,password=passwd,role_type='user')
    # users = dbm.user_list_users(2,5)
    # users2 = dbm.user_select_users('王',2,5)
    # print users
    # print users2
    # print users2[0]['userName']
    #
    # del dbm
    #test_user_count()
    #test_insert()
    passwd = 'password'
    passwd = str_sha256(passwd)
    print passwd
    passwd = str_sha256(passwd)
    print passwd

    # createDb(BASENAME)
    # #print getBucketIdByName('aaa')
    # testInsertBucket()
    # # print listBucket()
    # # insertFile('qiniuKey','encryptKey','bucket')
    # # img = getFileByFileId(1)
    # # print img[3]
    # # print type(img[3])
    # # print img
    # #print getFiles2AnnotateByBucketId(1,'haha',2)
    # # updateAnnotation(1,'haha','type1','dadada')
    # # print listBucket()
    # #clearOwnFileByUser('haha')
    #
    #
    # token = 'eyJuYW1lIjp4aWFvd2FuZywicGFzc3dkIjp3YW5nMnBhc3MsInRpbWUiOjIwMTctMDktMDctMTctNTUtMzN9'
    #print userValidate('xiaowang','wang2pass')
    #print userValidateByToken(token)
    #print getUserInfoByName('xiaowang')