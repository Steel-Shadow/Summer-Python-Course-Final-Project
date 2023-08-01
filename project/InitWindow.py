from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from utils.tools import MAIN_WINDOW_SIZE, create_information, MyButton

BUTTON_SIZE = [MAIN_WINDOW_SIZE[0]-100, 27]

class InitWindow(QWidget):
    def __init__(self, parent=None, caller=None):
        super().__init__(parent)
        self.caller = caller
        self.init_ui()

    def init_ui(self):

        # 设置子窗口大小以符合主窗口大小
        self.resize(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])

        # 定义图标logo
        label = QLabel()# 创建标签
        pixmap = QPixmap("utils/img/名称.png") # 创建一个 QPixmap 对象，加载图片文件
        pixmap = pixmap.scaled(MAIN_WINDOW_SIZE[0]-100, MAIN_WINDOW_SIZE[1]-235)
        label.setPixmap(pixmap) # 在标签中显示图片
        label.setStyleSheet('border-radius:10px;background:#FFFFFF;border:1px;')
        label.setAlignment(Qt.AlignCenter)
        # 设置三个选项按钮
        log_btn = MyButton('登录')
        reg_btn = MyButton('注册')
        abt_btn = MyButton('关于')
        log_btn.setFixedSize(BUTTON_SIZE[0], BUTTON_SIZE[1])
        reg_btn.setFixedSize(BUTTON_SIZE[0], BUTTON_SIZE[1])
        abt_btn.setFixedSize(BUTTON_SIZE[0], BUTTON_SIZE[1])
        # 将其点击事件链接到回调方法
        log_btn.clicked.connect(self.caller.shift_to_login)
        reg_btn.clicked.connect(self.caller.shift_to_register)
        abt_btn.clicked.connect(self.show_about)

        # 将组件加入布局器
        # 定义布局和组件
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignHCenter)
        layout.addWidget(label)
        layout.addWidget(log_btn)
        layout.addWidget(reg_btn)
        layout.addWidget(abt_btn)


    def show_about(self):
        create_information('本平台为2023年暑期Python全英课程大作业，开发人员为刘伟哲（数据库）、王艺杰（知识图谱）、王乐（网络爬虫）、龚家年（GUI界面）。', '关于')
