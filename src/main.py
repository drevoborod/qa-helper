from PyQt5.QtWidgets import (
    QApplication, QWidget, QFrame, QLineEdit, QComboBox, QLabel, QPushButton,
    QGridLayout, QDesktopWidget, QScrollArea, QVBoxLayout, QStyle, QSizePolicy, QHBoxLayout, QMainWindow
)

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QBrush, QColor, QIcon

from core import Parser


class MainWindow(QWidget):
    def __init__(self, exit_callback):
        super().__init__()
        self.exit_callback = exit_callback
        self.config = Parser()
        self.init_ui()
        self._center()

    def init_ui(self):
        self.setWindowTitle("Universal QA helper")
        requests_frame = RequestsFrame(self, self.config.structure.http_requests)
        main_grid = QGridLayout(self)
        main_grid.addWidget(requests_frame, 0, 0)
        self.setLayout(main_grid)
        self.show()

    def _center(self):
        width = QDesktopWidget().availableGeometry().size().width() // 100 * 75
        height = QDesktopWidget().availableGeometry().size().height() // 100 * 75
        self.setGeometry(0, 0, width, height)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ScrollableFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.scrollable_box = self._prepare_scroll_area()

    def _prepare_scroll_area(self):
        area = QFrame(self)
        #area.setMinimumSize(100, 100)
        scroll_area = QScrollArea()

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(area)

        #self.setGeometry(600, 100, 1000, 900)

        scrollable_box = QVBoxLayout(area)
        area.setLayout(scrollable_box)
        vbox = QVBoxLayout(self)
        vbox.addWidget(area)
        self.setLayout(vbox)

        return scrollable_box


class RequestsFrame(ScrollableFrame):
    """Frame with all HTTP requests."""
    def __init__(self, parent, http_requests):
        super().__init__(parent)
        self.http_requests = http_requests
        self.init_ui()

    def init_ui(self):
        for item in self.http_requests.values():
            self.scrollable_box.addWidget(HTTPRequestFrame(self, item))


class HTTPRequestFrame(QFrame):
    """HTTP request configure area."""
    def __init__(self, parent, http_request_data):
        super().__init__(parent)
        self.http_request_data = http_request_data
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Panel)
        title = QLabel(self.http_request_data.name, self)

        url_title = QLabel("URL:", self)
        url_value = QLineEdit(self)
        url_value.setText(self.http_request_data.url)
        url_value.setReadOnly(True)

        url_frame = QFrame(self)
        url_frame_layout = QGridLayout()
        url_frame_layout.addWidget(url_title, 0, 0)
        url_frame_layout.addWidget(url_value, 0, 1)
        url_frame.setLayout(url_frame_layout)

        send_button = QPushButton("Send", self)

        grid = QGridLayout(self)
        grid.addWidget(title, 0, 0)
        grid.addWidget(send_button, 0, 1, alignment=Qt.AlignRight)
        grid.addWidget(url_frame, 1, 0, 1, 2)
        for number, param in enumerate(self.http_request_data.params.items(), start=2):
            grid.addWidget(ParamRow(self, *param), number, 0, 1, 2)
        self.setLayout(grid)


class ParamRow(QFrame):
    """HTTP request parameter value area."""
    def __init__(self, parent, request_param_name, request_param):
        super().__init__(parent)
        self.request_param_name = request_param_name
        self.request_param = request_param
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Box)
        grid = QGridLayout(self)
        self.setFrameShape(QFrame.NoFrame)

        name = QLabel(self.request_param_name, self)
        name.setFrameShape(QFrame.Box)

        if self.request_param.text:
            area = QLineEdit(self)
            area.setText(self.request_param.text)
        else:
            area = QComboBox(self)
            area.addItems(map(str, self.request_param.choices))

        grid.addWidget(name, 0, 0, alignment=Qt.AlignLeft)
        grid.addWidget(area, 0, 1)
        #if self.request_param.description:
        descr_title = QLabel("Description:", self)
        descr_value = QLineEdit(self)
        descr_value.setText(self.request_param.description)
        descr_value.setDisabled(True)
        grid.addWidget(descr_title, 1, 0, alignment=Qt.AlignLeft)
        grid.addWidget(descr_value, 1, 1)

        self.setLayout(grid)


if __name__ == "__main__":
    app = QApplication([])
    gui = MainWindow(app.exit)
    app.exec()
