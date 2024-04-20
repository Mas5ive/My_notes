from application.note_app import NoteApp
from application.user import UserData


def main():
    user_data = UserData()
    app = NoteApp(user_data)
    app.run()


if __name__ == '__main__':
    main()
