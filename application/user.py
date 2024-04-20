import os
import pickle
from typing import Dict, List


class UserData:
    """
    The UserData class represents user-specific data, including the sequence of notes created and their contents.
    It provides methods for loading and dumping data to/from a pickle file.

    Attributes:
        history: contains a sequence of titles of notes created by the user.
        notes: contains title and text information
        _file_ext: data file extension
        _filedir: directory where user data is stored
        _abspath: full path to the user data file
    """

    _file_ext = '.pickle'
    _filedir = 'application/data/'
    # create a directory with user data files
    os.makedirs(os.path.dirname(_filedir), exist_ok=True)

    def __init__(self, filename='userdata') -> None:
        """
        Loads data from the pickle file specified in the filename.
        If the file does not exist, the values are set by default

        Args:
            filename: file name (specified without a path and without an extension)
        """
        self.history: List[str] = []
        self.notes: Dict[str, str] = {}
        self._abspath = os.path.abspath(self._filedir + filename + self._file_ext)

        try:
            with open(self._abspath, 'rb') as file:
                self.history = pickle.load(file)
                self.notes = pickle.load(file)
        except FileNotFoundError:
            pass

    def dump_data(self) -> None:
        """
        Dumps the history and notes data to a pickle file specified by abspath.
        If the file doesn't exist, it will be created.
        """
        with open(self._abspath, 'wb') as file:
            pickle.dump(self.history, file)
            pickle.dump(self.notes, file)
