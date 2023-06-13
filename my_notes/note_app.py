from data.user import UserData


class NoteApp:

    def __init__(self) -> None:
        self._cur_app = None
        self._prev_app = None
        self.user_data = UserData()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.user_data.dump_data()
        return False

    def run(self):
        while self._cur_app:
            pass


if __name__ == '__main__':
    with NoteApp() as app:
        app.run()
