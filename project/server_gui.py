import json
import requests

import flet as ft

import sqlite3
from project.models import Set, Exercise, Workout
from datetime import datetime

import project.api

class ServerInfo:
    def __init__(self):
        self.server_address = "http://127.0.0.1:1234"

    def signed_up_users(self):

        response = requests.get(
            f"{self.server_address}/signed_up_users"
        )

        return response.json()


class ServerVeiw:
    def __init__(self) -> None:
        self.page = None

        temp_server = ServerInfo()

        self.user_lst = temp_server.signed_up_users()["response"]



    def return_workout_table(self):
        row_lst = []

        for i in range(len(self.user_lst)):
            row_lst.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.user_lst[i])),
                    ],
                ))

        table1 = ft.DataTable(
            # width=100,
            # height=100,
            columns=[
                ft.DataColumn(ft.Text("users name")),
            ],
            rows=row_lst
        )

        return table1

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS

        self.page.add(self.return_workout_table())

        self.page.bgcolor = "#E7CDFF"
        self.page.update()


def main() -> None:
    ft.app(target=ServerVeiw().main)


if __name__ == "__main__":
    main()