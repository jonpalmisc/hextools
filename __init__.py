from binaryninja import core_ui_enabled
from .widget import HexToolsSidebarWidgetType

if core_ui_enabled():
    from binaryninjaui import Sidebar

    Sidebar.addSidebarWidgetType(HexToolsSidebarWidgetType())
