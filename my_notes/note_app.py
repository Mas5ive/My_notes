from prompt_toolkit.application import Application
from typing import Literal, Callable
from data.user import UserData
from sub_apps import gallery


class NoteApp:
    """
    The NoteApp class introduces a note-taking application that uses the State pattern.
    it`s responsible for managing the user data, file paths, and the flow of sub-applications.

    The __enter__ and __exit__ methods implement a context manager to automatically load and
    dump the user data to a file.

    Attributes:
        _filedir: directory where user data is stored
        _file_ext: data file extension
    """

    _filedir = 'data/'
    _file_ext = '.pickle'

    def __init__(self, filename: str = 'userdata') -> None:
        """
        Setting the path to the file with user and application data states

        Args:
            filename: file name (specified without a path and without an extension)

        Instance attributes:

            Data:

            user_data: an instance of UserData class to store user data.
            _filepath: full path to the user data file

            States:

            cur_sub_app: current active sub-app. When an instance of the class is initialised,
                it is always in the "gallery" state.
            prev_sub_app: previous active sub-app. Influences the logic behavior of the current state
        """
        self.user_data = UserData()
        self._filepath = self._filedir + filename + self._file_ext
        self._prev_sub_app: Callable[..., Application] | None = None
        self._cur_sub_app: Callable[..., Application] | None = gallery

    def __enter__(self) -> 'NoteApp':
        """
        Enter method for the context manager.
        """
        self.user_data.load_data(self._filepath)
        return self

    def __exit__(self, type, value, tb) -> Literal[False]:
        """
        Exit method for the context manager.

        Args:
            type: Exception type, if any.
            value: Exception value, if any.
            tb: Traceback, if any.

        Returns:
            Literal[False]: Always returns False to propagate exceptions.
        """
        self.user_data.dump_data(self._filepath)
        return False

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
