import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication

from GraphWindow import *
from LoginWindow import *
from RegisterWindow import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # 设置主窗口大小和位置（几何参数）
        self.center_point = QDesktopWidget().availableGeometry().center()
        self.center_x = self.center_point.x()
        self.center_y = self.center_point.y()
        self.setGeometry(self.center_x - int(MAIN_WINDOW_SIZE[0] / 2),
                         self.center_y - int(MAIN_WINDOW_SIZE[1] / 2),
                         MAIN_WINDOW_SIZE[0],
                         MAIN_WINDOW_SIZE[1])
        # 设置窗口图标
        self.setWindowIcon(QIcon('6.png'))

        self.setWindowTitle(PROGRAM_NAME)

        # 新建所需的窗口
        self.log_win = LoginWindow(self)
        self.reg_win = RegisterWindow(self)
        self.graph_win = GraphWindow(self)

        # 创建堆叠布局器并将可切换的窗口加入
        self.layout = QStackedLayout()
        self.layout.addWidget(self.log_win)
        self.layout.addWidget(self.reg_win)
        self.layout.addWidget(self.graph_win)

    def shift_to_login(self):
        self.layout.setCurrentIndex(0)

    def shift_to_register(self):
        self.layout.setCurrentIndex(1)

    def shift_to_graph(self):
        # 重新设置主窗口几何参数（将其扩大）
        self.setGeometry(self.center_x - int(GRAPH_WINDOW_SIZE[0] / 2),
                         self.center_y - int(GRAPH_WINDOW_SIZE[1] / 2),
                         GRAPH_WINDOW_SIZE[0],
                         GRAPH_WINDOW_SIZE[1])
        self.layout.setCurrentIndex(2)

    def closeEvent(self, event):
        # 释放资源
        User.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
