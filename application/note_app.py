from prompt_toolkit.application import Application
from typing import Callable
from .user import UserData
from .sub_apps import gallery


class NoteApp:
    """
    The NoteApp class introduces a note-taking application that uses the State pattern.
    it`s responsible for managing the user data, file paths, and the flow of sub-applications.
    """

    def __init__(self, user_data: UserData) -> None:
        """
        Setting the path to the file with user and application data states

        Instance attributes:

            user_data: an instance of UserData class to store user data.

            States:

            cur_sub_app: current active sub-app. When an instance of the class is initialised,
                it is always in the "gallery" state.
            prev_sub_app: previous active sub-app. Influences the logic behavior of the current state
        """
        self._prev_sub_app: Callable[..., Application] | None = None
        self._cur_sub_app: Callable[..., Application] | None = gallery
        self.user_data = user_data

    def run(self) -> None:
        """
        Runs the note-taking application by switching sub-applications (its windows) and changing user data.
        """
        note_num = 0
        while self._cur_sub_app:
            sub_app = self._cur_sub_app(self.user_data, note_num, self._prev_sub_app)
            next_sub_app, note_num = sub_app.run()
            self._prev_sub_app = self._cur_sub_app
            self._cur_sub_app = next_sub_app

        self.user_data.dump_data()
