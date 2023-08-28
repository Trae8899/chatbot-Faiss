import flet as ft
from AIChat import VectorQAAI
from setting_api import set_api
from FaissUpload import FaissConvert

class Chatlayout(ft.Row):
    def __init__(self, app ,page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app=app
        self.page = page
        self.vertical_alignment=ft.CrossAxisAlignment.START
        self.gpt=VectorQAAI(self.page)
        self.faissConv=FaissConvert(self.page)
        self.setmodule=set_api(self.page)
        self.guestauthpage=ft.Column([ft.Text("GUEST Cannot access this page")])
        self.pipinglitmitpage=ft.Column([ft.Text("Only for Piping Eng.")])
        self._active_view : ft.Control = self.guestauthpage
    
        self.controls = [
            ft.Column([self.active_view])
        ]
    
    @property
    def active_view(self):
        return self._active_view
    
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[0].controls[0] = self._active_view
        self.controls[0].expand=True
        self.update()
    
    def set_chat_view(self):
        self.active_view = self.gpt.build_page()
        self.active_view.update
        self.page.update()
    
    def set_convert_view(self):
        self.active_view = self.faissConv.build_page()
        self.active_view.update
        self.page.update()

    def set_upload_view(self):
        self.active_view = self.convert.build_page()
        self.active_view.update
        self.page.update()

    def set_folder_view(self):
        self.active_view = self.pipinglitmitpage
        self.active_view.update
        self.page.update()

    def set_sett_view(self):
        self.active_view = self.setmodule.build_page()
        self.active_view.update
        self.page.update()