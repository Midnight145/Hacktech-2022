import sys
import traceback

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class LoggerWorker(QObject):
    def __init__(self):
        super(LoggerWorker, self).__init__()
        self.running = True

    def start(self):
        if not self.running:
            self.running = True

        print("Running!")
        # Start Process Keylogger
    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Focus Checker")

        self.btn = QPushButton("Start Keylogger")
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.start_keylogger)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        self.logThread = QThread()
        self.logThread.start()
        self.worker = LoggerWorker()
        self.worker.moveToThread(self.logThread)

        self.setCentralWidget(self.btn)

    def start_keylogger(self, pressed):
        if pressed:
            self.btn.setText("Stop Keylogger")
            self.worker.start()
        else:
            self.btn.setText("Start Keylogger")
            self.worker.stop()
            self.stop_thread()

    def stop_thread(self):
        self.worker.stop()
        self.logThread.quit()
        self.logThread.wait()
        print("Thread Stopped!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec()
