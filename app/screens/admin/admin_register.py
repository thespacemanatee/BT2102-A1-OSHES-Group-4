import PySimpleGUI as sg

from app.utils import setup_window

NAME_VAL = 'name_val'
GENDER_VAL = 'gender_val'
EMAIL_ADDRESS_VAL = 'email_address_val'
PHONE_NUMBER_VAL = 'phone_number_val'
ADDRESS_VAL = 'address_val'
PASSWORD_VAL = 'password_val'
WRONG_ENTRY = 'wrong_entry'


def administrator_register_screen():
    layout = [[sg.Column([
        [sg.Text('Name:')],
        [sg.Input(key=NAME_VAL, size=53)],
        [sg.Text('Gender:')],
        [sg.Input(key=GENDER_VAL, size=53)],
        [sg.Text('Email Address:')],
        [sg.Input(key=EMAIL_ADDRESS_VAL, size=53)],
        [sg.Text('Phone Number:')],
        [sg.Input(key=PHONE_NUMBER_VAL, size=53)],
        [sg.Text('Address:')],
        [sg.Input(key=ADDRESS_VAL, size=53)],
        [sg.Text('Password:')],
        [sg.Input(key=PASSWORD_VAL, size=53)],
        [sg.Text(key=WRONG_ENTRY)],
        [sg.Button('Register', size=25),
         sg.Button('Cancel', size=25)]
    ], pad=25)]]

    window = setup_window('Administrator Registration', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == 'Cancel':
            break

        elif event == 'Register' and values[NAME_VAL] and values[GENDER_VAL] and values[EMAIL_ADDRESS_VAL] and \
                values[PHONE_NUMBER_VAL] and values[ADDRESS_VAL] and values[PASSWORD_VAL]:
            window.close()

        else:
            window[WRONG_ENTRY].update(
                'Please make sure every field is completed.', text_color='red')

    window.close()
