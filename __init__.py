from binaryninja import core_ui_enabled

from PySide6.QtCore import Qt

from . import docking
from .widget import HexToolsDockWidget

if core_ui_enabled():
    docking.register_widget(
        HexToolsDockWidget, "Hex Tools", Qt.RightDockWidgetArea, Qt.Vertical, False
    )
