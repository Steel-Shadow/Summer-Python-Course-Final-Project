from PyQt5.QtWidgets import QVBoxLayout, QTabWidget

from Utils import *

class GraphWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 设置子窗口大小以符合主窗口大小
        self.resize(GRAPH_WINDOW_SIZE[0], GRAPH_WINDOW_SIZE[1])

        layout = QVBoxLayout()

        # 创建一个选项卡控件
        tabs = QTabWidget()

        # 创建三个标签页面并将其添加到选项卡控件中/TODO：替换为neo4j的界面/
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        tabs.addTab(tab1, "Tab 1")
        tabs.addTab(tab2, "Tab 2")
        tabs.addTab(tab3, "Tab 3")

        # 在第一个标签页面中添加一个标签
        label1 = QLabel('This is Tab 1')
        tab1.layout = QVBoxLayout()
        tab1.layout.addWidget(label1)
        tab1.setLayout(tab1.layout)

        # 在第二个标签页面中添加一个标签
        label2 = QLabel('This is Tab 2')
        tab2.layout = QVBoxLayout()
        tab2.layout.addWidget(label2)
        tab2.setLayout(tab2.layout)

        # 在第三个标签页面中添加一个标签
        label3 = QLabel('This is Tab 3')
        tab3.layout = QVBoxLayout()
        tab3.layout.addWidget(label3)
        tab3.setLayout(tab3.layout)

        # 将选项卡控件添加到垂直布局中
        layout.addWidget(tabs)

        self.setLayout(layout)

