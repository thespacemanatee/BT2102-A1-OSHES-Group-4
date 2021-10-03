import PySimpleGUI as pg

from screens.login import login_screen


def main():
    # 0 - START HERE: intro window
    intro_layout = [[pg.Text("Welcome to OSHES.")],
                    [pg.Text("Are you a customer or an administrator?")],
                    [pg.Button('Customer'), pg.Button('Administrator')]
                    ]
    intro_window = pg.Window('Welcome!', intro_layout)
    intro_event, intro_values = intro_window.read()
    intro_window.close()
    # goes to screens/login.py - open customer login window or admin login window
    login_screen(intro_event, intro_values)


if __name__ == "__main__":
    main()
