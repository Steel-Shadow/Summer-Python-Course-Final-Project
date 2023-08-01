import time

from PyQt5.QtWidgets import *

from GraphWindow import *
from InitWindow import InitWindow
from LoginWindow import *
from RegisterWindow import *


class MainWindow(MyTitleWidget):
    def __init__(self):
        super().__init__()
        self.name = None  # 用户名
        # 设置主窗口大小和位置（几何参数）
        self.setGeometry(CENTER_POINT.x() - int(MAIN_WINDOW_SIZE[0] / 2),
                         CENTER_POINT.y() - int(MAIN_WINDOW_SIZE[1] / 2),
                         MAIN_WINDOW_SIZE[0],
                         MAIN_WINDOW_SIZE[1])
        self.setMaximumSize(self.width(), self.height())

        # 用到的窗口
        self.init_win = InitWindow(caller=self)
        self.log_win = LoginWindow(caller=self)
        self.reg_win = RegisterWindow(caller=self)
        self.graph_win = GraphWindow(caller=self)

        # 创建堆叠布局器并将可切换的窗口加入
        subWidget = QWidget()
        self.s_layout = QStackedLayout(subWidget)
        self.s_layout.addWidget(self.init_win)
        self.s_layout.addWidget(self.log_win)
        self.s_layout.addWidget(self.reg_win)
        self.s_layout.addWidget(self.graph_win)
        self.layout.addWidget(subWidget)

    def shift_to_login(self):
        self.s_layout.setCurrentIndex(1)

    def shift_to_register(self):
        self.s_layout.setCurrentIndex(2)

    def shift_to_graph(self, name):
        # 重新设置主窗口几何参数（将其扩大）
        self.graph_win.init_html(name)
        time.sleep(0.5)
        self.s_layout.setCurrentIndex(3)
        self.set_size_to_graph()

    def set_size_to_graph(self):
        # self.setMaximumSize()
        self.setMaximumSize(GRAPH_WINDOW_SIZE[0], GRAPH_WINDOW_SIZE[1])
        self.setGeometry(CENTER_POINT.x() - int(GRAPH_WINDOW_SIZE[0] / 2),
                         CENTER_POINT.y() - int(GRAPH_WINDOW_SIZE[1] / 2),
                         GRAPH_WINDOW_SIZE[0],
                         GRAPH_WINDOW_SIZE[1])

    def set_size_to_graph_extend(self):
        self.setMaximumSize(GRAPH_WINDOW_EXTEND_SIZE[0], GRAPH_WINDOW_EXTEND_SIZE[1])
        self.setGeometry(CENTER_POINT.x() - int(GRAPH_WINDOW_EXTEND_SIZE[0] / 2),
                         CENTER_POINT.y() - int(GRAPH_WINDOW_EXTEND_SIZE[1] / 2),
                         GRAPH_WINDOW_EXTEND_SIZE[0],
                         GRAPH_WINDOW_EXTEND_SIZE[1])

    def closeEvent(self, event):
        app_path = os.path.abspath(os.path.dirname(__file__))
        if self.name:
            name_nodes_path = os.path.join(app_path, 'templates', self.name + '_nodes.json')
            name_links_path = os.path.join(app_path, 'templates', self.name + '_links.json')
            # print('show!')
            with open('templates/nodes_data.json', encoding='utf-8') as file:
                nodes_code = file.read()
            with open('templates/links_data.json', encoding='utf-8') as file:
                links_code = file.read()
            with open(name_nodes_path, 'w+', encoding='utf-8') as file:
                file.write(nodes_code)
            with open(name_links_path, 'w+', encoding='utf-8') as file:
                file.write(links_code)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建主窗口
    main_win = MainWindow()
    # 设置全局样式
    main_win.setStyleSheet(OVERALL_STYLE)
    # 显示窗口
    main_win.show()
    sys.exit(app.exec_())
