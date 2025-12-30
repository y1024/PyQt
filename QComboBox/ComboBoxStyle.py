#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2025/12/27
@author: Irony
@site: https://pyqt.site | https://github.com/PyQt5
@email: 892768447@qq.com
@file: ComboBoxStyle.py
@description:
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication, QComboBox, QListView, QVBoxLayout, QWidget
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (
        QApplication,
        QComboBox,
        QListView,
        QVBoxLayout,
        QWidget,
    )

Style = """
QComboBox {
  color: #000;
  border: 1px solid #d9d9d9;
  background-color: #fff;
  padding: 4px 11px;
  border-radius: 6px;
  combobox-popup: 0;
}

QComboBox:disabled {
  color: rgba(0, 0, 0, 0.25);
  border-color: #d9d9d9;
  background-color: #f6f6f6;
}

QComboBox:hover,
QComboBox:focus {
  border-color: #1677ff;
}

QComboBox::drop-down {
  width: 12px;
  padding: 10px;
  border-left: 1px solid #d9d9d9;
}

QComboBox::drop-down:hover {
  border-left-color: #1677ff;
}

QComboBox::down-arrow {
  image: url("Data/icons/arrow_down.svg");
}

QComboBox::down-arrow:on {
  image: url("Data/icons/arrow_up.svg");
}

QComboBox QFrame {
  background-color: transparent;
}

QComboBox QAbstractItemView {
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  background-color: #fff;
}


QComboBox QListView {
  outline: none;
  font-weight: normal;
}

QComboBox QListView::item {
  color: #000;
  min-height: 32px;
  padding: 0px 4px;
  border: 1px solid transparent;
  border-radius: 4px;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border-left: 3px solid transparent;
  margin: 0px 6px 2px 6px;
}

QComboBox QListView::item:hover {
  background-color: #F0F0F0;
}

QComboBox QListView::item:selected {
  font-weight: 600;
  background-color: #F0F0F0;
  border-left: 3px solid qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.18 rgba(255, 255, 255, 0), stop:0.2 rgba(0, 103, 192, 255), stop:0.8 rgba(0, 103, 192, 255), stop:0.82 rgba(255, 255, 255, 0));
}
"""


def FramelessComboBox(comboBox, minWidth=50):
    comboBox.setView(QListView())
    view = comboBox.view()
    view.setMinimumWidth(comboBox.width() + minWidth)
    if view.parentWidget():
        p = view.parentWidget()
        p.setAttribute(Qt.WA_TranslucentBackground)
        p.setWindowFlags(
            p.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )


class ComboBoxStyle(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.comboBox1 = QComboBox(self)
        self.comboBox2 = QComboBox(self)
        layout.addWidget(self.comboBox1)
        layout.addWidget(self.comboBox2)

        items = ["Item " + str(i) for i in range(10)]
        self.comboBox1.addItems(items)
        self.comboBox2.addItems(items)

        FramelessComboBox(self.comboBox1)
        FramelessComboBox(self.comboBox2)


if __name__ == "__main__":
    import cgitb
    import sys

    cgitb.enable(format="text")

    app = QApplication(sys.argv)
    app.setStyleSheet(Style)

    w = ComboBoxStyle()
    w.show()

    sys.exit(app.exec_())
