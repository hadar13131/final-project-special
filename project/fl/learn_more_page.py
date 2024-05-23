import flet as ft
import welcome_page


class LearnMorePage:

    def __init__(self) -> None:
        self.page = None
        self.text1 = ft.Text("ABOUT US", size=60, color='#8532B8', weight=ft.FontWeight.W_500,
                             selectable=True, font_family="Elephant")

        self.m1 = ft.Text("information", size=20, color='#8532B8')
        self.m2 = ft.Text("pictures", size=20, color='#8532B8')

        self.button_Back = ft.ElevatedButton(text="BACK", on_click=self.back_to_welcome, bgcolor='#8532B8',
                                             color='white')

        self.main_text = ft.Text(
            f"POWER APP is a training application, where you can \nPLAN, EDIT and SEE your progress over time. \n\n"
            f"In addition, you will be able to SHARE your selected workouts \nwith other users, "
            f"and you will also be able \nto see theirs!",
            size=30, color="#99CCFF", weight=ft.FontWeight.W_500,
            font_family="Aharoni"
        )

        self.learn_more_panel = ft.Column(
            [
                self.text1,
                self.m1,
                self.m2,
                self.button_Back
            ]
        )

        self.learn_more_panel = ft.Column(
            # width=600,
            controls=[
                self.button_Back,
                ft.Text("ABOUT US", size=60, color='#8532B8', weight=ft.FontWeight.W_500,
                        selectable=True, font_family="Elephant"),
                self.main_text,
            ]
        )


    def back_to_welcome(self, e: ft.ControlEvent) -> None:
        self.page.clean()
        app_instance = welcome_page.First_page()
        app_instance.main(self.page)

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.ALWAYS

        row_container = ft.Row([self.learn_more_panel])
        row_container.main_alignment = ft.MainAxisAlignment.CENTER

        row_container.width = 920
        self.page.add(row_container)

        self.page.horizontal_alignment = 'CENTER'
        self.page.vertical_alignment = 'CENTER'

        self.page.update()


def main() -> None:
    ft.app(target=LearnMorePage.main)


if __name__ == "__main__":
    main()