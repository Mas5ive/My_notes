import pickle
from typing import List, Dict


FILENAME = 'data/userdata.pickle'


class UserData:
    def __init__(self):
        self.history: List[str] = []
        self.notes: Dict[str, str] = {}
        self._load_data()

    def _load_data(self):
        try:
            with open(FILENAME, 'rb') as file:
                self.history = pickle.load(file)
                self.notes = pickle.load(file)
        except FileNotFoundError:
            pass

    def dump_data(self):
        with open(FILENAME, 'wb') as my_test_file:
            pickle.dump(self.history, my_test_file)
            pickle.dump(self.notes, my_test_file)


if __name__ == '__main__':
    pass
