import flet as ft
from time import sleep
from module_langchain.QAchain import ask_asme


class Message():
    def __init__(self, user_name: str, text: str, message_type: str = "chat_message",subcontents=[]):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type
        self.subcontents=subcontents

class ChatMessage(ft.Column):
    def __init__(self, message: Message):
        super().__init__()
        user_name=message.user_name
        text = message.text
        message_type = message.message_type
        self.subcontents=message.subcontents
        self.icon=ft.CircleAvatar(
            content=ft.Text(self.get_initials(user_name)),
            color=ft.colors.WHITE,
            bgcolor=self.get_avatar_color(user_name),
            width=40
        )
        self.subcontents_row=ft.Column()
        self.subcontents_row.visible=False
        self.textcontent=ft.Column(
            [
                ft.Text(user_name, weight="bold"),
                ft.Text(text, selectable=True),
            ],
            tight=True,
            spacing=5,
            expand=True,
            #icons.KEYBOARD_DOUBLE_ARROW_DOWN
        )
        self.toggle_subcon_btn = ft.IconButton(
            icon=ft.icons.KEYBOARD_DOUBLE_ARROW_DOWN,
            selected_icon_color=ft.colors.BLUE_GREY_400,
            selected=False,
            selected_icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP,
            on_click=self.toggle_subcontents,
            icon_size=20,
        )
        self.horizontal_alignment=ft.CrossAxisAlignment.START
        self.controls=[
            ft.Column([
                ft.Row([self.icon,self.textcontent,self.toggle_subcon_btn]),
                self.subcontents_row,
            ])
        ]
        self.subcon_set()
            
    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        return "G"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
    
    def toggle_subcontents(self,e):
        self.subcontents_row.visible = not self.subcontents_row.visible
        self.toggle_subcon_btn.selected = not self.toggle_subcon_btn.selected
        self.page.update()

    def subcon_set(self):
        if len(self.subcontents)==0:
            self.toggle_subcon_btn.visible=False
        for text in self.subcontents:
            try:
                self.subcontents_row.controls.append(ft.Text(text))
            except:
                continue
            

class VectorQAAI(ft.UserControl):
    def __init__(self,chatpage:ft.Page):
        super().__init__()
        self.page=chatpage
        self.page.pubsub.subscribe(self.on_message)
        self.user_name=self.page.session.get("user_name")
        self.new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=self.send_message_click,
        )
        self.chat = ft.ListView(
            height=500,
            # expand=5,
            spacing=10,
            auto_scroll=True,
        )
        self.chatbtn=ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=self.send_message_click
                )
        self.engineertype=ft.Dropdown(
            options=[
                ft.dropdown.Option("Mechanical"),
                ft.dropdown.Option("Electrical"),
                ft.dropdown.Option("Manual"),
            ],
            value="Manual",
            on_change=self.changetype,
        )
        self.promptmessage=ft.TextField(label="PROMPT",expand=True,value="")
        self.prompt_row=ft.Row([self.engineertype,self.promptmessage])
        self.new_message_row=ft.Row([self.new_message,self.chatbtn])
        self.chathistory=None
        # self.new_message_row=ft.Row([self.new_message,self.chatbtn])

    def on_message(self,message:Message):
        m=ChatMessage(message)
        self.chat.controls.append(m)
        self.chat.update()

    def send_message_click(self,e):
        self.user_name=self.page.session.get("user_id")
        query=self.new_message.value
        
        if query !="":
            usermessage=Message(self.user_name,query)
            self.page.pubsub.send_all(usermessage)
            self.new_message_row.visible=False
            self.new_message.value = ""
            self.new_message_row.update()
            try:
        
                result=ask_asme(query,self.indextpath,chat_history=self.chathistory,prompt_concept=self.promptmessage.value,openai_api=self.openapi)
                print (result)
                self.chathistory=result['chat_history']
                sub_text1="source1\n"+self.subcon_text(result['source_documents'][0])
                sub_text2="source2\n"+self.subcon_text(result['source_documents'][1])
                aichat1=Message(self.engineertype.value+"GPT", result['answer'],subcontents=[sub_text1,sub_text2])
                
            except Exception as err:
                aichat1=Message(self.engineertype.value+"GPT", "Error:"+str(err))
            self.page.pubsub.send_all(aichat1)
            
        self.new_message_row.visible=True
        self.new_message_row.update()
    
    def subcon_text(self,source_document):
        text_source="DOC: "+source_document.metadata['source']
        try:
            text_page ="PAGE: "+str(int(source_document.metadata['page']))
        except:
            text_page=""
        origin_text=source_document.page_content
        conc_text=text_source+"\n"+text_page+"\n"+origin_text
        return conc_text

    def changetype(self,e):
        if self.engineertype.value=="Mechanical":
            self.promptmessage.value="You are the Mechanical Engineer for plant engineering."
            self.promptmessage.read_only=True
        elif self.engineertype.value=="Electrical":
            self.promptmessage.value="You are the Electrical Engineer for plant engineering."
            self.promptmessage.read_only=True
        else:
            self.promptmessage.value=""
            self.promptmessage.read_only=False
        self.prompt_row.update()

    
    def build_page(self):
        self.openapi=self.page.session.get("OPENAI_API_KEY")
        self.indextpath=self.page.session.get("FAISS_INDEX_PATH")
        self.user_name=self.page.session.get("user_id")
        
        return ft.Column([ft.Container(content=ft.Column(
            [ft.Container(content=ft.Column([
                    ft.Container(content=self.prompt_row,padding=ft.padding.symmetric(horizontal=30)),
                    ft.Container(content=self.chat,padding=ft.padding.symmetric(horizontal=30)),
                    ft.Container(content=self.new_message_row,padding=ft.padding.symmetric(horizontal=30)),
                ]))
            ]
            ),
            padding=ft.padding.symmetric(horizontal=30)
        )],
        )


if __name__ == "__main__":
    def main(page: ft.Page):
        AIchat=VectorQAAI(page)
        page.add(AIchat.build_page())
        page.scroll="AUTO"
        page.on_resize=page.update()
        page.update()
    
    ft.app(main)
