import PySimpleGUI as sg

from screens.intro import intro_screen


sg.set_options(font=("Arial", 16))


def main():
    intro_screen()


if __name__ == "__main__":
    main()
