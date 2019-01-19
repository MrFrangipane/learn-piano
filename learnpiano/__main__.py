import os
from PySide.QtGui import QApplication, QSound, QWidget
import mido

PATH = "E:/PROJETS/dev/learn-piano/audio/sample-conform"
if os.environ.get('LP_SAMPLES_PATH', False):
    PATH = os.environ['LP_SAMPLES_PATH']


NOTES = {
    48: 'Piano.ff.C3.wav',
    49: 'Piano.ff.Db3.wav',
    50: 'Piano.ff.D3.wav',
    51: 'Piano.ff.Eb3.wav',
    52: 'Piano.ff.E3.wav',
    53: 'Piano.ff.F3.wav',
    54: 'Piano.ff.Gb3.wav',
    55: 'Piano.ff.G3.wav',
    56: 'Piano.ff.Ab3.wav',
    57: 'Piano.ff.A3.wav',
    58: 'Piano.ff.Bb3.wav',
    59: 'Piano.ff.B3.wav',
    60: 'Piano.ff.C4.wav',
    61: 'Piano.ff.Db4.wav',
    62: 'Piano.ff.D4.wav',
    63: 'Piano.ff.Eb4.wav',
    64: 'Piano.ff.E4.wav',
    65: 'Piano.ff.F4.wav',
    66: 'Piano.ff.Gb4.wav',
    67: 'Piano.ff.G4.wav',
    68: 'Piano.ff.Ab4.wav',
    69: 'Piano.ff.A4.wav',
    70: 'Piano.ff.Bb4.wav',
    71: 'Piano.ff.B4.wav'
}


def open_port(name):
    port_names = mido.get_input_names()
    print 'Ports:\n' + '\n'.join(port_names)

    for port_name in port_names:
        if name.lower() in port_name.lower():
            print '-> opening ' + port_name
            return mido.open_input(port_name)
    raise RuntimeError('No midi port found : {}'.format(name))


def note_on(port):
    print 'Waiting for MIDI message'
    message = port.receive()
    print '\t' + str(message)
    while message.type != 'note_on':
        message = port.receive()
    return message


class Dummy(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        sounds = dict()
        for note_id, filename in NOTES.items():
            filepath = PATH + '/' + filename
            sounds[note_id] = QSound(filepath)

        with open_port('XBoard25') as port_in:
            message = note_on(port_in)

            while message.note != 72:
                if message.velocity > 0:
                    sounds[message.note].play()

                message = note_on(port_in)

        print "Exiting"
        import sys
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication([])
    widget = Dummy()
    app.exec_()
