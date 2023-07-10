from typing import Literal
from data.user import UserData
from sub_apps import gallary


class NoteApp:

    def __init__(self) -> None:
        self.prev_sub_app = None
        self.cur_sub_app = gallary
        self.user_data = UserData()

    def __enter__(self) -> 'NoteApp':
        self.user_data.load_data()
        return self

    def __exit__(self, type, value, tb) -> Literal[False]:
        self.user_data.dump_data()
        return False

    def run(self) -> None:
        note_num = 0
        while self.cur_sub_app:
            sub_app = self.cur_sub_app(self.user_data, note_num, self.prev_sub_app)
            next_sub_app, note_num = sub_app.run()
            self.prev_sub_app = self.cur_sub_app
            self.cur_sub_app = next_sub_app
