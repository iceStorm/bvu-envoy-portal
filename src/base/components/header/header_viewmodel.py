from datetime import datetime
from typing import List

class NavItemIcon:
    original: str
    alternate: str

    def __init__(self, original: str, alternate: str = ''):
        self.original = original
        self.alternate = alternate


class NavItem:
    href: str
    title: str
    icon: NavItemIcon
    is_active: bool

    def __init__(self, href: str, title: str, icon: NavItemIcon = None, is_active: bool = False):
        self.href = href
        self.title = title
        self.icon = icon
        self.is_active = is_active


class NavBarViewModel:
    today: str
    nav_items = []

    def __init__(self, nav_items: List[NavItem]):
        date_of_week = self.get_day_of_week_name(datetime.today().weekday())
        self.today = date_of_week + ", " + datetime.now().today().strftime('ngày %d tháng %m, năm %Y.')
        self.nav_items = nav_items

    def get_day_of_week_name(self, index: int):
        return f"Thứ {index + 2}" if index < 6 else "Chủ Nhật"

    def set_active_nav_item(self, path: str):
        for item in self.nav_items:
            if item.href == path:
                item.is_active = True
