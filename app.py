import math
import traceback

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *
import time

import numpy

import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQT, NavigationToolbar2QT
from matplotlib.figure import Figure

import main
from notifier.notifier import notify

handler = main.handler
config = main.config


class Worker(QObject):
    finished = Signal()
    ready = Signal(int)

    @Slot()
    def run(self):
        while True:
            time.sleep(config["check_rate"])
            api_resp = main.run()
            if api_resp == 'distracted':
                notify()
            print("tick")

    def stop(self):
        self.finished.emit()


class Graph(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Graph, self).__init__(parent, **kwargs)

        df = pd.read_csv("key_data.csv")
        df = df.iloc[:, :-2]

        x = list(df)
        y = list(df.iloc[-1])

        print(df)

        y = [0 if pd.isnull(i) else i for i in y]

        print(f'{x}')
        print(f'{y}')


        self._data = [
            #[1, 2, 3, 4, 5, 4, 3, 2, 1],
            #[5, 4, 3, 2, 1, 2, 3, 4, 5]
            y, x
        ]
        self._currentDataIdx = 0

        self._barSet = QBarSet("Key Usage per min")
        self._barSet.append(self._data[self._currentDataIdx])

        self._barSeries = QBarSeries()
        self._barSeries.setBarWidth(1)
        self._barSeries.append(self._barSet)

        self._chart = QChart()
        self._chart.setTheme(QChart.ChartTheme.ChartThemeDark)
        self._chart.addSeries(self._barSeries)

        self._chart.createDefaultAxes()
        self._chart.legend().hide()

        self._chart.axisX(self._barSeries).setVisible(True)
        self._chart.axisY(self._barSeries).setVisible(True)

        # Set the Y-axis range/limits 0 to 20
        self._chart.axisY(self._barSeries).setRange(0, 20)

        self._chartView = QChartView(self._chart)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self._chartView)
        self.setLayout(self.layout)

        self._timerId = self.startTimer(60000)

    def timerEvent(self, event: QTimerEvent):
        if self._timerId != event.timerId():
            return

        # Replace the data in the existing series
        #self._currentDataIdx = 1 if not self._currentDataIdx else 0
        #for i, n in enumerate(self._data[self._currentDataIdx]):
        #    self._barSet.replace(i, n)

        df = pd.read_csv("key_data.csv")
        df = df.iloc[:, :-2]

        y = list(df.iloc[-1])
        y = [0 if pd.isnull(i) else i for i in y]

        self._currentDataIdx = 1
        for i, n in enumerate(y):
            self._barSet.replace(i, n)


class OverallPie(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(OverallPie, self).__init__(parent, **kwargs)

        df = pd.read_csv("key_data.csv")
        df = list(df.iloc[:, -2])

        self.total_focus = 0
        self.total_distracted = 0
        self.total_afk = 0
        self.total = 0

        for i in df:
            if i == "focused":
                self.total_focus += 1
            elif i == "distracted":
                self.total_distracted += 1
            else:
                self.total_afk += 1

        total = self.total_focus + self.total_afk + self.total_distracted

        self.OPieList = [self.total_afk/self.total, self.total_focus/self.total, self.total_distracted/self.total]

        self.series = QPieSeries()

        self.series.append("AFK", self.OPieList[0])
        self.series.append("Focused", self.OPieList[1])
        self.series.append("Distracted", self.OPieList[2])

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Overall Distractiveness")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chartview = QChartView(self.chart)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chartview)
        self.setLayout(self.layout)

        self._timerId = self.startTimer(60000)

    def timerEvent(self, event: QTimerEvent):
        if self._timerId != event.timerId():
            return

        df = pd.read_csv("key_data.csv")
        i = str(list(df.iloc[-1, -2]))

        if i == "focused":
            self.OPieList[1] += 1
        elif i == "distracted":
            self.OPieList[2] += 1
        else:
            self.OPieList[3] += 1

        # Replace the data in the existing series
        # self._currentDataIdx = 1 if not self._currentDataIdx else 0
        # for i, n in enumerate(self._data[self._currentDataIdx]):
        #    self._barSet.replace(i, n)



class MainWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)

        self.setWindowTitle("Focus Checker")

        self.btn = QPushButton("Start Focus Monitor")
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.start_keylogger)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        self.toolbar = QToolBar("Tools")
        self.addToolBar(self.toolbar)

        self.tool_btn = QPushButton("Keypress Bar Graph")
        self.tool_btn.clicked.connect(self.show_table)
        self.toolbar.addWidget(self.tool_btn)

        self.tool_btn2 = QPushButton("Distracted Pie Chart")
        self.tool_btn2.clicked.connect(self.show_pie)
        self.toolbar.addWidget(self.tool_btn2)

        self.setCentralWidget(self.btn)

        self.obj = Worker()
        self.thread = QThread()

        #self.obj.ready.connect(self)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.run)

    def show_pie(self):
        self.opie = OverallPie()
        self.opie.show()

    def show_table(self):
        self.table = Graph()
        self.table.show()

    def start_keylogger(self, pressed):
        if pressed:
            handler.running = True
            self.btn.setText("Stop Focus Monitor")
            self.thread.start()

        else:
            handler.running = False
            self.btn.setText("Start Focus Monitor")
            self.thread.terminate()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())
