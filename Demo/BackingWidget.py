#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/12/27
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: BackingWidget.py
@description:
"""

try:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtWidgets import QApplication, QWidget
except ImportError:
    from PySide2.QtCore import Slot
    from PySide2.QtWidgets import QApplication, QWidget

from Lib.BackingPaint import BackingPaint


class BackingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._showed = False
        self._thread = BackingPaint(self)
        self.resize(800, 600)

    def closeEvent(self, event):
        if self._thread:
            self._thread.stop()
            self._thread.quit()
            self._thread.wait(100)
            del self._thread
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._showed:
            self._showed = True
            self._thread.start()
            self._thread.resized.emit(self.width(), self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._showed and self._thread and self._thread.isRunning():
            self._thread.resized.emit(self.width(), self.height())

    def paintEngine(self):
        return None

    @Slot()
    def paintOnGui(self):
        if self._thread:
            self._thread.paintOnGui()


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")
    app = QApplication(sys.argv)
    w = BackingWidget()
    w.show()
    sys.exit(app.exec_())
