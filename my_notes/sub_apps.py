from data.user import UserData
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import (
    HorizontalAlign,
    HSplit,
    VerticalAlign,
    VSplit,
    Window,
    WindowAlign,
)


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
    pass


def deleter(data: UserData, note_num: int) -> Application:
    pass


def factory(data: UserData, note_num: int) -> Application:
    pass


def gallary(data: UserData, *args) -> Application:
    pass


if __name__ == '__main__':
    test_data = UserData()
    test_data.history = ['first', 'second', 'third']
    test_data.notes = {
        'first': 'qqqqqqqqqqqqqqq qqqqqqqqqqqq qqqqqqqqq q qqqqqqqqqqq qqqqqqq qqqq qqqqqqqq',
        'second': 'wwwwwwww w wwwww www wwwwwww wwwww wwwww wwwwww wwwww wwwwwwww ww www w w',
        'third': 'eeee eee eeeeeee ee e eeeeee eeeee eeeeeeeeeeee eee eee e ee eeeeee eee ee'
    }

    res_func, res_num = view(test_data, 0).run()
    while res_func == view:
        res_func, res_num = res_func(test_data, res_num).run()
