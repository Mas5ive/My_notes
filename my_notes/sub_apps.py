"""
    Factory functions that create Application instances (from the prompt-toolkit library) with unique features.
    They represent application windows containing certain functionality.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.layout import Layout, Dimension
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import (
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Frame,
    Label,
    RadioList,
    TextArea,
    ValidationToolbar,
)
from typing import Callable
from data.user import UserData


def gallery(data: UserData, *args) -> Application:
    """
    The function sets up a gallery user interface for the app.
    If the user history is empty, a message is displayed with options to create a note or exit.
    If the history is not empty, a list of notes is displayed with options to view, delete, create or exit.

    Key bindings are set for different actions such as view, delete, create and exit.

    Arguments:
        data: an instance of the UserData class containing user data.
        *args: arguments that are not handled in any way

    Returns:
        Application: an instance of the Application class with unique Gallery sub-app settings.
    """

    kb = KeyBindings()

    if not data.history:
        body = HSplit(
            [
                Window(
                    FormattedTextControl('Your gallery is empty\nIt`s time to fill it up!'),
                    height=2,
                    align=WindowAlign.CENTER,
                ),
                Window(
                    FormattedTextControl(HTML('<b><u>C</u></b>reate | <b><u>E</u></b>xit')),
                    height=2,
                    align=WindowAlign.CENTER,
                ),
            ],
            padding_char='-',
            padding=1,
        )
    else:
        body = HSplit(
            [
                VSplit(
                    [
                        note_list := RadioList([(idx, note) for idx, note in enumerate(data.history)]),
                        Window(
                            FormattedTextControl(HTML(
                                '<DarkGray> Use the keys to move:</DarkGray>\n'
                                'Up, Down, Page Up/Down')),
                            height=2,
                            align=WindowAlign.CENTER,
                        ),
                    ]
                ),
                VSplit(
                    [
                        Window(
                            FormattedTextControl(HTML('<b>Enter</b> or <b>click</b> to select')),
                            height=2,
                            align=WindowAlign.LEFT,
                        ),
                        Window(
                            FormattedTextControl(HTML('<b><u>V</u></b>iew | <b><u>D</u></b>elete')),
                            height=2,
                            align=WindowAlign.CENTER,
                        ),
                        Window(
                            FormattedTextControl(HTML('<b><u>C</u></b>reate | <b><u>E</u></b>xit')),
                            height=2,
                            align=WindowAlign.RIGHT,
                        )
                    ]
                )
            ],
            padding_char='-', padding=1,
        )

        @ kb.add("v")
        def call_view(event) -> None:
            event.app.exit(result=(view, note_list.current_value))

        @ kb.add("d")
        def call_deleter(event) -> None:
            event.app.exit(result=(deleter, note_list.current_value))

    @ kb.add("c")
    def call_factory(event) -> None:
        event.app.exit(result=(factory, len(data.history)))

    @ kb.add("e")
    def exit(event) -> None:
        event.app.exit(result=(None, 0))

    custom_style = Style.from_dict({
        'dialog': 'bg:#DEB887',
        'dialog.body': 'bg:#FFDEAD #562800',
        'dialog frame.label': 'fg:#FFDEAD bg:#562800',
    })

    return Application(
        layout=Layout(Dialog(title='NOTES', body=body, with_background=True)),
        full_screen=True,
        mouse_support=True,
        key_bindings=kb,
        style=custom_style
    )


def view(data: UserData, note_num: int, *args) -> Application:
    """
    The function sets up an user interface for viewing a specific note.
    It displays the note's title and content along with options to edit, navigate to previous or next notes,
    go back to the Gallery, or delete the note.

    Key bindings are set up for different actions, such as navigating, editing, creating, and deleting.

    Arguments:
        data: an instance of the UserData class containing user data.
        note_num: the index of the note to view.
        *args: arguments that are not handled in any way.

    Returns:
        Application: an instance of the Application class with unique View sub-app settings.
    """

    body = HSplit(
        [
            Frame(
                Window(
                    FormattedTextControl(f'#{note_num+1} ' + data.history[note_num]),
                    height=1,
                    align=WindowAlign.CENTER,
                ),
                style='class:window bold',
            ),
            VSplit(
                [
                    TextArea(
                        text=data.notes[data.history[note_num]],
                        focus_on_click=True,
                        read_only=True,
                        wrap_lines=False,
                        width=Dimension(min=55),
                        height=Dimension(min=5),
                    )
                ],
                style='class:textarea'
            ),
            VSplit(
                [
                    Window(
                        FormattedTextControl(
                            HTML('  Edit te<b><u>X</u></b>t / tit<b><u>L</u></b>e')
                        ),
                        width=Dimension(min=20),
                        ignore_content_width=True,
                        height=2,
                        align=WindowAlign.LEFT,
                        style='class:window'
                    ),
                    Window(
                        FormattedTextControl(
                            HTML('<b><u>P</u></b>revious | <b><u>N</u></b>ext     ')
                        ),
                        width=Dimension(min=20),
                        ignore_content_width=True,
                        height=2,
                        align=WindowAlign.CENTER,
                        style='class:window'
                    ),
                    Window(
                        FormattedTextControl(
                            HTML('<b><u>B</u></b>ack  <b><u>D</u></b>elete  ')
                        ),
                        width=Dimension(min=15),
                        ignore_content_width=True,
                        height=2,
                        align=WindowAlign.RIGHT,
                        style='class:window'
                    )
                ]
            )
        ]
    )

    next_note_num = note_num+1 if note_num != len(data.history)-1 else 0
    prev_note_num = note_num-1 if note_num != 0 else len(data.history)-1

    kb = KeyBindings()

    @ kb.add("p")
    def view_prev_note(event) -> None:
        event.app.exit(result=(view, prev_note_num))

    @ kb.add("n")
    def view_next_note(event) -> None:
        event.app.exit(result=(view, next_note_num))

    @ kb.add("b")
    def call_gallery(event) -> None:
        event.app.exit(result=(gallery, None))

    @ kb.add("x")
    def call_editor(event) -> None:
        event.app.exit(result=(editor, note_num))

    @ kb.add("l")
    def call_factory(event) -> None:
        event.app.exit(result=(factory, note_num))

    @ kb.add("d")
    def call_deleter(event) -> None:
        event.app.exit(result=(deleter, note_num))

    custom_style = Style.from_dict({
        'window': 'bg:#FFDEAD #562800',
        'textarea': 'bg:#DEB887 #562800'
    })

    return Application(
        layout=Layout(body),
        full_screen=True,
        mouse_support=True,
        key_bindings=kb,
        style=custom_style
    )


def editor(data: UserData, note_num: int, *args) -> Application:
    """
    The function sets up an user interface for editing a specific note.
    It displays the note's title and provides a text area for editing the note's content.
    Options to save the changes and exit or cancel the editing process are included.

    Key bindings are set up for different actions, such as saving, canceling, copying, and pasting.

    Arguments:
        data: an instance of the UserData class containing user data.
        note_num: the index of the note to view.
        *args: arguments that are not handled in any way.

    Returns:
        Application: an instance of the Application class with unique Editor sub-app settings.
    """

    body = HSplit(
        [
            Frame(
                Window(
                    FormattedTextControl(f'#{note_num+1} ' + data.history[note_num]),
                    height=1,
                    align=WindowAlign.CENTER,
                ),
                style="class:window bold",
            ),
            VSplit(
                [
                    text_area := TextArea(
                        text=data.notes[data.history[note_num]],
                        multiline=True,
                        wrap_lines=False,
                        focus_on_click=True,
                        width=Dimension(min=55),
                        height=Dimension(min=5),
                        style='class:textarea'
                    )
                ]
            ),
            VSplit(
                [
                    Window(
                        FormattedTextControl(
                            HTML('  Enter <b>Ctrl+S</b> to save')
                        ),
                        height=2,
                        width=Dimension(min=28),
                        align=WindowAlign.LEFT,
                        style='class:window'
                    ),
                    Window(
                        FormattedTextControl(
                            HTML('Enter <b>ESC</b> to cancel  ')
                        ),
                        height=2,
                        width=Dimension(min=27),
                        align=WindowAlign.RIGHT,
                        style='class:window'
                    )
                ]
            )
        ]
    )

    kb = KeyBindings()

    @ kb.add("c-s")
    def exit_with_save(event) -> None:
        data.notes[data.history[note_num]] = text_area.text
        event.app.exit(result=(view, note_num))

    @ kb.add("escape")
    def exit_with_cancel(event) -> None:
        event.app.exit(result=(view, note_num))

    @ kb.add("c-c", eager=True)
    def copy_selection_text(event) -> None:
        selection = event.current_buffer.copy_selection()
        event.app.clipboard.set_data(selection)

    @ kb.add("c-v", eager=True)
    def paste_buffer_text(event) -> None:
        buffer = event.app.clipboard.get_data()
        event.current_buffer.paste_clipboard_data(buffer)

    custom_style = Style.from_dict({
        'window': 'bg:#A0522D #FFDEAD',
        'textarea': 'bg:#DEB887 #562800'
    })

    return Application(
        layout=Layout(body),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True,
        style=custom_style
    )


def deleter(data: UserData, note_num: int, calling_sub_app: Callable[..., Application]) -> Application:
    """
    The function sets up an user interface for confirming the deletion of a specific note.
    It displays a dialog with the note's title and a message asking the user to confirm the deletion.
    Two buttons, "OK" and "Cancel," are provided to handle the user's choice.

    The function defines handlers for the button actions, including removing the note from the data,
    and exiting the app.

    Arguments:
        data: an instance of the UserData class containing user data.
        note_num: the index of the note to delete.
        calling_sub_app: the previous sub-app that initiated the call.

    Returns:
        Application: an instance of the Application class with unique Deleter sub-app settings.
    """

    def ok_handler() -> None:
        deleted_note = data.history.pop(note_num)
        data.notes.pop(deleted_note)
        if not data.history:
            result = (gallery, None)
        else:
            result = (calling_sub_app, note_num if note_num == 0 else note_num-1)
        get_app().exit(result=result)

    def cancel_handler() -> None:
        get_app().exit(result=(calling_sub_app, note_num))

    ok_button = Button(text='OK', handler=ok_handler)
    cancel_button = Button(text='Cancel', handler=cancel_handler)

    dialog = Dialog(
        title=f'#{note_num+1} ' + data.history[note_num],
        body=HSplit(
            [
                Label(
                    text='Do you really want to delete this note?',
                    align=WindowAlign.CENTER
                ),
            ],
            padding=Dimension(preferred=1, max=1),
        ),
        buttons=[cancel_button, ok_button],
        with_background=True,
    )

    custom_style = Style.from_dict({
        "dialog": "bg:#390606",
        'dialog shadow': 'bg:#000000',
        "dialog.body": "bg:#FFDEAD #7d0000",
        'dialog frame.label': 'fg:#FFDEAD bg:#e70606',
    })

    return Application(
        layout=Layout(dialog),
        full_screen=True,
        mouse_support=True,
        style=custom_style
    )


def factory(data: UserData, note_num: int, calling_sub_app: Callable[..., Application]) -> Application:
    """
    The function sets up an user interface for creating or editing a note title (if one already exists).
    It displays a dialog box with an input field for the title of the note.

    The function defines a custom validator, an accept handler and a cancel handler.
    Key bindings are set for copying and pasting text.

    Arguments:
        data: an instance of the UserData class containing user data.
        note_num: the index of the note to delete.
        calling_sub_app: the previous sub-app that initiated the call.

    Returns:
        Application: an instance of the Application class with unique Factory sub-app settings.
    """

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

        if calling_sub_app == gallery:
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

    dialog = Dialog(
        title='Enter a note title',
        body=HSplit(
            [
                TextArea(
                    text='' if calling_sub_app == gallery else data.history[note_num],
                    multiline=False,
                    focus_on_click=True,
                    validator=FactoryValidator(),
                    accept_handler=accept_handler
                ),
                ValidationToolbar(),
            ],
            padding=Dimension(preferred=1, max=1),
        ),
        buttons=[cancel_button],
        with_background=True,
    )

    kb = KeyBindings()

    @ kb.add("c-c", eager=True)
    def copy_selection_text(event) -> None:
        selection = event.current_buffer.copy_selection()
        event.app.clipboard.set_data(selection)

    @ kb.add("c-v", eager=True)
    def paste_buffer_text(event) -> None:
        buffer = event.app.clipboard.get_data()
        event.current_buffer.paste_clipboard_data(buffer)

    custom_style = Style.from_dict({
        'dialog': 'bg:#DEB887',
        'dialog shadow': 'bg:#000000',
        'dialog.body': 'bg:#FFDEAD #562800',
        'dialog frame.label': 'fg:#FFDEAD bg:#562800',
    })

    return Application(
        layout=Layout(dialog),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True,
        style=custom_style
    )
