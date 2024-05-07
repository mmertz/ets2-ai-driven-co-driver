from PyQt5 import QtCore, QtWidgets


class LoadingOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setGeometry(50, 50, 200, 100)  # Adjust these values as needed
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Loading...", self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    @QtCore.pyqtSlot()
    def show_overlay(self):
        self.show()

    @QtCore.pyqtSlot()
    def hide_overlay(self):
        self.hide()
