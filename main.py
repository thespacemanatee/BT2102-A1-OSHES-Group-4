import PySimpleGUI as sg

from app.database.utils import cancel_requests_after_deadline
from app.screens.intro import intro_screen

sg.change_look_and_feel('Reddit')
sg.set_options(font=("Arial", 13))


def main():
    cancel_requests_after_deadline()
    intro_screen()


if __name__ == "__main__":
    main()
