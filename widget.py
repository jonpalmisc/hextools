from typing import Optional

from binaryninja import BinaryView
from binaryninjaui import (
    SidebarWidget,
    SidebarWidgetType,
    UIActionHandler,
    getMonospaceFont,
)

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QFont, QImage, QColor
from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from .core import parseFloat, parseInt


instance_id = 0


class HexToolsSidebarWidget(SidebarWidget):

    data: BinaryView
    offset: int
    table: QTableWidget

    def __init__(self, name, frame, data):
        SidebarWidget.__init__(self, name)
        self.data = data
        self.offset = 0

        global instance_id
        instance_id += 1

        self.actionHandler = UIActionHandler()
        self.actionHandler.setupActionHandler(self)

        self.table = QTableWidget()
        self.initTable()
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def initTable(self):
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Data Type", "Value"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setFont(getMonospaceFont(self))
        self.refreshTable()

    def refreshTable(self):
        self.table.clearContents()

        data = self.data.read(self.offset, 8)

        i8 = parseInt(data, 1)
        u8 = parseInt(data, 1, False)
        i16 = parseInt(data, 2)
        u16 = parseInt(data, 2, False)
        i32 = parseInt(data, 4)
        u32 = parseInt(data, 4, False)
        i64 = parseInt(data, 8)
        u64 = parseInt(data, 8, False)
        f32 = parseFloat(data[:4])
        f64 = parseFloat(data)

        content = {
            "int8_t": str(i8),
            "uint8_t": str(u8),
            "int16_t": str(i16),
            "uint16_t": str(u16),
            "int32_t": str(i32),
            "uint32_t": str(u32),
            "int64_t": str(i64),
            "uint16_t": str(u64),
            "float": str(f32),
            "double": str(f64),
        }

        self.table.setRowCount(len(content))

        i = 0
        for k in content:
            label = QTableWidgetItem(k)
            value = QTableWidgetItem(content[k])

            # Prevent editing
            label.setFlags(label.flags() ^ Qt.ItemIsEditable)

            print(f"item: {k}, {content[k]}")

            self.table.setItem(i, 0, label)
            self.table.setItem(i, 1, value)

            i += 1

    def notifyOffsetChanged(self, offset):
        self.offset = offset
        self.refreshTable()


class HexToolsSidebarWidgetType(SidebarWidgetType):
    def __init__(self):
        icon = QImage(56, 56, QImage.Format_RGB32)
        icon.fill(0)

        p = QPainter()
        p.begin(icon)
        p.setFont(QFont("Open Sans", 56))
        p.setPen(QColor(255, 255, 255, 255))
        p.drawText(QRectF(0, 0, 56, 56), Qt.AlignCenter, "X")
        p.end()

        SidebarWidgetType.__init__(self, icon, "HexTools")

    def createWidget(self, frame, data):
        return HexToolsSidebarWidget("HexTools", frame, data)
