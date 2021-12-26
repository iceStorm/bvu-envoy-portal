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
    user: any
    full_name: str
    nav_items = []

    def __init__(self, user: any, full_name: str, nav_items: [NavItem]):
        self.user = user
        self.full_name = full_name
        self.nav_items = nav_items

    def set_active_nav_item(self, path: str):
        for item in self.nav_items:
            if item.href == path:
                item.is_active = True

