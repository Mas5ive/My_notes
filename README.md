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

- there is mouse cursor support in some parts of the app
- note text editing is fairly rudimentary. Supports some of your shell commands + Ctrl-C and Ctrl-V for copy and paste, as well as multi-line input.
- created some strict rules for naming notes

### Сonstraints

- The app is designed for one user
- Notes are stored in a .pickle file

## Overview

...

## Installation and run

```bash
git clone https://github.com/Mas5ive/My-notes
cd My-notes/
```

### Using **Poetry** + Make

Install:

```bash
make install
```

Run:

```bash
make mynotes
```

### Using **Poetry**

Install:

```bash
poetry install
```

Run:

```bash
poetry run mynotes
```

### Using **Pip** (+Make)

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
