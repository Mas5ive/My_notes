from note_app import NoteApp


if __name__ == '__main__':
    with NoteApp() as app:
        app.run()
