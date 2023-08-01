import ast

from PyQt5.QtCore import QUrl, QProcess
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QComboBox, QTextBrowser

from utils.sorter import sort_by_search_key, sort_by_name, sort_by_college, sort_by_platform
from utils.tools import *

GRAPH_WINDOW_MAIN_SIZE = [1200, 900]
GRAPH_WINDOW_SIDE_SIZE = [500, 900]
BOX_ICON_SIZE = [20, 20]
COMBOBOX_SIZE = [120, 27]


class SearchBox(QWidget):
    def __init__(self, parent=None, caller=None):
        super().__init__(parent)
        self.caller = caller

        self.comboBox = self.init_comboBox()
        self.comboBox.setFixedSize(COMBOBOX_SIZE[0], COMBOBOX_SIZE[1])
        self.imgComboBox = ImgComboBox('utils/img/排序.png', self.comboBox, width=190, icon_width=27, icon_height=27)
        self.imgLineEdit = ImgLineEdit('utils/img/关键词.png', '自定义搜索关键词', width=210, icon_width=19,
                                       icon_height=19)
        self.imgLineEdit.line_edit.returnPressed.connect(lambda: caller.searchActivated(self.imgLineEdit.text()))

        # 创建布局并添加控件
        layout = QHBoxLayout(self)
        layout.addWidget(self.imgComboBox)
        layout.addWidget(self.imgLineEdit)

    def init_comboBox(self):
        comboBox = QComboBox()
        comboBox.addItem('排序关键词')
        comboBox.addItem('课程名称')
        comboBox.addItem('学校名称')
        comboBox.addItem('平台名称')
        comboBox.model().item(0).setEnabled(False)
        comboBox.activated[str].connect(self.caller.sortActivated)
        return comboBox


class SideBar(QWidget):
    def __init__(self, parent=None, caller=None):
        super().__init__(parent)
        self.list = []
        self.caller = caller
        self.setStyleSheet('border:1px solid black')
        self.setFixedSize(GRAPH_WINDOW_SIDE_SIZE[0], GRAPH_WINDOW_SIDE_SIZE[1])
        self.init_ui()

    def init_ui(self):
        self.textBrowser = QTextBrowser()
        # 设置打开链接时在外部浏览器中打开
        self.textBrowser.setOpenExternalLinks(True)
        # 设置链接在QTextBrowser中打开
        self.textBrowser.setOpenLinks(True)
        # 将光标移到文本末尾
        self.textBrowser.moveCursor(QTextCursor.End)
        min_btn = MyButton()
        min_btn.setIcon(QIcon('utils/img/侧栏隐藏.png'))
        min_btn.clicked.connect(self.caller.hideSideBar)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(SearchBox(caller=self))
        btn_layout.addWidget(min_btn)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(self.textBrowser)

    def sortActivated(self, str):
        if str == '课程名称':
            list = sort_by_name(self.list)
        elif str == '学校名称':
            list = sort_by_college(self.list)
        else:
            list = sort_by_platform(self.list)
        self.showInfo(list)

    def searchActivated(self, str):
        list = sort_by_search_key(self.list, str)
        self.showInfo(list)

    def showInfo(self, list):
        str = ''
        for elem in list:
            str += '<a href="'
            str += elem[2]
            str += '">'
            str += elem[1]
            str += '</a><br>'
            if elem[2]:
                str += '平台：'
                str += elem[0]
                str += '<br>'
            if elem[3]:
                str += '学校：'
                str += elem[3]
                str += '<br>'
            str += '<br>'
        self.textBrowser.setText(str)


