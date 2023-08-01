import re
import sys
import os
from time import sleep

from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QMessageBox, QFrame, QGroupBox, QPushButton, \
    QVBoxLayout, QDialog, QApplication, QDesktopWidget

PROGRAM_NAME = '课程资源推荐平台'

# 先创建一个QApplication，以获得屏幕的尺寸信息
app = QApplication(sys.argv)
SCREEN_GEOMETRY = QDesktopWidget().availableGeometry()
CENTER_POINT = QDesktopWidget().availableGeometry().center()  # 获取中心点位置（注意可能因为不同尺寸屏幕而不同，因此不能设为常量，需即时获取）
FADING_DIALOG_POINT = QPoint(CENTER_POINT.x() - 120, CENTER_POINT.y() - 50)


# 一些常量的设置
MAIN_WINDOW_SIZE = [400, 300]
GRAPH_WINDOW_SIZE = [1200, 900]
GRAPH_WINDOW_EXTEND_SIZE = [1700, 900]
BAR_SIZE = [250, 50]
BAR_ICON_SIZE = [24, 24]
BAR_TEXT_HEIGHT = 25
TITLE_FIXED_WIDTH = 23

# C:\Users\KARL\Desktop\git clone\Summer-Python-Course-Final-Project\gui\utils\styles\overall_style.qss
# if (os.getcwd())
# app_path = os.path.abspath(os.path.dirname(__file__))

# 读取配置文件到内存中
with open('utils/styles/overall_style.qss', encoding='utf-8') as style:
    OVERALL_STYLE = style.read()
with open('utils/styles/link_btn_style.qss', encoding='utf-8') as style:
    LINK_BUTTON_STYLE = style.read()
with open('utils/styles/fading_dialog_style_green.qss', encoding='utf-8') as style:
    FADING_DIALOG_GREEN_STYLE = style.read()
with open('utils/styles/fading_dialog_style_red.qss', encoding='utf-8') as style:
    FADING_DIALOG_RED_STYLE = style.read()
with open('utils/styles/img_line_edit.qss', encoding='utf-8') as style:
    IMG_LINE_EDIT_STYLE = style.read()
with open('templates/originKG.html', encoding='utf-8') as html:
    HTML_CODE = html.read()


# 自定义的文本标签和输入框组合的widget
class TextLineEdit(QWidget):
    def __init__(self, label_text="", placeholder_text=""):
        super().__init__()

        # 创建标签和文本框控件
        self.label = QLabel(label_text)
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder_text)

        # 创建布局并添加控件
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)

        # 创建QFrame控件并设置边框样式
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Sunken)
        layout.addWidget(self.frame)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        return self.line_edit.setText(text)


# 自定义的图片标签和输入框组合的widget
class ImgLineEdit(QGroupBox):
    def __init__(self, img_url="", placeholder_text="", width=BAR_SIZE[0], height=BAR_SIZE[1], icon_width=BAR_ICON_SIZE[0], icon_height=BAR_ICON_SIZE[1]):
        super().__init__()
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.setFixedSize(width, height)

        # 创建标签和文本框控件
        self.label = QLabel()
        pixmap = QPixmap(img_url)
        pixmap = pixmap.scaled(self.icon_width, self.icon_height)
        self.label.setPixmap(pixmap)
        self.line_edit = QLineEdit()
        self.line_edit.setFixedHeight(BAR_TEXT_HEIGHT)
        self.line_edit.setPlaceholderText(placeholder_text)

        # 创建布局并添加控件
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.setAlignment(Qt.AlignCenter)

        self.setContentsMargins(0, 0 ,0 ,0)
        self.setStyleSheet(IMG_LINE_EDIT_STYLE)

    def text(self):
        return self.line_edit.text()


class ImgComboBox(QGroupBox):
    def __init__(self, img_url="", comboBox=None, width=BAR_SIZE[0], height=BAR_SIZE[1], icon_width=BAR_ICON_SIZE[0], icon_height=BAR_ICON_SIZE[1]):
        super().__init__()
        self.icon_width = icon_width
        self.icon_height = icon_height
        self.setFixedSize(width, height)

        # 创建标签和文本框控件
        self.label = QLabel()
        pixmap = QPixmap(img_url)
        pixmap = pixmap.scaled(self.icon_width, self.icon_height)
        self.label.setPixmap(pixmap)

        # 创建布局并添加控件
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(comboBox)
        layout.setAlignment(Qt.AlignCenter)

        self.setContentsMargins(0, 0 ,0 ,0)
        self.setStyleSheet(IMG_LINE_EDIT_STYLE)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        return self.line_edit.setText(text)

# 自定义的停留时能将指针变成手指的按钮
class MyButton(QPushButton):
    def __init__(self, word='', style=''):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setText(word)
        self.setStyleSheet(style)


