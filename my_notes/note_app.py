from prompt_toolkit.application import Application
from typing import Literal, Callable
from data.user import UserData
from sub_apps import gallery


class NoteApp:
    """
    The NoteApp class introduces a note-taking application that uses the State pattern.
    It supports a context manager for easier handling of user data.

    Attributes:
        user_data: an instance of UserData class to store user data.
        cur_sub_app: current active sub-app. When an instance of the class is initialised,
            it is always in the "gallery" state.
        prev_sub_app: previous active sub-app.
    """

    def __init__(self) -> None:
        self.prev_sub_app: Callable[..., Application] | None = None
        self.cur_sub_app: Callable[..., Application] | None = gallery
        self.user_data = UserData()

    def __enter__(self) -> 'NoteApp':
        """
        Performs setup operations when entering a 'with' block.
        Loads user data from a file.
        Returns:
            NoteApp: The current instance of the NoteApp class.
        """
        self.user_data.load_data()
        return self

    def __exit__(self, type, value, tb) -> Literal[False]:
        """
        Performs cleanup operations when exiting a 'with' block.
        Dumps user data in a file.
        Returns:
            False: Indicates that any exception raised within the 'with' block should propagate.
        """
        self.user_data.dump_data()
        return False

    def run(self) -> None:
        """
        Runs the note-taking application by switching sub-applications (its windows) and changing user data.
        """
        note_num = 0
        while self.cur_sub_app:
            sub_app = self.cur_sub_app(self.user_data, note_num, self.prev_sub_app)
            next_sub_app, note_num = sub_app.run()
            self.prev_sub_app = self.cur_sub_app
            self.cur_sub_app = next_sub_app
