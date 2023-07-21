import pymysql


class User:
    # 打开数据库连接
    db = pymysql.connect(host='10.192.226.127',
                         user='root',
                         password='123456')
    # 创建游标对象
    cursor = db.cursor()
    # 创建游标对象
    init_cmds = [
        '''create database if not exists user_management''',
        '''use user_management''',
        '''create table if not exists users(
            id       INT AUTO_INCREMENT PRIMARY KEY,
            account  VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL)''',
        '''create table if not exists user_node_relationship(
            relationship_id	INT AUTO_INCREMENT PRIMARY KEY,
            user_id	INT,
            node_name varchar(255) NOT NULL)'''
    ]
    # 执行初始化
    for i in init_cmds:
        cursor.execute(i)

    def __init__(self, user_id: int, account: str):
        self.id = user_id
        self.account = account

    @classmethod
    def register(cls, account: str, password: str) -> int:
        """注册账号,-1表示账号已注册"""
        query_exist_account = "SELECT * FROM users WHERE account = %s"
        User.cursor.execute(query_exist_account, account)

        if User.cursor.fetchall():
            # 已存在账号，注册失败
            return -1

        add_account = 'INSERT INTO users (account, password) VALUES(%s, %s)'
        User.cursor.execute(add_account, (account, password))
        User.db.commit()
        # 账号注册成功
        return 0

    @classmethod
    def login(cls, account: str, password: str):
        """登录成功返回 0 ，否则 -1 """
        query = "SELECT * FROM users WHERE account = %s AND password = %s"
        params = (account, password)
        User.cursor.execute(query, params)

        result = User.cursor.fetchall()
        if result:
            # 登录成功
            return User(result[0][0], account)
        else:
            # 账户不存在或密码错误'
            return None

    @classmethod
    def close(cls):
        """关闭数据库"""
        User.db.close()
        User.cursor.close()

    @classmethod
    def reset_all(cls):
        """清除所有用户信息"""
        User.cursor.execute('delete from users')
        User.cursor.execute('ALTER TABLE users AUTO_INCREMENT = 0')
        User.db.commit()

    def has_node(self, node_name: str) -> int:
        """检查该用户是否有某个知识图谱节点，有节点返回 0 ，否则 -1"""
        query = f"SELECT * FROM user_node_relationship WHERE user_id = {self.id} AND node_name = {node_name}"
        User.cursor.execute(query)
        result = User.cursor.fetchall()

        if result:  # 有节点
            return 0
        else:  # 无节点
            return -1

    @staticmethod
    def add_node(account: str, password: str) -> int:
        """注册账号,-1表示账号已注册"""
        query_exist_account = "SELECT * FROM users WHERE account = %s"
        User.cursor.execute(query_exist_account, account)

        if User.cursor.fetchall():
            print('已存在账号，注册失败')
            return -1

        add_account = 'INSERT INTO users (account, password) VALUES(%s, %s)'
        User.cursor.execute(add_account, (account, password))
        User.db.commit()
        print('账号注册成功')
        return 0
