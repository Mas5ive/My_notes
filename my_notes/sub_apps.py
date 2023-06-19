from prompt_toolkit.document import Document
from data.user import UserData
from typing import Callable
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import (
    TextArea,
    Button,
    Dialog,
    Label,
    ValidationToolbar,
)
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import (
    HorizontalAlign,
    HSplit,
    VerticalAlign,
    VSplit,
    Window,
    WindowAlign,
)


def gallary(data: UserData, *args) -> Application:
    pass


def view(data: UserData, note_num: int) -> Application:
    body = HSplit(
        [
            Window(
                FormattedTextControl(f'#{note_num} ' + data.history[note_num]),
                height=2,
                align=WindowAlign.CENTER,
                # style="bg:#88ff88 #000000",
            ),
            Window(
                FormattedTextControl(data.notes[data.history[note_num]]),
                height=2,
                align=WindowAlign.CENTER,
                # style="bg:#88ff88 #000000",
            ),
            VSplit(
                [
                    Window(
                        FormattedTextControl('Edit teXt / titLe'),
                        height=2,
                        align=WindowAlign.LEFT,
                        # style=
                    ),
                    Window(
                        FormattedTextControl('<- previous  next ->'.ljust(25, ' ')),
                        height=2,
                        align=WindowAlign.CENTER,
                        # style=
                    ),
                    Window(
                        FormattedTextControl('Back  Delete'),
                        height=2,
                        align=WindowAlign.RIGHT,
                        # style=
                    )
                ]
            )
        ]
    )

    next_note_num = note_num+1 if note_num != len(data.history)-1 else 0
    prev_note_num = note_num-1 if note_num != 0 else len(data.history)-1

    kb = KeyBindings()

    @ kb.add("left")
    def view_prev_note(event):
        event.app.exit(result=(view, prev_note_num))

    @ kb.add("right")
    def view_next_note(event):
        event.app.exit(result=(view, next_note_num))

    @ kb.add("b")
    def call_gallery(event):
        event.app.exit(result=(gallary, None))

    @ kb.add("x")
    def call_editor(event):
        event.app.exit(result=(editor, note_num))

    @ kb.add("l")
    def call_factory(event):
        event.app.exit(result=(factory, note_num))

    @ kb.add("d")
    def call_deleter(event):
        event.app.exit(result=(deleter, note_num))

    return Application(
        layout=Layout(body),
        full_screen=True,
        key_bindings=kb
    )


def editor(data: UserData, note_num: int) -> Application:
    text_area = TextArea(
        text=data.notes[data.history[note_num]],
        multiline=True,
        focus_on_click=True
    )

    body = HSplit(
        [
            Window(
                FormattedTextControl(f'#{note_num} ' + data.history[note_num]),
                height=2,
                align=WindowAlign.CENTER,
                # style="bg:#88ff88 #000000",
            ),
            text_area,
            VSplit(
                [
                    Window(
                        FormattedTextControl('Enter Ctrl+S to save'),
                        height=2,
                        align=WindowAlign.LEFT,
                        # style=
                    ),
                    Window(
                        FormattedTextControl('Enter ESC to cancel'),
                        height=2,
                        align=WindowAlign.RIGHT,
                        # style=
                    )
                ]
            )
        ]
    )

    kb = KeyBindings()

    @ kb.add("c-s")
    def exit_with_save(event):
        data.notes[data.history[note_num]] = text_area.text
        event.app.exit(result=(view, note_num))

    @ kb.add("escape")
    def exit_with_cancel(event):
        event.app.exit(result=(view, note_num))

    @kb.add("c-c", eager=True)
    def copy_selection_text(event):
        selection = event.current_buffer.copy_selection()
        event.app.clipboard.set_data(selection)

    @kb.add("c-v", eager=True)
    def paste_buffer_text(event):
        buffer = event.app.clipboard.get_data()
        event.current_buffer.paste_clipboard_data(buffer)

    return Application(
        layout=Layout(body),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True
    )


