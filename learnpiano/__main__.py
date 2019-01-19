import os
import pygame
from PySide.QtGui import QApplication, QWidget
import mido


EXIT_NOTE_NUMBER = 71
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


def find_samples_folder():
    if os.environ.get('LP_SAMPLES_PATH', False):
        return os.environ['LP_SAMPLES_PATH']

    print __file__

    installation_folder = os.path.dirname(os.path.dirname(__file__)) + '/audio/sample-conform'
    if os.path.isdir(installation_folder):
        return installation_folder

    installation_folder = os.path.dirname(__file__) + '/audio/sample-conform'
    if os.path.isdir(installation_folder):
        return installation_folder


def midi_port_open(name):
    port_names = mido.get_input_names()
    print 'MIDI Ports:\n' + '\n'.join(['- ' + name_ for name_ in port_names])

    for port_name in port_names:
        if name.lower() in port_name.lower():
            print '-> opening ' + port_name
            return mido.open_input(port_name)

    raise RuntimeError('No midi port found : {}'.format(name))


def midi_recieve(port):
    message = port.receive()
    # print '\t' + str(message)
    return message


def poll_note_on(port):
    # print 'Waiting for MIDI note on'
    message = midi_recieve(port)

    while message.type != 'note_on':
        message = midi_recieve(port)
    return message


def load_samples():
    samples = dict()
    samples_folder = find_samples_folder()

    for note_id, filename in NOTES.items():
        filepath = samples_folder + '/' + filename

        if not os.path.isfile(filepath):
            raise RuntimeError('Sample not found : ' + filepath)

        samples[note_id] = pygame.mixer.Sound(filepath)

    return samples


def audio_init():
    print 'Init audio ...'
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    while pygame.mixer.get_init() is None:
        pass


def audio_close():
    pygame.mixer.quit()


class Dummy(QWidget):
    def __init__(self, midi_port, parent=None):
        QWidget.__init__(self, parent)

        self.samples = load_samples()

        with midi_port_open(midi_port) as port_in:
            message = poll_note_on(port_in)

            while message.note != EXIT_NOTE_NUMBER:
                if message.velocity > 0:
                    self.samples[message.note].play()

                message = poll_note_on(port_in)

        print "Exiting"
        import sys
        sys.exit(0)


if __name__ == '__main__':
    audio_init()

    app = QApplication([])
    widget = Dummy(midi_port='XBoard25')
    widget.show()
    app.exec_()

    audio_close()
