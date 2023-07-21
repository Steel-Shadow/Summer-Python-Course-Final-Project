from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from src.user.User import *
from Utils import *


class LoginWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):

        # 设置子窗口大小以符合主窗口大小
        self.resize(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])

        # 定义布局和组件
        layout = QVBoxLayout()
        self.accountBar = LabeledLineEdit('账号', '请输入您的账号')
        self.passwordBar = LabeledLineEdit('密码', '请输入您的密码')
        layout.addWidget(self.accountBar)
        layout.addWidget(self.passwordBar)
        # 设置两个选项按钮
        log_btn = QPushButton('登录')
        reg_btn = QPushButton('没有账号？现在注册')
        # 将其点击事件链接到回调方法
        log_btn.clicked.connect(self.login)
        reg_btn.clicked.connect(self.parentWidget().shift_to_register)
        # 将两个按钮加入布局器
        layout.addWidget(log_btn, )
        layout.addWidget(reg_btn)

        # 将定义好的布局器设为该窗口的布局器
        self.setLayout(layout)

    # 当点击登录按钮时，调用此回调方法
    def login(self):
        id = self.accountBar.text()
        password = self.passwordBar.text()
        if User.login(id, password):  # 调用外部的登录接口，判断是否登录成功
            create_information('登录成功！')
            self.parentWidget().shift_to_graph()
        else:
            create_warning('账号或密码错误！')
