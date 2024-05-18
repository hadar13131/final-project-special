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
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        # on_change=handle_change,
        # on_submit=handle_submit,
        # on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(self.public_user_lst[i]), on_click=self.close_anchor, data=self.public_user_lst[i])
            for i in range(len(self.public_user_lst))
        ],
    )
        self.button_show_info = ft.ElevatedButton(text="show user profile details", on_click=self.show_user_info,
                                                  bgcolor='#8532B8', color='white')

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
                        ft.Text("THE Details-", size=30, color='#8532B8',
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


    def close_anchor(self, e):
        text = f"{e.control.data}"
        self.search_user.close_view(text)
        self.selected_user = e.control.data
        self.page.add(self.button_show_info)
        self.page.update()
    def chosen_user(self, e: ft.ControlEvent):
        self.selected_user = e.control.data
        self.page.add(self.button_show_info)
        self.page.update()

    def show_user_info(self, e: ft.ControlEvent) -> None:

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








    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS
        self.page.bgcolor = ft.colors.GREY_100
        self.page.add(self.search_user)
        self.page.update()


def main() -> None:
    ft.app(target=SharePage.main)


if __name__ == "__main__":
    main()


# class UserShare:
#
#     def __init__(self, client:Client) -> None:
#         self.page = None
#         self.client = client
#
#         self.text1 = ft.Text("YOUR Profile Page", size=55, color='#8532B8', weight=ft.FontWeight.W_500,
#                              selectable=True, font_family="Elephant")
#
#         self.workout_table = self.return_workout_table()
#
#         self.button_show_info = ft.ElevatedButton(text="show my profile details", on_click=self.show_your_info,
#                                                   bgcolor='#8532B8', color='white')
#
#
#         self.username1 = ft.TextField(label="user name", read_only=True, autofocus=True, border_color=ft.colors.RED)
#         self.first_name = ft.TextField(label="first name", autofocus=True, border_color='#8532B8')
#         self.last_name = ft.TextField(label="last name", autofocus=True, border_color='#8532B8')
#         self.phone_number = ft.TextField(label="phone number", autofocus=True, border_color='#8532B8')
#         self.email = ft.TextField(label="email", read_only=True, autofocus=True, border_color=ft.colors.RED)
#         self.age = ft.TextField(label="age", autofocus=True, border_color='#8532B8')
#
#         self.massageE = ft.TextField(read_only=True, border="none", color='#A8468C')
#
#         # self.gender = ft.TextField(label="gender", autofocus=True, border_color='#8532B8')
#         self.gender = ft.Dropdown(
#             label="gender",
#             hint_text="Choose your gender",
#             options=[
#                 ft.dropdown.Option("Female"),
#                 ft.dropdown.Option("Male"),
#                 ft.dropdown.Option("Other"),
#             ]
#         )
#
#         self.goals = ft.TextField(label="goals", autofocus=True, border_color='#8532B8')
#
#         self.button1 = ft.ElevatedButton(text="change", on_click=self.change_your_info, bgcolor='#8532B8', color='white')
#
#         self.public = ft.CupertinoSwitch(
#             label="Public Account",
#             on_change=self.change_privacy,
#             value=self.client.privacy,
#         )
#
#         self.info_page = ft.Container(
#                              margin=20,
#                              padding=20,
#                              alignment=ft.alignment.center,
#                              bgcolor='#CC99FF',
#                              border_radius=10,
#                              border=ft.border.all(3, '#8532B8'),
#                              content=ft.Column(
#                                  width=600,
#                                  controls=[
#                                      ft.Column([
#                                          ft.Text("Your Details-", size=30, color='#8532B8',
#                                                  weight=ft.FontWeight.W_500,
#                                                  selectable=True, font_family="Elephant",
#                                                  text_align=ft.alignment.center)
#                                      ]),
#                                      ft.Column([
#                                          ft.Text("you can change them...", size=15, color='#8532B8',
#                                                  weight=ft.FontWeight.W_500,
#                                                  selectable=True, font_family="Elephant",
#                                                  text_align=ft.alignment.center)
#                                      ]),
#                                      ft.Column([
#                                          ft.Row([
#                                              self.username1,
#                                              self.email,
#                                          ]),
#                                          ft.Row([
#                                              self.first_name,
#                                              self.last_name,
#                                          ]),
#                                          self.phone_number,
#                                          self.age,
#                                          self.gender,
#                                          self.goals,
#                                          self.public,
#                                          self.button1,
#                                          self.massageE
#                                      ]),
#
#                                  ],
#                              ))
#
#         self.count_workouts = ft.Column(
#             alignment=ft.alignment.top_center,
#             controls=[
#                 ft.Row([
#                     ft.Text("WORKOUT COUNTER", size=30, color='#8532B8', weight=ft.FontWeight.W_500,
#                             selectable=True, font_family="Elephant", text_align=ft.alignment.center)
#                 ]),
#
#             ft.Container(
#                     margin=10,
#                     padding=10,
#                     alignment=ft.alignment.center,
#                     bgcolor='#CC99FF',
#                     border_radius=360,
#                     content=ft.Row(
#                         [
#                             ft.Column([
#                                 self.button_count("YOU PLANED- " + str(self.count_future_workouts(datetime.now())) + " WORKOUTS")
#
#                             ]),
#                             ft.Column([
#                                 self.button_count(
#                                     "YOU DID- " + str(len(self.client.user_workout_lst) - int(
#                                     self.count_future_workouts(datetime.now()))) + " WORKOUTS")
#
#                             ])
#                         ]
#                     )
#                 )]
#         )
#
#
#         self.table1 = ft.Row(
#             # scroll=ft.ScrollMode.ALWAYS,
#             # width=600,
#             controls=[
#                 ft.Container(
#                     margin=10,
#                     padding=10,
#                     alignment=ft.alignment.center,
#                     bgcolor='#CC99FF',
#                     content=ft.Row(
#                         controls=[
#                             # ft.Row([
#                             #     ft.Text("YOUR WORKOUTS PLAN:", size=20, color='#8532B8',
#                             #             weight=ft.FontWeight.W_500,
#                             #             selectable=True, font_family="Arial Rounded MT Bold"),
#                             # ]),
#                             self.workout_table
#                             # ft.Column([
#                             #
#                             #         # scroll=ft.ScrollMode.ALWAYS,
#                             #         self.workout_table
#                             #     # ft.ElevatedButton(text="change details", on_click=self.change_your_info,
#                             #     #                   bgcolor='#8532B8',
#                             #     #                   color='white'),
#                             # ]
#
#                             # ),
#
#                         ]
#                     )
#                 ),
#
#                 ft.Column([]),
#
#             ],
#             alignment=ft.MainAxisAlignment.CENTER
#         )
#
#
#         self.view = (ft.Column
#         ([
#             ft.Row([
#             ft.Text("YOUR Profile Page", size=55, color=ft.colors.BLACK, weight=ft.FontWeight.W_500,
#                                     selectable=True, font_family="Century Gothic", text_align=ft.alignment.center),
#             ]),
#             ft.Row([
#                 self.button_show_info
#             ]),
#             ft.Row([
#
#             ])
#         ]))
#
#
#         self.view2 = ft.Column([
#                          ft.Container(
#                              margin=10,
#                              padding=10,
#                              alignment=ft.alignment.top_left,
#                              bgcolor='#CC99FF',
#                              border_radius=10,
#                              border=ft.border.all(3, '#8532B8'),
#                              content=ft.Row(
#                                  # width=600,
#                                  controls=[
#                                      ft.Column(scroll=ft.ScrollMode.ALWAYS,
#                                             height=400,
#                                                controls=[
#                                              ft.Row([
#                                                  ft.Text("YOUR WORKOUTS PLAN:", size=20, color='#8532B8',
#                                                          weight=ft.FontWeight.W_500,
#                                                          selectable=True, font_family="Arial Rounded MT Bold")
#                                              ]),
#                                              ft.Row(
#                                                  controls=[
#                                                  self.table1
#                                              ]),
#
#                                      ]),
#
#
#
#                                  ],
#                              ))
#                      ])
#
#         self.veiw3 = ft.Column(
#                     alignment=ft.MainAxisAlignment.START,
#                     controls=[ft.Container(
#                              margin=10,
#                              padding=10,
#                              # alignment=ft.alignment.center,
#                              # bgcolor='#CC99FF',
#                              # border_radius=10,
#                              # border=ft.border.all(3, '#8532B8'),
#                              content=ft.Column(
#                                  controls=[
#                                      ft.Column(
#                                          height=400,
#                                          alignment=ft.MainAxisAlignment.START,
#                                          controls=[
#                                          self.count_workouts
#                                  ],
#                              )
#                      ])
#
#                         )])
#
#         # self.veiw3 = ft.Container(
#         #         margin=10,
#         #         padding=10,
#         #         # alignment=ft.alignment.center,
#         #         # bgcolor='#CC99FF',
#         #         # border_radius=10,
#         #         # border=ft.border.all(3, '#8532B8'),
#         #         content=self.count_workouts,
#         #             alignment=ft.alignment.top_right
#         #
#         #
#         #     )
#
#     def change_privacy(self, e: ft.ControlEvent):
#         public = self.public.value
#         response = self.client.change_privacy(name=self.client.username, public=public)
#         self.massageE.value = response["response"]
#         self.page.update()
#
#     def button_count(self, value: str):
#         button = ft.FilledButton(
#             value,
#             style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=100, bgcolor="#D767F5", color=ft.colors.BLACK)
#         )
#
#         return button
#
#     def show_user_info(self, e: ft.ControlEvent) -> None:
#
#         info1 = self.client.bring_info(self.)
#
#         self.username1.value = self.client.username
#         # self.email.value = info1["email"]
#         self.first_name.value = info1["first_name"]
#         self.last_name.value = info1["last_name"]
#         # self.phone_number.value = info1["phone_num"]
#         self.age.value = info1["age"]
#         self.gender.value = info1["gender"]
#         self.goals.value = info1["goals"]
#
#         self.page.clean()
#         row_container = ft.Row([self.info_page])
#         row_container.main_alignment = ft.MainAxisAlignment.CENTER
#
#         row_container.width = 600
#         self.page.add(row_container)
#
#         self.page.update()
#
#
#     def change_your_info(self, e: ft.ControlEvent):
#         username1 = self.client.username
#         firstname = self.first_name.value
#         lastname = self.last_name.value
#         phone_number = self.phone_number.value
#         email = self.email.value
#         age = int(self.age.value)
#         gender = self.gender.value
#         goals = self.goals.value
#
#         if firstname and lastname and phone_number and age and gender and goals:
#             if c_e.is_valid_phone_number(phone_number):
#                 response = self.client.fill_info(name=username1, first_name=firstname, last_name=lastname,
#                                                  phone_num=phone_number, email=email, age=age, gender=gender, goals=goals)
#                 self.massageE.value = response["response"]
#
#                 if self.massageE.value == "the information added":
#                     self.massageE.value = "the information changed"
#                     # row = ft.Row([self.button_Next])
#                     # self.page.add(row)
#                     self.page.update()
#
#             else:
#                 self.massageE.value = "the phone number is not write correctly"
#                 self.page.update()
#
#         else:
#             self.massageE.value = "please fill the all fields"
#             self.page.update()
#
#
#     def return_workout_table(self):
#
#         # the values is the place in the database.
#         date_lst = [] #value = 3
#         name_lst = [] #value = 2
#         workoutinfo_lst = [] #value = 4
#
#         date_lst = self.future_workouts_by_value(value=3)
#         name_lst = self.future_workouts_by_value(value=2)
#         workoutinfo_lst = self.future_workouts_by_value(value=4)
#
#         workoutinfo_lst1 = []
#         for w in workoutinfo_lst:
#             workoutinfo_lst1.append(self.format_exercise_lst(e_lst=w))
#
#         row_lst = []
#
#         for i in range(len(date_lst)):
#             row_lst.append(
#                 ft.DataRow(
#                     cells=[
#                         ft.DataCell(ft.Text(datetime.strptime(date_lst[i], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d'))),
#                         ft.DataCell(ft.Text(name_lst[i])),
#                         # ft.DataCell(ft.ExpansionTile(title=ft.Text("workout info"), controls=workoutinfo_lst1[i]))
#                     ],
#                 ))
#
#
#         table1 = ft.DataTable(
#             # width=100,
#             # height=100,
#             columns=[
#                 ft.DataColumn(ft.Text("date")),
#                 ft.DataColumn(ft.Text("workout name")),
#                 # ft.DataColumn(ft.Text("workout info"), numeric=True),
#             ],
#             rows=row_lst
#         )
#
#         return table1
#
#     # def workout_info_format(self, workout):
#     #     for i1 in workout:
#     #         i = json.loads(i1)
#     #         ft.ExpansionTile(
#     #             title=ft.Text("exercises-"),
#     #             subtitle=ft.Text("TAP TO SEE THE EXERCISES"),
#     #             affinity=ft.TileAffinity.LEADING,
#     #             # initially_expanded=True,
#     #             collapsed_text_color=ft.colors.BLUE,
#     #             text_color=ft.colors.BLUE,
#     #             controls=self.format_exercise_lst(i["exerciselist"])
#     #         )
#
#     def format_exercise_lst(self, e_lst):
#         lst = []
#         if not e_lst:
#             return lst
#
#         n = 1
#         for i1 in e_lst:
#             i = json.loads(i1)
#             temp = ft.ExpansionTile(
#                 title=ft.Text(f"exercise {n}- {i['name']}"),
#                 subtitle=ft.Text("open for more"),
#                 affinity=ft.TileAffinity.LEADING,
#                 collapsed_text_color=ft.colors.PINK,
#                 text_color=ft.colors.PINK,
#                 controls=[
#                     ft.ExpansionTile(
#                         title=ft.Text("exercise information- "),
#                         subtitle=ft.Text("open for more"),
#                         affinity=ft.TileAffinity.LEADING,
#                         # initially_expanded=True,
#                         collapsed_text_color=ft.colors.BLUE,
#                         text_color=ft.colors.BLUE,
#                         controls=[
#                             ft.ListTile(title=ft.Text("power- " + i["power"]))
#                         ]
#                     ),
#
#                     ft.ExpansionTile(
#                         title=ft.Text("exercise sets- "),
#                         subtitle=ft.Text("open for more"),
#                         affinity=ft.TileAffinity.LEADING,
#                         # initially_expanded=True,
#                         collapsed_text_color=ft.colors.BLUE,
#                         text_color=ft.colors.BLUE,
#                         controls=self.format_set_lst(i["sets"])
#                     )
#                 ]
#             )
#
#             lst.append(temp)
#             n = n + 1
#
#         return lst
#
#
#     def format_set_lst(self, s_lst):
#         lst = []
#         if not s_lst:
#             return lst
#
#         for s in s_lst:
#             # s = json.loads(s1)
#             repetitions = s["repetitions"]
#             time = s["time"]
#             weight = s["weight"]
#             distance_KM = s["distance_KM"]
#
#             str1 = (f"repetitions- {repetitions} time- {time} weight- {weight} distance_KM- "
#                     f"{distance_KM}")
#             temp = ft.ListTile(title=ft.Text(str1))
#             lst.append(temp)
#
#         return lst
#
#     def future_workouts_by_value(self, value):
#         workout_lst = self.client.user_workout_lst
#
#         lst = []
#         for i in workout_lst:
#             date1 = datetime.strptime(i[3], '%Y-%m-%dT%H:%M:%S')
#             if date1 >= datetime.now():
#                 lst.append(i[value])
#
#         return lst
#
#     def count_future_workouts(self, date):
#         workout_lst = self.client.user_workout_lst
#
#         n = 0
#         for i in workout_lst:
#             date1 = datetime.strptime(i[3], '%Y-%m-%dT%H:%M:%S')
#             if date1 >= datetime.now():
#                 n = n + 1
#
#         return n
#
#
#
#
#     def main(self, page: ft.Page) -> None:
#         self.page = page
#         self.page.scroll = ft.ScrollMode.ALWAYS
#
#         row_container = ft.Row([self.view])
#         # row_container.main_alignment = ft.MainAxisAlignment.CENTER
#
#         row_container.width = 920
#         self.page.add(row_container)
#
#         self.page.add(ft.Row(
#             alignment=ft.MainAxisAlignment.CENTER,
#             controls=[ft.Row([self.view2, self.veiw3])]))
#
#         self.page.bgcolor = "#E7CDFF"
#         self.page.update()
#
#
# def main() -> None:
#     ft.app(target=Profile_Page.main)
#
#
# if __name__ == "__main__":
#     main()