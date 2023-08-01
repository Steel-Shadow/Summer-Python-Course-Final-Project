from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from utils.tools import MAIN_WINDOW_SIZE, ImgLineEdit, MyButton, LINK_BUTTON_STYLE, create_fading_dialog
from utils.user import User

BUTTON_SIZE = [MAIN_WINDOW_SIZE[0]-100, 30]

class LoginWindow(QWidget):

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
        #设置两个选项按钮
        log_btn = MyButton('登录')
        reg_btn = MyButton('没有账号？现在注册', LINK_BUTTON_STYLE)
        #将其点击事件链接到回调方法
        log_btn.clicked.connect(self.login)
        reg_btn.clicked.connect(self.caller.shift_to_register)

        #加入布局器
        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.accountBar)
        layout.addStretch()
        layout.addWidget(self.passwordBar)
        layout.addStretch()
        layout.addWidget(log_btn)
        layout.addStretch()
        layout.addWidget(reg_btn)
        layout.addStretch()

        # 将定义好的布局器设为该窗口的布局器
        layout.setAlignment(Qt.AlignHCenter)
        self.setLayout(layout)

    # 当点击登录按钮时，调用此回调方法
    def login(self):
        id = self.accountBar.text()
        password = self.passwordBar.text()
        if User.login(id, password):  # 调用外部的登录接口，判断是否登录成功
            self.caller.shift_to_graph(id)
            self.caller.name = id
            create_fading_dialog('utils/img/白确认.png', '登录成功！', False)
        else:
            create_fading_dialog('utils/img/白错误.png', '账号或密码错误！', True)
