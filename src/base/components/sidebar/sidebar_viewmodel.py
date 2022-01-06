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
    counter: int
    show_counter_icon: bool

    def __init__(self, href: str, title: str, counter=0, show_counter_icon=False, icon: NavItemIcon = None, is_active: bool = False):
        self.href = href
        self.title = title
        self.icon = icon
        self.is_active = is_active
        self.counter = counter
        self.show_counter_icon = show_counter_icon if counter == 0 else True


class NavItemGroup:
    label: str
    items: List[NavItem]

    def __init__(self, label: str, items: List[NavItem]):
        self.items = items
        self.label = label


class NavBarViewModel:
    today: str
    nav_item_groups = []

    def __init__(self, nav_item_groups: List[NavItemGroup]):
        date_of_week = self.get_day_of_week_name(datetime.today().weekday())
        self.today = date_of_week + ", " + datetime.now().today().strftime('ngày %d tháng %m, năm %Y.')
        self.nav_item_groups = nav_item_groups

    def get_day_of_week_name(self, index: int):
        return f"Thứ {index + 2}" if index < 6 else "Chủ Nhật"

    def set_active_nav_item(self, path: str):
        for group in self.nav_item_groups:
            for item in group.items:
                if item.href == path:
                    item.is_active = True