class MainGraph(QWidget):
    def __init__(self, parent=None, caller=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.caller = caller
        # 获取app.py所在目录的绝对路径
        self.app_path = os.path.abspath(os.path.dirname(__file__))

        # 创建QWebEngineView来加载Flask应用程序的URL
        self.webview = QWebEngineView()
        layout = QVBoxLayout(self)
        layout.addWidget(self.webview)

    def handle_stdout(self):
        if self.flask_process is not None:
            data = self.flask_process.readAllStandardOutput()
            stdout = bytes(data).decode("utf8", 'ignore')  # 字符串格式的标准输出
            print('subprocess stdout:' + stdout)
            if stdout[0] == '[':
                list = ast.literal_eval(stdout)
                self.caller.showSideBar(list)

    def handle_stderr(self):
        if self.flask_process is not None:
            data = self.flask_process.readAllStandardError()
            stderr = bytes(data).decode("utf8", 'ignore')  # 字符串格式的标准输出
            print('subprocess stderr:' + stderr)

    def init_html(self, name):
        # self.substitute_code(name)
        # print('done')
        # 启动Flask应用程序
        args = []
        script_path = os.path.join(self.app_path, "app.py")
        # print(script_path)
        args.append(script_path)
        args.append(name)
        self.flask_process = QProcess()
        self.flask_process.setWorkingDirectory(self.app_path)
        self.flask_process.readyReadStandardOutput.connect(self.handle_stdout)
        self.flask_process.readyReadStandardError.connect(self.handle_stderr)
        self.flask_process.start('python', args)
        print('app.py started successfully!')
        # sleep(0.5)
        self.webview.setUrl(QUrl('http://127.0.0.1:5000'))
        print('url appointed successfully!')

    def substitute_code(self, name):
        name_json_path = os.path.join(self.app_path, 'templates', name + '.json')
        default_json_path = os.path.join(self.app_path, 'templates\origin.json')
        # print(name_json_path)
        # print(default_json_path)
        try:
            with open(name_json_path, encoding='utf-8') as file:
                substitute_code = file.readlines()
                # print(substitute_code)
        except FileNotFoundError:
            print('default')
            with open(default_json_path, encoding='utf-8') as file:
                substitute_code = file.readlines()
                # print(substitute_code)

        substitute_code[0] = '"data": ' + substitute_code[0]
        substitute_code[len(substitute_code) - 1] = '],\n'

        with open('templates/originKG.html', 'r', encoding='utf-8') as file:
            code = file.readlines()
            # print(code)

        with open('templates/originKG.html', 'w', encoding='utf-8') as file:
            break_index = None
            # print(len(code))
            for i in range(118, len(code)):
                # print(i)
                if code[i] == '            ],\n':
                    break_index = i
                    # print(i)
                    break
            del code[117:break_index + 1]
            for line in reversed(substitute_code):
                code.insert(117, '            ' + line)
                # print(code)
            file.writelines(code)

    def closeEvent(self, event):
        self.flask_process.terminate()


class GraphWindow(QWidget):

    def __init__(self, parent=None, caller=None):
        super().__init__(parent)
        self.showSide = False
        self.caller = caller
        self.init_ui()

    def init_ui(self):
        # 设置子窗口大小以符合主窗口大小
        self.resize(GRAPH_WINDOW_SIZE[0], GRAPH_WINDOW_SIZE[1])
        self.setContentsMargins(0, 0, 0, 0)
        #
        self.mainGraph = MainGraph(caller=self)
        self.sideBar = SideBar(caller=self)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.mainGraph)
        self.layout.addWidget(self.sideBar)
        self.sideBar.hide()

    def init_html(self, name):
        self.mainGraph.init_html(name)

    def showSideBar(self, list):
        self.caller.set_size_to_graph_extend()
        self.resize(GRAPH_WINDOW_EXTEND_SIZE[0], GRAPH_WINDOW_EXTEND_SIZE[1])
        # self.layout.addWidget(self.sideBar)
        self.sideBar.list = list
        self.sideBar.showInfo(self.sideBar.list)
        self.sideBar.show()
        self.showSide = True

    def hideSideBar(self):
        if self.showSide:
            self.caller.set_size_to_graph()
            self.sideBar.hide()
            # self.layout.removeWidget(self.sideBar)
            self.resize(GRAPH_WINDOW_SIZE[0], GRAPH_WINDOW_SIZE[1])
            self.showSide = False
