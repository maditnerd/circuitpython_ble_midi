import time
import array
import math
import board
from simpleio import map_range

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

# Proximity Sensor
import adafruit_apds9960.apds9960

# MPR 121
import adafruit_mpr121

PITCHBEND_IS = False
midi_note_array = []
i2c = board.I2C()
apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
apds9960.enable_proximity = True

midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)
midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)
ble = adafruit_ble.BLERadio()

print("Advertising BLE")
ble.start_advertising(advertisement)

note = ["C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A4","A#4","B4"]
mpr121 = adafruit_mpr121.MPR121(i2c, 90)
cap = [False,False,False,False,False,False,False,False,False,False,False,False]

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

        proximity = apds9960.proximity               
        if proximity != 0:
            pitch_bend = int(map_range(proximity, 0, 250, 0, 8191))
            print("PITCH:" + str(pitch_bend))
            midi.send(PitchBend(pitch_bend))
            if PITCHBEND_IS is False:
                PITCHBEND_IS = True
        else:
            if PITCHBEND_IS is True:
                PITCHBEND_IS = False
                midi.send(PitchBend(0))
    print("Disconnected")
    print("Advertising BLE")
    ble.start_advertising(advertisement)
