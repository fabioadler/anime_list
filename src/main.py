from bs4 import BeautifulSoup as bs
from PIL import Image
from io import BytesIO
import flet as ft
import requests,base64,webbrowser,time

class MeusAnimes():
    def __init__(self,page:ft.Page):
        self.page=page
        self.page.title="Animes"
        self.page.window.icon="favicon.ico"
        self.page.scroll=ft.ScrollMode.ALWAYS
        self.page.update()
        self.home()

    def home(self):
        self.page.clean()
        self.animes=[]
        for anime in self.get_animes():
            self.animes.append(
                ft.Container(
                    expand=True,
                    ink=True,
                    url=anime["link"],
                    col={
                        "xs":12,
                        "sm":6,
                        "md":3
                    },
                    padding=6,
                    border_radius=10,
                    content=ft.Column(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                expand=True,
                                border_radius=10,
                                src_base64=self.image_web(anime["image"]),
                                fit=ft.ImageFit.COVER
                            ),
                            ft.Text(
                                expand=True,
                                value=anime["nome"]
                            )
                        ]
                    ),
                    on_click=lambda e: webbrowser.open_new(e.url)
                )
            )
        self.conteudo_pag=ft.Container(
            expand=True,
            margin=ft.Margin(top=20,bottom=0,left=0,right=0),
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.ResponsiveRow(
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    col={
                                        "xs":10,
                                        "sm":8,
                                        "md":6
                                    },
                                    content=ft.Column(
                                        expand=True,
                                        alignment=ft.MainAxisAlignment.START,
                                        controls=[
                                            ft.Text(
                                                value="Lista de Animes",
                                                size=40,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(
                                                value="Animes Online",
                                                size=15,
                                                weight=ft.FontWeight.BOLD
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        margin=ft.Margin(top=40,bottom=0,left=0,right=0),
                        content=ft.ResponsiveRow(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=self.animes
                        )
                    )
                ]
            )
        )
        self.page.add(self.conteudo_pag)
        self.page.update()
        time.sleep(60)
        self.home()  

    def get_animes(self):
        conteudo=(bs(requests.get("https://animesonlinecc.to/").text,"html.parser")).find_all("article",{'class':'item se episodes'})
        animes=[]
        c=0
        for ani in list(map(lambda e: f"{e.text};;{str(e.find("img")).split('"')[3]};;{str(e.find("a")).split('"')[1]}",conteudo)):
            if(c>5):
                anime = ani.split(";;")
                animes.append({"nome":anime[0],"image":anime[1],"link":anime[2]})
            else:
                pass
            c+=1

        return animes
    
    def image_web(self,url):
        png_output = BytesIO()
        (Image.open(BytesIO(requests.get(url).content))).save(png_output, format="PNG")
        png_output.seek(0)
        return base64.b64encode(png_output.read()).decode('utf-8')
    
ft.app(target=MeusAnimes,assets_dir="assets")