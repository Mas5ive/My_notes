from prompt_toolkit.input.posix_pipe import PosixPipeInput
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from application.user import UserData
from application.sub_apps import (
    deleter,
    editor,
    factory,
    gallery,
    view,
)


# These resources will help to map key combinations to their byte representations
# https://www.physics.udel.edu/~watson/scen103/ascii.html - ASCII Table
# https://en.wikipedia.org/wiki/ANSI_escape_code          - ANSI escape code


class TestGallery:

    def test_empty_gallery(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        # prepare data
        user_data.history.clear()
        user_data.notes.clear()

        mock_input.send_bytes(b'\x1b[B')  # DOWN - it shouldn't work.
        mock_input.send_bytes(b'\r')      # ENTER - it Shouldn't work.
        mock_input.send_text('v')         # it Shouldn't work.
        mock_input.send_text('e')         # It Should work !

        app = gallery(user_data)
        result = app.run()
        assert result == (None, 0)

    def test_call_exit(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_text('e')

        app = gallery(user_data)
        result = app.run()
        assert result == (None, 0)

    def test_call_view(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        # select the note two steps below
        mock_input.send_bytes(b'\x1b[B')  # DOWN
        mock_input.send_bytes(b'\x1b[B')  # DOWN
        mock_input.send_bytes(b'\r')      # ENTER
        mock_input.send_text('v')

        app = gallery(user_data)
        result = app.run()
        assert result == (view, 2)

    def test_call_delete(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_bytes(b'\x1b[B')  # DOWN
        mock_input.send_bytes(b'\r')      # ENTER
        mock_input.send_text('d')

        app = gallery(user_data)
        result = app.run()
        assert result == (deleter, 1)


class TestDeleter:

    def test_ok_with_no_first_note(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_bytes(b'\x1b[C')  # RIGHT
        mock_input.send_bytes(b'\r')      # ENTER

        app = deleter(user_data, 1, view)
        result = app.run()
        assert result == (view, 0)

    def test_ok_with_first_note(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_bytes(b'\x1b[C')  # RIGHT
        mock_input.send_bytes(b'\r')      # ENTER

        app = deleter(user_data, 0, view)
        result = app.run()
        assert result == (view, 0)

    def test_ok_with_single_note(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        # prepare data
        single_note = user_data.history[0]
        user_data.history = [single_note]
        user_data.notes = {single_note: user_data.notes[single_note]}

        mock_input.send_bytes(b'\x1b[C')  # RIGHT
        mock_input.send_bytes(b'\r')      # ENTER

        app = deleter(user_data, 0, view)
        result = app.run()
        assert result == (gallery, None)

    def test_cancel(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_bytes(b'\r')      # ENTER

        app = deleter(user_data, 0, view)
        result = app.run()
        assert result == (view, 0)


class TestView:

    def test_call_deleter(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_text('d')

        app = view(user_data, 1)
        result = app.run()
        assert result == (deleter, 1)

    def test_call_gallery(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_text('b')

        app = view(user_data, 0)
        result = app.run()
        assert result == (gallery, None)

    def test_call_factory(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_text('l')

        app = view(user_data, 2)
        result = app.run()
        assert result == (factory, 2)

    def test_call_editor(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_text('x')

        app = view(user_data, 2)
        result = app.run()
        assert result == (editor, 2)

    def test_call_view_prev_note(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        note_num = 1
        ff = view
        # iterating in a circle (start:1 -> end:1)
        for iteration, _ in enumerate(user_data.history, 1):
            mock_input.send_text('p')         # Left
            app = ff(user_data, note_num)
            ff, note_num = app.run()
        assert (ff, note_num) == (view, 1)

    def test_call_view_next_note(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        note_num = 1
        ff = view
        # iterating in a circle (start:1 -> end:1)
        for iteration, _ in enumerate(user_data.history, 1):
            mock_input.send_text('n')         # RIGHT
            app = ff(user_data, note_num)
            ff, note_num = app.run()
        assert (ff, note_num) == (view, 1)


class TestEditor:

    def test_exit_with_save(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        # prepare data
        note = 'test note'
        user_data.history.append(note)
        user_data.notes[note] = ''

        line1 = 'test line1'
        line2 = 'test line2'
        mock_input.send_text(line1)
        mock_input.send_bytes(b'\r')     # ENTER for multiline input
        mock_input.send_text(line2)
        mock_input.send_bytes(b'\x13')   # Ctrl-S

        app = editor(user_data, -1)
        result = app.run()
        assert result == (view, -1)
        assert user_data.notes[note] == line1 + '\n' + line2

    def test_exit_with_cancel(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        notes_before = user_data.notes.copy()
        mock_input.send_bytes(b'\x1b')   # ESC

        app = editor(user_data, 0)
        result = app.run()
        assert result == (view, 0)
        assert notes_before == user_data.notes

    def test_copy_paste_selection_text(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        first_line_text = user_data.notes[user_data.history[0]].split('\n')[0]

        exit_key = KeyBindings()

        @exit_key.add('c-d')
        def exit_with_result(event) -> None:
            event.app.exit(result=event.current_buffer.text)

        mock_input.send_bytes(b'\x1b[1;2F')   # Shift-End to select the first line
        mock_input.send_bytes(b'\x03')        # Ctrl-C
        mock_input.send_bytes(b'\x16')        # Ctrl-V
        mock_input.send_bytes(b'\x04')        # Ctrl-D

        app = editor(user_data, 0)
        app.key_bindings = merge_key_bindings([app.key_bindings, exit_key])
        result = app.run()
        assert result == 2*first_line_text


class Testfactory:

    def test_cancel(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        mock_input.send_bytes(b'\x09')         # Tab
        mock_input.send_bytes(b'\r')           # ENTER

        app = factory(user_data, 0, view)
        result = app.run()
        assert result == (view, 0)

    def test_edit_note_title(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        new_note_title = 'new title'

        mock_input.send_bytes(b'\x1b[1;2F')    # Shift-End to select the first line
        mock_input.send_text(new_note_title)
        mock_input.send_bytes(b'\r')           # ENTER

        app = factory(user_data, 0, view)
        result = app.run()
        assert result == (view, 0)
        assert new_note_title == user_data.history[0]

    def test_create_new_note(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        note_title = 'note title'
        num_note = len(user_data.history)

        mock_input.send_text(note_title)
        mock_input.send_bytes(b'\r')           # ENTER

        app = factory(user_data, num_note, gallery)
        result = app.run()
        assert result == (editor, num_note)
        assert user_data.history[num_note] == note_title

    def test_copy_paste_selection_text(self, user_data: UserData, mock_input: PosixPipeInput) -> None:
        note_title = user_data.history[0]

        exit_key = KeyBindings()

        @exit_key.add('c-d')
        def exit_with_result(event) -> None:
            event.app.exit(result=event.current_buffer.text)

        mock_input.send_bytes(b'\x1b[1;2F')    # Shift-End to select the first line
        mock_input.send_bytes(b'\x03')         # Ctrl-C
        mock_input.send_bytes(b'\x16')         # Ctrl-V
        mock_input.send_bytes(b'\x04')         # Ctrl-D

        app = factory(user_data, 0, view)
        app.key_bindings = merge_key_bindings([app.key_bindings, exit_key])
        result = app.run()
        assert result == 2*note_title
