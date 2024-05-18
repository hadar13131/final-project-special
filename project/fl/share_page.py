from project.models import Set, Exercise, Workout
import json

import calendar
from datetime import datetime

import flet as ft
import calendar
from datetime import datetime
from project.client import Client

import project.check_errors as c_e

class SharePage:
    def __init__(self, client: Client) -> None:
        self.page = None
        self.client = client

        self.username1 = ft.TextField(label="user name", read_only=True, autofocus=True, border_color=ft.colors.RED)
        self.first_name = ft.TextField(label="first name", read_only=True, autofocus=True, border_color=ft.colors.RED)
        self.last_name = ft.TextField(label="last name", read_only=True, autofocus=True, border_color=ft.colors.RED)
        self.age = ft.TextField(label="age", read_only=True, autofocus=True, border_color=ft.colors.RED)

        self.gender = ft.TextField(label="gender", read_only=True, autofocus=True, border_color=ft.colors.RED)

        self.goals = ft.TextField(label="goals", read_only=True, autofocus=True, border_color=ft.colors.RED)

        self.public_user_lst = self.client.public_user_lst(userid=self.client.username)["response"]

        self.search_user = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Search Friends",
        view_hint_text="Choose a friend",
        on_change=self.handle_change,
        on_submit=self.handle_submit,
        on_tap=self.handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(self.public_user_lst[i]), on_click=self.close_anchor, data=self.public_user_lst[i])
            for i in range(len(self.public_user_lst))
        ],
    )

        self.massage_show_workout = ft.TextField(read_only=True, border="none", color='#A8468C')

        self.info_page = ft.Text("")

    def handle_change(self, e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(self, e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(self, e):
        print(f"handle_tap")

    def close_anchor(self, e):
        self.page.clean()
        self.page.add(self.search_user)
        text = f"{e.control.data}"
        self.search_user.close_view(text)
        self.selected_user = e.control.data

        self.show_user_workouts()
        self.show_user_info()
        self.page.update()

    def show_user_info(self) -> None:

        self.info_page = ft.Container(
            margin=20,
            padding=20,
            alignment=ft.alignment.center,
            bgcolor='#CC99FF',
            border_radius=10,
            border=ft.border.all(3, '#8532B8'),
            content=ft.Column(
                width=600,
                controls=[
                    ft.Column([
                        ft.Text(f"{self.selected_user} profile details-", size=30, color='#8532B8',
                                weight=ft.FontWeight.W_500,
                                selectable=True, font_family="Elephant",
                                text_align=ft.alignment.center)
                    ]),
                    ft.Column([
                        ft.Row([
                            self.username1,
                        ]),
                        ft.Row([
                            self.first_name,
                            self.last_name,
                        ]),
                        self.age,
                        self.gender,
                        self.goals,
                    ]),

                ],
            ))

        info1 = self.client.bring_info(self.selected_user)

        self.username1.value = self.selected_user
        self.first_name.value = info1["first_name"]
        self.last_name.value = info1["last_name"]
        self.age.value = info1["age"]
        self.gender.value = info1["gender"]
        self.goals.value = info1["goals"]

        row_container = ft.Row([self.info_page])
        row_container.main_alignment = ft.MainAxisAlignment.CENTER

        row_container.width = 600
        self.page.add(row_container)

        self.page.update()

    def show_user_workouts(self) -> None:
        workoutid_lst = self.client.bring_shared_workoutid(chosed_user=self.selected_user)["response"]

        if workoutid_lst == "":
            self.massage_show_workout.value = f"{self.selected_user} didn't share any workout"
            self.page.update()

        else:
            self.page.add(ft.Text("the workouts"))
            self.page.update()



    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS
        self.page.bgcolor = ft.colors.GREY_100
        self.page.add(self.search_user)
        self.page.add(self.info_page)
        self.page.update()


def main() -> None:
    ft.app(target=SharePage.main)


if __name__ == "__main__":
    main()

