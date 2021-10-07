import PySimpleGUI as sg

from app.screens.intro import intro_screen

sg.change_look_and_feel('Reddit')
sg.set_options(font=("Arial", 16))


def main():
    intro_screen()


if __name__ == "__main__":
    main()