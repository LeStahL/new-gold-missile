import mido, argparse

parser = argparse.ArgumentParser(description='Team210 midi file to shader conversion tool.')
parser.add_argument('-o', '--output', dest='out')
args, rest = parser.parse_known_args()

if rest == []:
    print('No input file present. Can not do anything.')
    exit()

if args.out == None:
    print('No output specified. Will exit.')
    exit()

def noteToFreq(note):
    return (440. / 32.) * (2. ** ((note - 9.) / 12.))

midiFile = mido.MidiFile(rest[0])
midiMessages = []
channelNumbers = {}
for midiMessage in midiFile:
    if 'note_on' in str(midiMessage) or 'note_off' in str(midiMessage):
        midiMessages.append(midiMessage)
        channelNumbers[midiMessage.channel] = True
channelNumbers = list(set(channelNumbers.keys()))
on_times = []
on_separators = []
off_times = []
off_separators = []
for channelNumber in channelNumbers:
    midiTicks = 0
    midiTempo = 0.
    for midiMessage in midiMessages:
        if midiMessage.channel == channelNumber:
            if midiMessage.type == 'note_on':
                on_times += [mido.tick2second(midiTicks, midiFile.ticks_per_beat, midiTempo)]
            elif midiMessage.type == 'note_off':
                off_times += [mido.tick2second(midiTicks, midiFile.ticks_per_beat, midiTempo)]
            elif midiMessage.type == 'set_tempo':
                midiTempo = midiMessage.tempo
            midiTicks += midiMessage.time
            print(midiTicks)
    on_separators += [len(on_times)]
    off_separators += [len(off_times)]
print(on_times)
print(on_separators)
print(off_times)
print(off_separators)