def deleter(data: UserData, note_num: int, calling_sub_app: Callable) -> Application:

    def ok_handler() -> None:
        deleted_note = data.history.pop(note_num)
        data.notes.pop(deleted_note)
        if not data.history:
            result = (gallary, None)
        else:
            result = (calling_sub_app, note_num if note_num == 0 else note_num-1)
        get_app().exit(result=result)

    def cancel_handler() -> None:
        get_app().exit(result=(calling_sub_app, note_num))

    ok_button = Button(text='OK', handler=ok_handler)
    cancel_button = Button(text='Cancel', handler=cancel_handler)

    dialog = Dialog(
        title=f'#{note_num} ' + data.history[note_num],
        body=HSplit(
            [
                Label(
                    text='Do you really want to delete this note?',
                    # dont_extend_height=True,
                    align=WindowAlign.CENTER
                ),
            ],
            padding=Dimension(preferred=1, max=1),
        ),
        buttons=[cancel_button, ok_button],
        with_background=True,
    )

    return Application(
        layout=Layout(dialog),
        full_screen=True,
        mouse_support=True
    )


def factory(data: UserData, note_num: int, calling_sub_app: Callable) -> Application:

    class FactoryValidator(Validator):
        def validate(self, document: Document) -> None:
            text = document.text

            conditions = {
                'The title of the note must be unique!': lambda: text in data.notes,
                'The title of the note cannot be empty!': lambda: len(text) == 0,
                f'The title of the note should be more succinct (up to 62 characters, now {len(text)})':
                    lambda: 62 < len(text)
            }
            for massage, condition in conditions.items():
                if condition():
                    raise ValidationError(message=massage, cursor_position=len(text))

    def accept_handler(buffer: Buffer) -> None:
        note_title = buffer.text

        if calling_sub_app == gallary:
            data.history.append(note_title)
            data.notes[note_title] = ''
            result = (editor, note_num)
        else:
            text_note = data.notes.pop(data.history[note_num])
            data.notes[note_title] = text_note
            data.history[note_num] = note_title
            result = (calling_sub_app, note_num)
        get_app().exit(result=result)

    def cancel_handler() -> None:
        get_app().exit(result=(calling_sub_app, note_num))

    cancel_button = Button(text='Cancel', handler=cancel_handler)

    text_area = TextArea(
        text='' if calling_sub_app == gallary else data.history[note_num],
        multiline=False,
        focus_on_click=True,
        validator=FactoryValidator(),
        accept_handler=accept_handler
    )

    dialog = Dialog(
        title='Enter a note title',
        body=HSplit(
            [
                text_area,
                ValidationToolbar(),
            ],
            padding=Dimension(preferred=1, max=1),
        ),
        buttons=[cancel_button],
        with_background=True,
    )

    kb = KeyBindings()

    @kb.add("c-c", eager=True)
    def copy_selection_text(event):
        selection = event.current_buffer.copy_selection()
        event.app.clipboard.set_data(selection)

    @kb.add("c-v", eager=True)
    def paste_buffer_text(event):
        buffer = event.app.clipboard.get_data()
        event.current_buffer.paste_clipboard_data(buffer)

    return Application(
        layout=Layout(dialog),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True
    )


if __name__ == '__main__':
    test_data = UserData()
    test_data.history = [
        'first',
        'second',
        'third'
    ]
    test_data.notes = {
        'first': 'qqqqqqqqqqqqqqq qqqqqqqqqqqq qqqqqqqqq q qqqqqqqqqqq qqqqqqq qqqq qqqqqqqq',
        'second': 'wwwwwwww w wwwww www wwwwwww wwwww wwwww wwwwww wwwww wwwwwwww ww www w w',
        'third': 'eeee eee eeeeeee ee e eeeeee eeeee eeeeeeeeeeee eee eee e ee eeeeee eee ee'
    }

    res_func = factory(test_data, 0, view).run()
    print(test_data.history)
    print(test_data.notes)
    print(res_func)
