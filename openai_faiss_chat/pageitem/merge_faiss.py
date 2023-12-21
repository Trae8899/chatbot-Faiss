import flet as ft
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from module_langchain.embedding_faiss import merge_faiss

class Faissmerge(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.indextpath=None
        self.openapi=None
        self.page=page
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_folder_set)
        self.selected_files = ft.Text()
        self.picker=ft.ElevatedButton(
            "Pick Folder",
            icon=ft.icons.FOLDER,
            on_click=lambda _: self.pick_files_dialog.get_directory_path()
            )
        self.mergebtn=ft.FilledButton(
            "Merge",
            icon=ft.icons.CLOUD_UPLOAD_OUTLINED,
            on_click=self.merge_clicked,
            visible=False
            )
        self.filetext=ft.Text(style=ft.TextThemeStyle.LABEL_MEDIUM)
        self.progress=ft.Column([
            ft.ProgressBar(),
            ],
            visible=False
        )
        self.targetlist=ft.Text(style=ft.TextThemeStyle.LABEL_MEDIUM)
        self.targettext=ft.Column([
            ft.Text("Target",style=ft.TextThemeStyle.LABEL_MEDIUM),
            self.targetlist,
            ],
            visible=False
        )
        self.mergepath=None
        self.faissfolders=None
    
    def get_subdirectories(self,path):
        return [(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    
    def pick_folder_set(self, e=None):
        self.mergebtn.visible, self.targettext.visible = False, False
        self.targetlist.value=None
        if e.path:
            self.mergepath = e.path
            self.selected_files.value =str(e.path)
            self.faissfolders = self.get_subdirectories(self.mergepath)
            folder_names = [name for path, name in self.faissfolders]
            self.targetlist.value = " \n".join(folder_names)
            self.targettext.visible=True
            self.mergebtn.visible=True
            
        else:
            self.selected_files.value ="Cancelled!" 
            
            
        self.targettext.update()
        self.selected_files.update()
        self.mergebtn.update()  
    # def merge_clicked(self, e=None):
    #     if self.mergepath and self.faissfolders:
    #         resultpath = self.page.session.get("FAISS_INDEX_PATH", os.path.dirname(self.mergepath))
    #         faisspaths = [os.path.join(path, name) for path, name in self.faissfolders]
    #         mergefaiss = merge_faiss(faisspaths, resultpath=resultpath)
    #         self.page.session.set("FAISS_INDEX_PATH", mergefaiss)
    #         self.targetlist.value = "Finished"
    #     self.targetlist.update()

    def merge_clicked(self,e=None):
        self.mergebtn.visible = False
        self.mergebtn.update()
        
        if not self.mergepath:
            return
        resultpath=self.indextpath
        try:
            if not os.path.exists(self.indextpath) or self.indextpath=='':
                resultpath=os.path.dirname(self.mergepath)
        except:
            pass
            

        self.progress.visible=True
        self.progress.update()
        faisspaths=[]
        try:
            for path,name in self.faissfolders:
                faisspaths.append(os.path.join(path,name))
            mergefaiss=merge_faiss(faisspaths,resultpath=resultpath)
            self.page.session.set("FAISS_INDEX_PATH",mergefaiss[0])
            self.filetext.value="Finished - "

        except Exception as err:
            print (err)
            self.filetext.value="ERROR-"+str(err)
        
        self.filetext.visible=True
        self.filetext.update()
        self.progress.visible=False
        self.progress.update()

        self.mergebtn.visible = True
        self.mergebtn.update()


    def build_page(self):
        self.page.controls.clear()
        self.openapi=self.page.session.get("OPENAI_API_KEY")
        self.indextpath=self.page.session.get("FAISS_INDEX_PATH")
        return ft.Column(
            [
                self.pick_files_dialog,
                self.picker,
                self.selected_files,
                self.targettext,
                self.mergebtn,
                self.filetext,
                self.progress,
                
            ]
        )

if __name__ == "__main__":
    def main(page: ft.Page):
        AIchat=Faissmerge(page)
        page.add(AIchat.build_page())
        page.scroll="AUTO"
        page.on_resize=page.update()
        page.update()
    
    ft.app(main)