# 自定义的标题行，抛弃原有的丑陋ui
class MyTitleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isDragging = False

        self.subFrame = QFrame()
        # self.subFrame.setStyleSheet('background:#AEEEEE')
        min_btn = MyButton()
        min_btn.setIcon(QIcon('utils/img/最小化.png'))
        min_btn.clicked.connect(self.showMinimized)
        close_btn = MyButton()
        close_btn.setIcon(QIcon('utils/img/关闭.png'))
        close_btn.clicked.connect(self.close)
        titleLabel = QLabel('课程资源推荐平台')
        titleLabel.setStyleSheet('background:#CAE1FF')

        imgLabel = QLabel()
        pixmap = QPixmap('utils/img/平台.png')
        pixmap = pixmap.scaled(28, 23)
        imgLabel.setPixmap(pixmap)
        imgLabel.setStyleSheet('background:#CAE1FF')

        h_layout = QHBoxLayout(self.subFrame)
        h_layout.addWidget(imgLabel)
        h_layout.addWidget(titleLabel)
        h_layout.addStretch()
        h_layout.addWidget(min_btn)
        h_layout.addWidget(close_btn)
        h_layout.setContentsMargins(5, 5, 5, 0)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.subFrame)
        # self.subFrame.raise_()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.subFrame.rect().contains(event.pos()):  # 判断是否在标题栏内
            self.isDragging = True
            self.dragPosition = event.globalPos() - self.pos()  # 计算鼠标位置与窗口位置之间的偏移量

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isDragging:
            self.move(event.globalPos() - self.dragPosition)  # 移动窗口到当前鼠标位置

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.isDragging = False


class FadingDialog(QDialog):

    def __init__(self, img_url, text, isRed=False):
        super().__init__()
        self.IMG_SIZE = [30, 30]
        self.img_url = img_url
        self.text = text
        self.isRed = isRed
        self.ini_ui()

    def ini_ui(self):
        self.setModal(False)
        # self.setWindowModality(Qt.NonModal) # 非阻塞性的窗口
        self.setWindowOpacity(0.75)  # 设置窗口透明度
        if self.isRed:
            self.setStyleSheet(FADING_DIALOG_RED_STYLE)
        else:
            self.setStyleSheet(FADING_DIALOG_GREEN_STYLE)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        img_label = QLabel()
        img_label.setPixmap(QPixmap(self.img_url).scaled(30, 30))
        msg_label = QLabel(self.text)
        close_btn = MyButton()
        close_btn.setIcon(QIcon('utils/img/白关闭.png'))
        close_btn.clicked.connect(self.close)

        main_layout = QHBoxLayout(self)
        main_layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        main_layout.addWidget(img_label)
        main_layout.addWidget(msg_label)
        main_layout.addWidget(close_btn)

        self.fade_timer = QTimer()
        self.fade_timer.setInterval(500)
        self.fade_timer.start()
        self.fade_timer.timeout.connect(self.faded_out)

    def faded_out(self):
        for i in range(75, 0, -1):
            opacity = i / 100
            self.setWindowOpacity(opacity)  # 设置窗口透明度
            self.update()
            QApplication.processEvents()  # 确保能够响应关闭事件
            sleep(0.01)
        self.fade_timer.stop()
        self.close()


# 创建自动消失的对话框
def create_fading_dialog(img_url, text, isRed=False):
    msg = FadingDialog(img_url, text, isRed)
    msg.move(FADING_DIALOG_POINT)
    msg.exec_()


# 创建一个通知信号框
def create_information(text, title='提示'):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.exec_()


# 创建一个警告对话框
def create_warning(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle('警告')
    msg.setText(text)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.exec_()


# 创建一个确认对话框
def create_confirm(text):
    msg = QMessageBox()
    pixmap = QPixmap('utils/img/确认.png')
    pixmap = pixmap.scaled(BAR_ICON_SIZE[0], BAR_ICON_SIZE[1])
    msg.setText(text)
    msg.setIconPixmap(pixmap)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.exec_()

def is_valid_url(url):
    url_regex = re.compile(
        r'^(http|https)://'  # 协议
        r'(([a-zA-Z0-9_!~*\'().&=+$%-]+:)?([a-zA-Z0-9_!~*\'().&=+$%-]+)@)?'  # 认证信息
        r'(([0-9]{1,3}\.){3}[0-9]{1,3}|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'  # IP地址或域名
        r'(:[0-9]{1,5})?'  # 端口号
        r'(/([a-zA-Z0-9_!~*\'().;?:@&=+$,%#-]+)*)*'  # 路径
        r'(\?[a-zA-Z0-9_!~*\'().;?:@&=+$,%#-]+)?'  # 查询参数
        r'(#[a-zA-Z0-9_!~*\'().;?:@&=+$,%#-]+)?$'  # 锚点
    )
    return url_regex.match(url) is not None