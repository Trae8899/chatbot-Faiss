import flet as ft
import os
import dotenv 


class set_api(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page=page
        self.openapi = ft.TextField(
            label="OPENAI_API_KEY", password=True, can_reveal_password=True,on_submit=self.env_set,
        )
        self.index = ft.TextField(
            label="FAISS_INDEX_PATH", on_submit=self.env_set,
        )
        self.allbtn=ft.FilledButton("All Submit",on_click=self.all_submit)

        
    def env_set(self,e):
        submitlist=[]
        submitlist.append(self.env_submit(e.control).strip())
        self.snackbar_print(submitlist)

    def all_submit(self,e):
        submitlist=[]
        try:
            submitlist.append(self.env_submit(self.openapi).strip())
        except:
            pass
        try:
            submitlist.append(self.env_submit(self.index).strip())
        except:
            pass
        self.snackbar_print(submitlist)
        
    def snackbar_print(self,submitlist:[]):
        submitlist = [item for item in submitlist if item is not None]
        
        if len(submitlist)==0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Nothing"), open=True))
        else:
            submittext=", ".join(submitlist)
            self.page.show_snack_bar(ft.SnackBar(ft.Text(submittext+" is Set"), open=True))
    
    def env_submit(self,textenv:ft.TextField):
        try:
            if textenv.value:
                self.page.session.set(textenv.label,textenv.value)
                print (textenv.label)
                print (textenv.value)
                return textenv.label
        except:
            return
        
    def build_page(self):
        self.page.controls.clear()
        return ft.Column([ft.Container(
            content=ft.Column(
            [
                ft.Text("OPEN AI API", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.openapi,
                ft.Text("FAISS INDEXPATH", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.index,
                self.allbtn
            ],
        ),
        padding=50
        )])


if __name__ == "__main__":
    def main(page: ft.Page):
        AIchat=set_api(page)
        page.add(AIchat.build_page())
        page.scroll="AUTO"
        page.on_resize=page.update()
        page.update()
    
    ft.app(main)