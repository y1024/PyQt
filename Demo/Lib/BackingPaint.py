#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/12/27
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: BackingPaint.py
@description:
"""

import os
import platform
from random import randint
from threading import Event

try:
    from PyQt5.QtCore import QMetaObject, QPoint, QRect, QSize, Qt, QThread
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtGui import QBackingStore, QPainter, QRegion
except ImportError:
    from PySide2.QtCore import QMetaObject, QPoint, QRect, QSize, Qt, QThread, Signal
    from PySide2.QtGui import QBackingStore, QPainter, QRegion


class BackingPaint(QThread):
    resized = Signal(int, int)

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = widget
        self._window = None
        self._backingStore = None
        self._rect = QRect()
        self._size = QSize(100, 100)
        self._oldSize = QSize(100, 100)
        self._resized = Event()
        self._exited = Event()
        self._init()

    def _init(self):
        self._widget.setAttribute(Qt.WA_NativeWindow)
        self._widget.setAttribute(Qt.WA_PaintOnScreen)
        self._widget.setAttribute(Qt.WA_StaticContents)
        self._widget.setAttribute(Qt.WA_OpaquePaintEvent)
        self._widget.setAttribute(Qt.WA_NoSystemBackground)
        self._widget.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self._widget.setUpdatesEnabled(False)
        self._widget.setAutoFillBackground(False)

        self._window = self._widget.windowHandle()
        self._window.create()

    def stop(self):
        self._exited.set()
        self.requestInterruption()

    def resize(self, w, h):
        self._resized.set()
        self._size = QSize(w, h)

    def paintOnGui(self):
        if self._backingStore and not self._exited.is_set():
            self._backingStore.flush(QRegion(self._rect))

    def run(self):
        self.resized.connect(self.resize, Qt.QueuedConnection)
        full = os.getenv("full")
        delay = int(1000 / 60)
        isMac = platform.system() == "Darwin"

        # create backingStore
        self._oldSize = self._widget.size()
        self._backingStore = QBackingStore(self._window)
        self._backingStore.resize(self._oldSize)

        # paint device
        rect = QRect(QPoint(0, 0), self._oldSize)
        self._backingStore.beginPaint(QRegion(rect))
        if not self._backingStore.paintDevice():
            print("paintDevice is None")
            return
        self._backingStore.endPaint()

        while not self._exited.is_set():
            if self._resized.is_set():
                self._oldSize = self._size
                self._backingStore.resize(self._oldSize)
                self._resized.clear()

            rect = QRect(QPoint(0, 0), self._oldSize)
            if full is None:
                rect = QRect(
                    randint(0, max(100, self._oldSize.width() - 100)),
                    randint(0, max(100, self._oldSize.height() - 100)),
                    randint(100, max(200, self._oldSize.width())),
                    randint(100, max(200, self._oldSize.height())),
                )

            # paint
            self._backingStore.beginPaint(QRegion(rect))
            device = self._backingStore.paintDevice()
            if device:
                painter = QPainter()
                painter.begin(device)
                painter.fillRect(rect, Qt.GlobalColor(randint(4, 19)))
                painter.end()
                self._backingStore.endPaint()
                if isMac:
                    self._rect = rect
                    QMetaObject.invokeMethod(
                        self._widget,
                        "paintOnGui",
                        Qt.QueuedConnection,
                    )
                else:
                    self._backingStore.flush(QRegion(rect))

            self.msleep(delay)

        print("paint thread end")
