from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from Utils import *
from Users import *

class RegisterWindow(QWidget):
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
        self.confirmPasswordBar = LabeledLineEdit('确认密码', '请再次输入您的密码')
        layout.addWidget(self.accountBar)
        layout.addWidget(self.passwordBar)
        layout.addWidget(self.confirmPasswordBar)
        #设置两个选项按钮
        reg_btn = QPushButton('注册')
        log_btn = QPushButton('已有账号？现在登录')
        #将其点击事件链接到回调方法
        reg_btn.clicked.connect(self.register)
        log_btn.clicked.connect(self.parentWidget().shift_to_login)
        #将两个按钮加入布局器
        layout.addWidget(reg_btn)
        layout.addWidget(log_btn)

        # 将定义好的布局器设为该窗口的布局器
        self.setLayout(layout)

    def register(self):
        id = self.accountBar.text()
        password = self.passwordBar.text()
        confirmPassword = self.confirmPasswordBar.text()
        if password != confirmPassword:
            create_warning('前后输入密码不一致！')
        elif register(id, password):
            create_information('注册成功！')
        else:
            create_warning('注册失败！')
