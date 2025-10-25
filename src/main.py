from bs4 import BeautifulSoup as bs
from PIL import Image
from io import BytesIO
import flet as ft
import requests,base64,time

class AnimeList():
    def __init__(self,page:ft.Page):
        self.page=page
        self.page.title="AnimeList"
        self.page.window.icon="favicon.ico"
        self.page.window.maximized=False
        #self.page.window.title_bar_hidden=True
        self.cor_vermelha="#BE0B32"
        self.cor_branca="#ffffff"
        self.cor_preta="#000000"
        self.page.bgcolor=self.cor_preta
        self.page.padding=0
        self.page.spacing=0
        self.page.scroll=ft.ScrollMode.ALWAYS
        self.page.update()
        self.get_animes()
        self.list_anime =[]
        for anime in self.animes:
            ani = anime.split("|")
            self.list_anime.append(
                ft.Container(
                    ink=True,
                    url=ani[0],
                    padding=10,
                    height=260,
                    col={
                        "xs":11,
                        "sm":6,
                        "md":4,
                        "lg":3
                    },
                    bgcolor=self.cor_vermelha,
                    border_radius=20,
                    tooltip=ani[2],
                    content=ft.Column(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            ft.ResponsiveRow(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        col={
                                            "md":12
                                        },
                                        border_radius=20,
                                        content=ft.Image(
                                            src_base64=self.image_web(ani[1]),
                                            fit=ft.ImageFit.COVER,
                                            height=180
                                        )
                                    )
                                ]
                            ),
                            ft.ResponsiveRow(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        col={
                                            "md":12
                                        },
                                        padding=ft.Padding(top=10,bottom=0,left=0,right=0),
                                        content=ft.Text(
                                            value=ani[2][0:60],
                                            text_align=ft.TextAlign.CENTER
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        self.conteudo = ft.Column(
            width=self.page.width,
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            padding=ft.Padding(top=10,bottom=10,left=0,right=0),
                            col={
                                "xs":11,
                                "sm":8,
                                "md":4
                            },
                            content=ft.Text(
                                value="AnimeList",
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.BOLD,
                                size=40,
                                color=self.cor_branca,
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(top=10,bottom=10,left=0,right=0),
                            col={
                                "xs":2,
                                "md":1
                            },
                            content=ft.Image(
                                src="favicon.png"
                            )
                        )
                    ]
                ),
                ft.Container(
                    col={
                        "md":10
                    },
                    padding=ft.Padding(top=40,bottom=10,left=40,right=40),
                    content=ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=self.list_anime
                    )
                )
            ]
        )
        self.page.add(
            self.conteudo
        )
        self.page.update()

    def get_animes(self):
        self.url="https://www.anroll.net"
        self.pag=bs(requests.get(self.url).text,"html.parser")
        self.conteudo=self.pag.find_all("li",{"class":"sc-bpSLYx fRpZuV release-item"})
        self.animes=[]
        for c in self.conteudo:
            a=str(c.find("a")).split('"')[1]
            img=str(c.find("img")).split('>')[0].split('"')[len(str(c.find("img")).split('"'))-6].split(",")[0].replace("&amp;w=256&amp;q=75 1x","&w=384&q=75").replace("&amp;w=256&amp;q=75 2x","&w=384&q=75")
            self.animes.append(f"{self.url}{a}|{self.url}{img}|{(c.text).replace("Episódio"," Epiósido")}")

    def image_web(self,url):
        png_output=BytesIO()
        (Image.open(BytesIO(requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}).content))).save(png_output, format="PNG")
        png_output.seek(0)
        return base64.b64encode(png_output.read()).decode('utf-8')
    
ft.app(target=AnimeList,assets_dir="assets")