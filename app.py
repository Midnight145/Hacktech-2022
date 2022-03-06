import traceback

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *

import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQT, NavigationToolbar2QT
from matplotlib.figure import Figure


# Key = 119, Mouse = 12


class LoggerWorker(QObject):
    def __init__(self):
        super(LoggerWorker, self).__init__()
        self.running = True

    def start(self, handler):
        if not self.running:
            self.running = True

        handler.running = True

        print("Running!")
        # Start Process Keylogger


    def stop(self, handler):
        self.running = False

        handler.running = False


class Graph(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Graph, self).__init__(parent, **kwargs)

        self._data = [
            [1, 2, 3, 4, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1, 2, 3, 4, 5]
        ]
        self._currentDataIdx = 0

        self._barSet = QBarSet("Bar Set")
        self._barSet.setColor(QColor(0, 230, 0))
        self._barSet.append(self._data[self._currentDataIdx])

        self._barSeries = QBarSeries()
        self._barSeries.setBarWidth(1)
        self._barSeries.append(self._barSet)

        self._chart = QChart()
        self._chart.addSeries(self._barSeries)
        self._chart.createDefaultAxes()
        self._chart.legend().hide()
        self._chart.axisX(self._barSeries).setVisible(False)
        self._chart.axisY(self._barSeries).setVisible(False)

        # Set the Y-axis range/limits 0 to 6
        self._chart.axisY(self._barSeries).setRange(0, 6)

        self._chartView = QChartView(self._chart)

        #self.setCentralWidget(self._chartView)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Bar Graph"))
        self.layout.addWidget(self._chartView)
        self.setLayout(self.layout)

        self._timerId = self.startTimer(1000)

    def timerEvent(self, event: QTimerEvent):
        if self._timerId != event.timerId():
            return

        # Replace the data in the existing series
        self._currentDataIdx = 1 if not self._currentDataIdx else 0
        for i, n in enumerate(self._data[self._currentDataIdx]):
            self._barSet.replace(i, n)


class MainWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)

        self.setWindowTitle("Focus Checker")

        self.btn = QPushButton("Start Keylogger")
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.start_keylogger)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        self.toolbar = QToolBar("Tools")
        self.addToolBar(self.toolbar)

        self.tool_btn = QPushButton("Show Table")
        self.tool_btn.clicked.connect(self.show_table)
        self.toolbar.addWidget(self.tool_btn)

        self.logThread = QThread()
        self.logThread.start()
        self.worker = LoggerWorker()
        self.worker.moveToThread(self.logThread)

        self.setCentralWidget(self.btn)

    def show_table(self):
        self.table = Graph()
        self.table.show()

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
    import sys
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())
