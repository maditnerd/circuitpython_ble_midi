import time
import board

# Midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

# BLE Midi
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import adafruit_ble_midi

# MPR 121
import adafruit_mpr121

midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)
midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)
ble = adafruit_ble.BLERadio()

note = ["C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A4","A#4","B4"]
i2c = board.I2C()
mpr121 = adafruit_mpr121.MPR121(i2c, 90)
cap = [False,False,False,False,False,False,False,False,False,False,False,False]

print("Advertising BLE")
ble.start_advertising(advertisement)

while True:
    print("Waiting for connection")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:

        for i in range(12):
            if mpr121[i].value:
                if cap[i] == False:
                    cap[i] = True
                    midi.send(NoteOn(note[i], 127))
                    print(str(i) + " - " + note[i] + " - ON")
            else:
                if cap[i] == True:
                    cap[i] = False
                    midi.send(NoteOff(note[i], 127))
                    print(str(i) + " - " + note[i] + " - OFF")

    print("Disconnected")
    print("Advertising BLE")
    ble.start_advertising(advertisement)
