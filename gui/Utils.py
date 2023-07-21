from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QMessageBox

PROGRAM_NAME = '课程资源推荐平台'

MAIN_WINDOW_SIZE = [400, 300]
GRAPH_WINDOW_SIZE = [1200, 900]

# 自定义的标签和输入框组合的widget
class LabeledLineEdit(QWidget):
    def __init__(self, label_text="", placeholder_text=""):
        super().__init__()

        # 创建标签和文本框控件
        self.label = QLabel(label_text)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder_text)

        # 创建布局并添加控件
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        return self.line_edit.setText(text)

# 创建一个通知信号框
def create_information(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
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
