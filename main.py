import flet as ft
from chat_layout import Chatlayout
from popup_color_item import PopupColorItem

class EngPT(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.user = None
        self.page = page
        self.page.theme_mode = "light"
        self.page.on_route_change = self.route_change
        self.theme_icon_button = ft.IconButton(
            ft.icons.DARK_MODE,
            selected=False,
            selected_icon=ft.icons.LIGHT_MODE,
            icon_size=35,
            tooltip="change theme",
            on_click=self.change_theme,
            style=ft.ButtonStyle(color={"": ft.colors.BLACK, "selected": ft.colors.WHITE}, ),
        )
        self.theme_Color_button = ft.PopupMenuButton(
            icon=ft.icons.COLOR_LENS_OUTLINED,
            tooltip="change Color",
            items=[
                PopupColorItem(color="deeppurple", name="Deep purple"),
                PopupColorItem(color="indigo", name="Indigo"),
                PopupColorItem(color="blue", name="Blue (default)"),
                PopupColorItem(color="teal", name="Teal"),
                PopupColorItem(color="green", name="Green"),
                PopupColorItem(color="yellow", name="Yellow"),
                PopupColorItem(color="orange", name="Orange"),
                PopupColorItem(color="deeporange", name="Deep orange"),
                PopupColorItem(color="pink", name="Pink"),
            ]
        )
        self.layout = Chatlayout(self,self.page)
        self.appbar_items = [
            ft.PopupMenuItem(text="Log-in", on_click=self.login),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(text="Contact", on_click=self.contact),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(text="Settings"),
            ft.PopupMenuItem(),
        ]
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.ENGINEERING_ROUNDED),
            leading_width=100,
            title=ft.Text(f"ENGPT", font_family="Pacifico", size=25),
            center_title=False,
            toolbar_height=70,
            bgcolor=ft.colors.BLUE,
            actions=[
                self.theme_Color_button,
                self.theme_icon_button,
                ft.Container(
                    content=ft.PopupMenuButton(items=self.appbar_items),
                    margin=ft.margin.only(left=50, right=25),
                ),
            ],
        )
        self.page.appbar=self.appbar
        self.tabbar = ft.Tabs(
            on_change=self.layoutchange,
            scrollable=True,
            selected_index=0,
            tabs=[
                ft.Tab(text="GPT"),
                ft.Tab(text="Convert"),
                ft.Tab(text="How 2 Use"),
                ft.Tab(text="Setting"),
            ],
        )
        self.initialize()
    
    def initialize(self):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [
                    self.tabbar,
                    self.layout,
                ],
                appbar=self.appbar,
                scroll=ft.ScrollMode.ALWAYS,
                padding=ft.padding.all(10),
            )
        )
        self.page.update()

    def change_theme(self, e):
        self.page.theme_mode = "light" if self.page.theme_mode == "dark" else "dark"
        self.theme_icon_button.selected = not self.theme_icon_button.selected
        self.page.update()

    def login(self, e):
        def close_dlg(e):
            username = user_id.value.strip()
            password = pass_word.value.strip()
            try:
                if e.control.text=="Cancel":
                    login_dialog.open = False
                    self.page.update()
                    return
            except:
                pass
            if username and password:
                self.page.session.set("user_id",username)
                self.page.session.set("user_password",password)
                self.appbar_items[0] = ft.PopupMenuItem(text=f"{username}'s Profile")
                self.appbar_items.append(ft.PopupMenuItem(
                    text="Logout",
                    on_click=self.logout,
                    )
                )
            login_dialog.open = False
            self.page.update()

        user_id = ft.TextField(label="ID")
        pass_word = ft.TextField(label="Password", password=True, can_reveal_password=True,on_submit=close_dlg)
        login_dialog = ft.AlertDialog(
            title=ft.Text("Please enter your login credentials"),
            content=ft.Column(
                [
                    user_id,
                    pass_word,
                    ft.Row(
                    [ft.ElevatedButton(text="Login", on_click=close_dlg),ft.ElevatedButton(text="Cancel", on_click=close_dlg),]
                    ),
                ],
                tight=True,
            ),
        )
        self.page.dialog = login_dialog
        login_dialog.open = True
        self.page.update()

    def logout(self, e):
        self.page.client_storage.clear()
        self.page.session.clear()
        self.user = None
        self.appbar_items[0] = ft.PopupMenuItem(text="Log-in", on_click=self.login)
        self.appbar_items.pop()
        self.page.update()

    def contact(self, e):
        def close_dlg(e):
            contact_dialog.open = False
            self.page.update()

        contact_dialog = ft.AlertDialog(
            title=ft.Text("Please contact for Error & Manual"),
            content=ft.Column(
                [
                    ft.Text("JAEHYUN PARK"),
                    ft.Text("qkrwogus88@naver.com"),
                    ft.Text("010-3066-3943"),
                    ft.ElevatedButton(text="OK", on_click=close_dlg),
                ],
                tight=True,
            ),
        )

        self.page.dialog = contact_dialog
        contact_dialog.open = True
        self.page.update()

    def layoutchange(self, e):
        if e.control.selected_index == 0:
            self.page.go("/")
        elif e.control.selected_index == 1:
            self.page.go("/convert")
        elif e.control.selected_index == 2:
            self.page.go("/manual")
        elif e.control.selected_index == 3:
            self.page.go("/setting")

    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/gpt")
        elif troute.match("/gpt"):
            self.layout.set_chat_view()
        elif troute.match("/convert"):
            self.layout.set_convert_view()
        elif troute.match("/manual"):
            self.layout.set_folder_view()
        elif troute.match("/setting"):
            self.layout.set_sett_view()
        
        self.layout.update()


def main(page: ft.Page):
    page.title = "EnGPT"
    page.padding = 0
    page.theme = ft.theme.Theme(font_family="Verdana")
    page.theme = ft.theme.Theme(color_scheme_seed="blue")
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}

    app = EngPT(page)
    page.add(app)
    
    page.go("/")
    
    # page.update()


# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)
