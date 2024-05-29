import requests

import flet as ft

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

        self.temp_server = ServerInfo()

        self.button_load = ft.IconButton(
            icon=ft.icons.REPLAY_CIRCLE_FILLED, on_click=self.load_again, data=0
        )


    def load_again(self, e: ft.ControlEvent):
        self.page.clean()
        self.page.add(self.button_load)
        self.page.add(self.return_workout_table())
        self.page.update()


    def return_workout_table(self):
        self.user_lst = self.temp_server.signed_up_users()["response"]
        row_lst = []

        for i in range(len(self.user_lst)):
            row_lst.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.user_lst[i][0])),
                        ft.DataCell(ft.Text(self.user_lst[i][1])),
                    ],
                ))

        table1 = ft.DataTable(
            # width=100,
            # height=100,
            columns=[
                ft.DataColumn(ft.Text("Registered Users", font_family="Arial Rounded MT Bold", size=20)),
                ft.DataColumn(ft.Text("Public Account", font_family="Arial Rounded MT Bold", size=20)),
            ],
            rows=row_lst
        )

        return table1

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS

        self.page.add(self.button_load)
        self.page.add(self.return_workout_table())

        self.page.bgcolor = "#E7CDFF"
        self.page.update()


def main() -> None:
    ft.app(target=ServerVeiw().main)


if __name__ == "__main__":
    main()