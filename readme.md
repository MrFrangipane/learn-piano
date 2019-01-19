# Learn Piano

Spaced repetition, MIDI-based, piano training program

## Installation

- Install `python-pyside`, `libasound-dev`, `jackd` and `libjack-dev` in order to be able to install `python-rtmidi`

- Create a virtualenv

```bash
virtualenv venv-learnpiano --system-site-packages
cd venv-learnpiano/bin
./python -m pip install git+http://github.com/MrFrangipane/learn-piano.git
```

## Execution

```bash
venv-learnpiano/bin/python -m learnpiano
```

---

Piano samples are based on : http://theremin.music.uiowa.edu/MISpiano.html
