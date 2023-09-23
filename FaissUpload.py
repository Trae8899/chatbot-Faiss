import flet as ft
import os
from module_langchain.embedding_faiss import embedding_folder

class FaissConvert(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.indextpath=None
        self.openapi=None
        self.page=page
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = ft.Text()
        self.picker=ft.ElevatedButton(
            "Pick files",
            icon=ft.icons.ATTACH_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=True,file_type="custom",allowed_extensions= ['pdf','docx'])
            )
        self.jsonfile=ft.FilledButton(
            "Convert",
            icon=ft.icons.CLOUD_UPLOAD_OUTLINED,
            on_click=self.jsons_Upload,
            visible=False
            )
        self.filetext=ft.Text(style=ft.TextThemeStyle.LABEL_MEDIUM)
        self.progress=ft.Column([
            self.filetext,
            ft.ProgressBar(),
            ],
            visible=False
        )
        self.donelist=ft.Text(style=ft.TextThemeStyle.LABEL_MEDIUM)
        self.donetext=ft.Column([
            ft.Text("DONE",style=ft.TextThemeStyle.LABEL_MEDIUM),
            self.donelist,
            ],
            visible=False
        )
        self.files=[]

    def pick_files_result(self,e: ft.FilePickerResultEvent):
        self.jsonfile.visible=False
        self.jsonfile.update()
        self.donetext.visible=False
        self.donetext.update()
        files=[]
        paths=[]
        if e.files:
            for f in e.files:
                files.append(f.name)
                paths.append(f.path)
            self.selected_files.value ="\n ".join(files)
            self.jsonfile.visible=True
            self.jsonfile.update()
        else:
            self.selected_files.value ="Cancelled!"
        self.files=paths
        self.selected_files.update()

    def jsons_Upload(self,e):
        self.donetext.visible=False
        self.donetext.update()
        jsonfiles=[]
        if len(self.files)==0:
            return
        if self.openapi:
            pass
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Setting is required"), open=True))
            return
        
        self.filetext.value="Uploading - "
        self.progress.visible=True
        self.progress.update()
        try:
            jsonfiles=embedding_folder(self.files,openai_api=self.openapi,resultpath=self.indexpath)
            if len(jsonfiles)>0:
                donelist=" \n".join(jsonfiles)
                self.donelist.value=donelist
                self.donetext.visible=True
                self.donetext.update()
        except Exception as err:
            print (err)
        self.progress.visible=False
        self.progress.update()


    def build_page(self):
        self.page.controls.clear()
        self.openapi=self.page.session.get("OPENAI_API_KEY")
        self.indexpath=self.page.session.get("FAISS_INDEX_PATH")
        return ft.Column(
            [
                self.pick_files_dialog,
                self.picker,
                self.selected_files,
                self.jsonfile,
                self.progress,
                self.donetext,
            ]
        )

if __name__ == "__main__":
    def main(page: ft.Page):
        AIchat=FaissConvert(page)
        page.add(AIchat.build_page())
        page.scroll="AUTO"
        page.on_resize=page.update()
        page.update()
    
    ft.app(main)