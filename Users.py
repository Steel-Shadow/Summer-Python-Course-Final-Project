import pymysql


class Users:
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123456',
                         database='user_management')
    # 创建游标对象
    cursor = db.cursor()
    # 创建游标对象
    init_cmds = [
        'create database if not exists user_management',
        'use user_management',
        '''CREATE TABLE if not exists users(
            id       INT AUTO_INCREMENT PRIMARY KEY,
            account  VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL)'''
    ]
    # 执行初始化
    for i in init_cmds:
        cursor.execute(i)

    @staticmethod
    def register(account: str, password: str) -> int:
        """注册账号,-1表示账号已注册"""
        query_exist_account = "SELECT * FROM users WHERE account = %s"
        Users.cursor.execute(query_exist_account, account)

        if Users.cursor.fetchall():
            print('已存在账号，注册失败')
            return -1

        add_account = 'INSERT INTO users (account, password) VALUES(%s, %s)'
        Users.cursor.execute(add_account, (account, password))
        Users.db.commit()
        print('账号注册成功')
        return 0

    @staticmethod
    def login(account: str, password: str) -> int:
        """登录成功返回 0 ，否则 -1 """
        query = "SELECT * FROM users WHERE account = %s AND password = %s"
        params = (account, password)
        Users.cursor.execute(query, params)
        result = Users.cursor.fetchall()

        if result:
            print(account, '登录成功')
            return 0
        else:
            print(account, '账户不存在或密码错误')
            return -1

    @staticmethod
    def close():
        """关闭数据库"""
        Users.db.close()
        Users.cursor.close()

    @staticmethod
    def reset_all():
        """清除所有用户信息"""
        Users.cursor.execute('delete from users')
        Users.cursor.execute('ALTER TABLE users AUTO_INCREMENT = 0')
        Users.db.commit()
