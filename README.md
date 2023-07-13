# My-notes

## Description

A simple CLI app in Python3 for taking notes. The core functionality is based on the      [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) library

### Available note operations

- create/save
- update/edit
- delete
- view content
    1. by titles in the notes gallery
    2. in a specific note in full

### Interface Features

- operations in the application are performed using hotkeys
- there is mouse cursor support in some parts of the app
- note text editing is fairly rudimentary. Supports some of your shell commands + Ctrl-C and Ctrl-V for copy and paste, as well as multi-line input.
- created some strict rules for naming notes

### Сonstraints

- The app is designed for one user
- Notes are stored in a .pickle file

## Overview

Empty gallery
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/1_gallery_empty.png)

Creating a note
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/6_create.png)

One example of validation
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/7_create_with_validation.png)

Gallery
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/2_gallery.png)

Viewing the contents of a note
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/3_view.png)

Editing a note
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/4_edit.png)

Deleting a note
![ ](https://raw.githubusercontent.com/Mas5ive/My_notes/main/presentation/5_delete.png)

## Installation and run

```bash
git clone https://github.com/Mas5ive/My_notes
cd My_notes/
```

### Using Poetry + Make

Install:

```bash
make install
```

Run:

```bash
make mynotes
```

### Using Poetry

Install:

```bash
poetry install
```

Run:

```bash
poetry run mynotes
```

### Using Pip (+Make)

- сreate a virtual environment
- activate it
- and run the command:

```bash
pip install -r requirements.txt
```

or

```bash
make install-pip
```

and run

```bash
python -m application.scripts.run
```

or

```bash
make mynotes
```
