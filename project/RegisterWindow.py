from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from utils.tools import MAIN_WINDOW_SIZE, ImgLineEdit, MyButton, LINK_BUTTON_STYLE, create_fading_dialog
from utils.user import User


class RegisterWindow(QWidget):
    def __init__(self, parent=None, caller=None):
        super().__init__(parent)
        self.caller = caller
        self.init_ui()

    def init_ui(self):

        # 设置子窗口大小以符合主窗口大小
        self.resize(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])

        # 定义组件
        self.accountBar = ImgLineEdit('utils/img/用户.png', '请输入您的账号')
        self.passwordBar = ImgLineEdit('utils/img/密码.png', '请输入您的密码')
        self.confirmPasswordBar = ImgLineEdit('utils/img/密码确认.png', '请再次输入您的密码')

        # 设置两个选项按钮
        reg_btn = MyButton('注册')
        log_btn = MyButton('已有账号？现在登录', LINK_BUTTON_STYLE)
        # 将其点击事件链接到回调方法
        reg_btn.clicked.connect(self.register)
        log_btn.clicked.connect(self.caller.shift_to_login)

        # 组合组件
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.accountBar)
        layout.addWidget(self.passwordBar)
        layout.addWidget(self.confirmPasswordBar)
        layout.addWidget(reg_btn)
        layout.addWidget(log_btn)

    def register(self):
        id = self.accountBar.text()
        password = self.passwordBar.text()
        confirmPassword = self.confirmPasswordBar.text()
        if password != confirmPassword:
            create_fading_dialog('img/白错误.png', '前后输入密码不一致！', True)
        else:
            if User.register(id, password):
                create_fading_dialog('img/白确认.png', '注册成功！')
            else:
                create_fading_dialog('img/白错误.png', '注册失败', True)
