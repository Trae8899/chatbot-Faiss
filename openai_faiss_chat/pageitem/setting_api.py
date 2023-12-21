import flet as ft
import os
import dotenv

try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    FAISS_INDEX_PATH = os.environ.get('FAISS_INDEX_PATH')
except:
    pass

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
    
    def startset(self):
        self.openapi.value=self.page.session.get('OPENAI_API_KEY')
        self.index.value=self.page.session.get('FAISS_INDEX_PATH')
        self.page.update()

        
    def env_set(self,e=None):
        submitlist=[]
        submitlist.append(self.env_submit(e.control).strip())
        self.snackbar_print(submitlist)

    def all_submit(self,e=None):
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
        textenv.value=str(textenv.value).strip()
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
        self.page.session.set('OPENAI_API_KEY',OPENAI_API_KEY)
        self.page.session.set('FAISS_INDEX_PATH',FAISS_INDEX_PATH)
        self.startset()
        return ft.Column([ft.Container(
            content=ft.Column(
            [
                ft.Text("OPEN AI API", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.openapi,
                ft.Text("FAISS INDEX PATH", style=ft.TextThemeStyle.DISPLAY_SMALL),
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