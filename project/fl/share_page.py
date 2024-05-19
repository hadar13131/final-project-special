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

        self.username1 = ft.TextField(label="user name", read_only=True, autofocus=True, border_color="#9C1414")
        self.first_name = ft.TextField(label="first name", read_only=True, autofocus=True, border_color="#9C1414")
        self.last_name = ft.TextField(label="last name", read_only=True, autofocus=True, border_color="#9C1414")
        self.age = ft.TextField(label="age", read_only=True, autofocus=True, border_color="#9C1414")

        self.gender = ft.TextField(label="gender", read_only=True, autofocus=True, border_color="#9C1414")

        self.goals = ft.TextField(label="goals", read_only=True, autofocus=True, border_color="#9C1414")

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

        self.show_user_info()
        self.show_user_workouts()

        self.page.update()

    def show_user_info(self) -> None:

        self.info_page = ft.Container(
            margin=20,
            padding=20,
            alignment=ft.alignment.center,
            bgcolor='#B3B3FF',
            border_radius=10,
            border=ft.border.all(5, '#BB77F9'),
            content=ft.Column(
                width=600,
                controls=[
                    ft.Column([
                        ft.Text(f"{self.selected_user} profile details-", size=30, color='#0E2841',
                                weight=ft.FontWeight.W_500,
                                selectable=True, font_family="Aptos",
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
        self.page.add(ft.Row([row_container]))

        self.page.update()

    def show_user_workouts(self) -> None:
        workoutid_lst = self.client.bring_shared_workoutid(chosed_user=self.selected_user)["response"]

        if not workoutid_lst:
            self.massage_show_workout.value = f"{self.selected_user} didn't share any workout"
            self.page.add(self.massage_show_workout)
            self.page.update()

        else:

            lst_workout = []
            for i in workoutid_lst:
                lst_workout.append(self.client.full_workout_by_workoutid(i)["response"])

            sorted_workout_lst = sorted(lst_workout, key=lambda x: x[3])

            self.full_workout_formate = self.show_workout(sorted_workout_lst)
            self.page.add(
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        controls=self.full_workout_formate
                    ))
            # self.page.add(self.full_workout_formate)
            self.page.update()


    #build the workout formate
    def show_workout(self, lst):
        format_workout_lst = []

        for i in lst:
            temp = ft.Container(
                width=500,
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor='#98BAFE',
                border_radius=10,
                border=ft.border.all(3, '#6A9BFE'),
                content=ft.Column(
                    [
                        ft.Row(

                            controls=[
                                ft.Text("Workout name- " + i[2], size=20, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_500, selectable=True, font_family="Aptos",
                                        text_align=ft.alignment.center),

                                ft.Text("date- " + str(datetime.strptime(i[3], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')),
                                        size=20, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_500, selectable=True, font_family="Aptos",
                                        text_align=ft.alignment.center)
                            ]
                        ),

                        ft.ExpansionTile(
                            title=ft.Text(i[2] + " exercises-"),
                            subtitle=ft.Text("TAP TO SEE THE EXERCISES"),
                            affinity=ft.TileAffinity.LEADING,
                            # initially_expanded=True,
                            collapsed_text_color="#525252",
                            text_color="#525252",
                            controls=self.format_exercise_lst(i[4])
                        )
                    ]
                )
            )

            format_workout_lst.append(temp)

        return format_workout_lst

    def format_exercise_lst(self, e_lst):
        lst = []
        if not e_lst:
            return lst

        n = 1
        for i1 in e_lst:
            i = json.loads(i1)
            temp = ft.ExpansionTile(
                title=ft.Text(f"exercise {n}- {i['name']}"),
                subtitle=ft.Text("open for more"),
                affinity=ft.TileAffinity.LEADING,
                collapsed_text_color='#8532B8',
                text_color='#8532B8',
                controls=[
                    ft.ExpansionTile(
                        title=ft.Text("exercise information- "),
                        subtitle=ft.Text("open for more"),
                        affinity=ft.TileAffinity.LEADING,
                        # initially_expanded=True,
                        collapsed_text_color=ft.colors.BLACK,
                        text_color=ft.colors.BLACK,
                        controls=[
                            ft.ListTile(title=ft.Text("power- " + i["power"]))
                        ]
                    ),

                    ft.ExpansionTile(
                        title=ft.Text("exercise sets- "),
                        subtitle=ft.Text("open for more"),
                        affinity=ft.TileAffinity.LEADING,
                        # initially_expanded=True,
                        collapsed_text_color=ft.colors.BLACK,
                        text_color=ft.colors.BLACK,
                        controls=self.format_set_lst(i["sets"])
                    )
                ]
            )

            lst.append(temp)
            n = n + 1

        return lst

    def format_set_lst(self, s_lst):
        lst = []
        if not s_lst:
            return lst

        for s in s_lst:
            # s = json.loads(s1)
            repetitions = s["repetitions"]
            time = s["time"]
            weight = s["weight"]
            distance_KM = s["distance_KM"]

            str1 = (f"repetitions- {repetitions} time- {time} weight- {weight} distance_KM- "
                    f"{distance_KM}")
            temp = ft.ListTile(title=ft.Text(str1), text_color="#AA74EC")
            lst.append(temp)

        return lst

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS
        self.page.bgcolor = "#D1D1FF"
        self.page.add(self.search_user)
        self.page.update()


def main() -> None:
    ft.app(target=SharePage.main)


if __name__ == "__main__":
    main()

