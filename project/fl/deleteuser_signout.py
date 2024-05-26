from project.models import Set, Exercise
import json
import hashlib

import flet as ft

from project.client import Client

# from login_signup import LoginPage
# from login_signup import SignUpPage
import login_signup
import welcome_page
import profile_page
import menu_page


class DeleteUserPage:
    def __init__(self, client: Client) -> None:
        self.page = None
        self.client = client

        self.text3 = ft.Text("delete", size=55, color='#8532B8', weight=ft.FontWeight.W_500, selectable=True,
                             font_family="Elephant")
        self.username3 = ft.TextField(label="User Name", autofocus=True, border_color='#8532B8')
        self.password3 = ft.TextField(label="Password", autofocus=True, password=True, can_reveal_password=True,
                                      border_color='#8532B8')
        self.button_delete = ft.ElevatedButton(text="Delete", on_click=self.click3, bgcolor='#8532B8', color='white')
        self.massageD3 = ft.TextField(read_only=True, border="none", color='#A8468C')

        self.button_Back = ft.ElevatedButton(text="BACK", on_click=self.back_to_profile, bgcolor='#CC99FF',
                                             color='black')

        self.main_panel_delete = ft.Column(
            alignment=ft.alignment.center_left,
            controls=[
                self.button_Back,
                ft.Column(
                    alignment=ft.alignment.center,
                    controls=[
                        ft.Text("DELETE-", size=40, color=ft.colors.BLACK,
                                weight=ft.FontWeight.W_500,
                                selectable=True, font_family="Century Gothic"),
                        ft.Text(""),

                        ft.Text("Are you sure you want to delete your user?", size=25, color=ft.colors.BLACK,
                                weight=ft.FontWeight.W_500,
                                selectable=True, font_family="Century Gothic"),

                        ft.Text("all of your information will delete...", size=20, color=ft.colors.BLACK,
                                weight=ft.FontWeight.W_500,
                                selectable=True,
                                font_family="Century Gothic"),

                    ]
                ),
                ft.Container(
                    margin=20,
                    padding=20,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    # border=ft.border.all(30, '#E1F3F1'),
                    content=ft.Column([
                        ft.Row([self.username3]),
                        ft.Row([self.password3]),
                        ft.Row([self.button_delete, self.massageD3]),
                    ])
                ),

            ]
        )

    def back_to_profile(self, e: ft.ControlEvent) -> None:
        self.page.clean()
        app_instance = menu_page.MenuApp(client=self.client)
        app_instance.main(self.page)

    def click3(self, e: ft.ControlEvent) -> None:
        username = self.username3.value
        password = self.password3.value
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.username3.error_text = ""
        self.password3.error_text = ""

        if username and password:
            response = self.client.delete(username, hashed_password)
            self.massageD3.value = response["response"]
            if "delete success" == self.massageD3.value:
                self.client = Client()
                self.page.clean()
                app_instance = welcome_page.First_page()
                app_instance.main(self.page)
            else:
                self.page.update()

            # app_instance = login_signup.SignUpPage()
            # app_instance.main(self.page)
            # row_container = ft.Row([app_instance.main_panel_signup])
            # self.page.add(row_container)
            # self.page.update()
            # self.page.update()

        elif (not username) and password:
            self.username3.error_text = "Please enter your username"
            self.page.update()

        elif (not password) and username:
            self.password3.error_text = "Please enter your password"
            self.page.update()

        else:
            self.password3.error_text = "Please enter your password"
            self.username3.error_text = "Please enter your username"
            self.page.update()

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS

        row_container = ft.Row([self.main_panel_delete], auto_scroll=True)
        row_container.main_alignment = ft.MainAxisAlignment.CENTER

        row_container.width = 650
        self.page.add(ft.Column([self.main_panel_delete]))

        self.page.horizontal_alignment = 'CENTER'
        self.page.vertical_alignment = 'CENTER'

        self.page.update()

def main() -> None:
    ft.app(target=DeleteUserPage.main)


if __name__ == "__main__":
    main()


class SignOutPage:
    def __init__(self, client: Client) -> None:
        self.page = None
        self.client = client

        self.text3 = ft.Text("signout", size=55, color='#8532B8', weight=ft.FontWeight.W_500, selectable=True,
                             font_family="Elephant")
        self.username3 = ft.TextField(label="User Name", autofocus=True, border_color='#8532B8')
        self.password3 = ft.TextField(label="Password", autofocus=True, password=True, can_reveal_password=True,
                                      border_color='#8532B8')
        self.button3 = ft.ElevatedButton(text="signout", on_click=self.click3, bgcolor='#8532B8', color='white')
        self.massageD3 = ft.TextField(read_only=True, border="none", color='#A8468C')

        self.button_Back = ft.ElevatedButton(text="BACK", on_click=self.back_to_profile, bgcolor='#CC99FF',
                                             color='black')


        self.main_panel_signout = ft.Column(
            alignment=ft.alignment.center,
            controls=[
                self.button_Back,
                        ft.Column(
                            alignment=ft.alignment.center,
                            controls=[
                        ft.Text("signout", size=55, color='#8532B8', weight=ft.FontWeight.W_500, selectable=True,
                                font_family="Elephant", text_align=ft.alignment.center),

                        ft.Container(
                            margin=20,
                            padding=20,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                            # border=ft.border.all(30, '#E1F3F1'),
                            content=ft.Column(
                                alignment=ft.alignment.center,
                                controls=[
                                    self.username3,
                                    self.password3,
                                    self.button3,
                                    self.massageD3
                            ])
                        ),
                        ])


            ]
        )

    def back_to_profile(self, e: ft.ControlEvent) -> None:
        self.page.clean()
        app_instance = menu_page.MenuApp(client=self.client)
        app_instance.main(self.page)

    def click3(self, e: ft.ControlEvent) -> None:
        username = self.username3.value
        password = self.password3.value
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.username3.error_text = ""
        self.password3.error_text = ""

        if username and password:
            response = self.client.signout(username, hashed_password)
            self.massageD3.value = response["response"]
            self.page.update()

            if self.massageD3.value == "the details are correct":
                self.client = Client()
                self.page.clean()
                app_instance = welcome_page.First_page()
                app_instance.main(self.page)

        elif (not username) and password:
            self.username3.error_text = "Please enter your username"
            self.page.update()

        elif (not password) and username:
            self.password3.error_text = "Please enter your password"
            self.page.update()

        else:
            self.password3.error_text = "Please enter your password"
            self.username3.error_text = "Please enter your username"
            self.page.update()

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS

        row_container = ft.Row([self.main_panel_signout], auto_scroll=True)
        row_container.main_alignment = ft.MainAxisAlignment.CENTER

        row_container.width = 650
        self.page.add(ft.Column([self.main_panel_signout]))

        self.page.horizontal_alignment = 'CENTER'
        self.page.vertical_alignment = 'CENTER'

        self.page.update()

def main() -> None:
    ft.app(target=DeleteUserPage.main)


if __name__ == "__main__":
    main()