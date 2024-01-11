# -*- coding:utf-8 -*-
import pymysql
from sshtunnel import SSHTunnelForwarder
from commons.config import PROJECT_PATH


class ConnectDatabase:
    """
    连接数据库
    """
    def __init__(self, user, password, database=None, connect_database_name=None, host=None, port=None):
        if connect_database_name == 'tidb':
            conn = pymysql.connect(
                        host='192.168.8.60',
                        port=4000,
                        user=user,
                        password=password,
                        database=database
            )
        elif connect_database_name == 'tw591':
            server = SSHTunnelForwarder(
                ('192.168.8.36', 22),  # 跳板机的IP和端口
                ssh_pkey=PROJECT_PATH + '/tools/t591MySQLConnect_20201009',  # 公钥
                ssh_username='t591MySQLConnect',  # 跳板机用户名
                ssh_password='addcn123',  # 跳板机密码
                remote_bind_address=('192.168.8.117', 3306),  # 所需要连接数据库的IP和端口
            )
            server.start()
            conn = pymysql.connect(
                host='127.0.0.1',  # 只能写127.0.0.1 不可更改
                port=server.local_bind_port,
                user=user,
                password=password,
                database=database
            )
        elif connect_database_name == 'tw591_prod':
            server = SSHTunnelForwarder(
                ('203.69.66.147', 10100),  # 跳板机的IP和端口
                ssh_pkey=PROJECT_PATH + '/tools/t591MySQLConnect_13306',  # 公钥
                ssh_username='t591MySQLConnect',  # 跳板机用户名
                ssh_password='addcn123',  # 跳板机密码
                remote_bind_address=('192.168.2.203', 3306),  # 所需要连接数据库的IP和端口
            )
            server.start()
            conn = pymysql.connect(
                host='127.0.0.1',  # 只能写127.0.0.1 不可更改
                port=server.local_bind_port,
                user=user,
                password=password,
                database=database
            )
        elif connect_database_name == 'tidb_prod':
            server = SSHTunnelForwarder(
                ('203.69.66.147', 10100),  # 跳板机的IP和端口
                ssh_pkey=PROJECT_PATH + '/tools/t591MySQLConnect_13306',  # 公钥
                ssh_username='t591MySQLConnect',  # 跳板机用户名
                ssh_password='addcn123',  # 跳板机密码
                remote_bind_address=('192.168.2.21', 4000),  # 所需要连接数据库的IP和端口
            )
            server.start()
            conn = pymysql.connect(
                host='127.0.0.1',  # 只能写127.0.0.1 不可更改
                port=server.local_bind_port,
                user=user,
                password=password,
                database=database
            )
        else:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
        self.conn = conn
        self.cursor = conn.cursor()
        self.database = database
        # self.cursor.execute('set names utf8')
        self.cursor.execute('set names latin1')

    def show_databases(self,):
        self.cursor.execute('show databases')
        print('所有的数据库>>>:', self.cursor.fetchall())

    def show_tables(self):
        if self.database is None:
            print('请填入查看数据库表连接的数据库名！')
        else:
            self.cursor.execute('show tables')
            print('查询数据库中所有的表>>>:', self.cursor.fetchall())

    def select_print(self, sql):
        self.cursor.execute(sql)
        for x in self.cursor.fetchall():
            print(x)

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print(self.cursor.rowcount, '插入数据成功！')
        except Exception as err:
            raise err

    def inserts(self, sql, val):
        try:
            self.cursor.executemany(sql, val)
            self.conn.commit()
            print(self.cursor.rowcount, '插入数据成功！')
        except Exception as err:
            raise err

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print('删除数据成功！')
        except Exception as err:
            raise err

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print('更新数据成功！')
        except Exception as err:
            raise err


if __name__ == '__main__':
    pass
    # 1.连接tidb_prod数据库
    # tidb = ConnectDatabase('10952', 'wentao123@', connect_database_name='tidb_prod')
    # tidb2 = ConnectDatabase('10952', 'wentao123@', connect_database_name='tidb')
    # tidb.show_databases()
    # tw591 = ConnectDatabase('10952', 'wentao123@', connect_database_name='tw591_prod')
    # user_info = get_yaml_data('../test_data/database_data.yaml')
    # print(user_info)
    # tw591 = ConnectDatabase(user_info['username'], user_info['password'],  connect_database_name=user_info["connect_database_tw591"])
    # tw591.show_databases()
    # tidb = ConnectDatabase(user_info['username2'], user_info['password2'],  connect_database_name=user_info["connect_database_tidb"])

