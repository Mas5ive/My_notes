import pickle
from typing import List, Dict


class UserData:
    """
    The UserData class represents user-specific data, including the sequence of notes created and their contents.
    It provides methods for loading and dumping data to/from a pickle file.

    Attributes:
        history: contains a sequence of titles of notes created by the user.
        notes: contains title and text information
    """

    def __init__(self) -> None:
        self.history: List[str] = []
        self.notes: Dict[str, str] = {}

    def load_data(self, filepath: str) -> None:
        """
        Loads data from a pickle file specified by filepath.
        If the file doesn't exist, the method silently does nothing.
        """
        try:
            with open(filepath, 'rb') as file:
                self.history = pickle.load(file)
                self.notes = pickle.load(file)
        except FileNotFoundError:
            pass

    def dump_data(self, filepath: str) -> None:
        """
        Dumps the history and notes data to a pickle file specified by filepath.
        If the file doesn't exist, it will be created.
        """
        with open(filepath, 'wb') as file:
            pickle.dump(self.history, file)
            pickle.dump(self.notes, file)
