import time
import board
import busio
import os
import mido
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo




# Map MIDI note numbers to note names
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def get_midi_files(directory):
	files_in_directory = os.listdir(directory)
	midi_files = {file for file in files_in_directory if file.endswith('.midi') or file.endswith('.mid')}
	return midi_files
	
def poll():
	curr_dir = os.getcwd()
	prev = get_midi_files(curr_dir) 
	
	while True:
		curr = get_midi_files(curr_dir)			
		new_files = curr - prev
		if new_files:
			for file in new_files:
				print(f'{file} created')
				notes_and_durations = parse_midi(file)
				return notes_and_durations

			
		prev = curr
		
		time.sleep(0.5)
		
def play_note(servo, play_time, rest_time):
    servo.angle = 60
    time.sleep(0.2)
    servo.angle = 150
    time.sleep(play_time)
    servo.angle = 0

#This is where we find whichever finger this note should be corresponding to
def find_servo(key):
    #do like key - leftmost_key to find the finger it should be
    servo = fingers[notemapping[key]]
    return servo
	

def process_note(note):
	#note is a tuple containing the key, playTime, and rest time data
	key, play_time = note
	play_time = int(play_time * 0.8)
	if key in notemapping:
	    print(key)
	    servo = find_servo(key)
	    #here we need to determine which servo to play and for how long
	    move_servo(servo, play_time)

# Function to move a servo from 0 to 180 and back to 0
def move_servo(servo, play_time):
    # Move from 0 to 180 degrees
    servo.angle = 60
    time.sleep(play_time / 1000)
    servo.angle = 0
    
def servo_chord_start(servo1,servo2,servo3):
    # Move from 0 to 180 degrees
    time.sleep(1)
    servo2.angle = 135
    servo1.angle = 135
    servo3.angle = 135
def servo_chord_end(servo1,servo2,servo3):
    # Move from 0 to 180 degrees
    time.sleep(1) 
    servo2.angle = 90
    servo1.angle = 90
    servo3.angle = 90
def play_chord(s1, s2, s3):
    servo_chord_start(s1,s2,s3)
    servo_chord_end(s1,s2,s3)

# Continuously cycle servos one after the other
#try:
 #   while True:
  #      for i in servo_order:
            #servo_chord_start(servos[0], servos[1], servos[6])
            #servo_chord_end(servos[0], servos[1], servos[6])
   #         move_servo(servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500))
    #        time.sleep(servo_delay)  # Delay between moving each servo

#loop through music array data
		
def get_note_name(midi_note):
    """Convert MIDI note number to note name with octave."""
    note = NOTE_NAMES[midi_note % 12]  # Find the note name
    octave = (midi_note // 12) - 1     # MIDI octave number (Middle C is C4, which is MIDI note 60)
    return f"{note}{octave}"

# Function to parse MIDI file and extract notes and durations
def parse_midi(file_path):
    midi = mido.MidiFile(file_path)
    
    notes_and_durations = []  # List to store tuples of (note, duration)
    current_notes = {}  # Dictionary to keep track of ongoing notes

    for i, track in enumerate(midi.tracks):
        print(f"Track {i}: {track.name}")
        time_elapsed = 0

        # Loop through all messages in the track
        for msg in track:
            time_elapsed += msg.time  # Update time for each event
            
            # If the message is a 'note_on' event
            if msg.type == 'note_on' and msg.velocity > 0:
                current_notes[msg.note] = time_elapsed  # Record when the note starts playing
                
            # If the message is a 'note_off' event or a 'note_on' event with velocity 0
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in current_notes:
                    start_time = current_notes.pop(msg.note)  # Retrieve the start time
                    duration = time_elapsed - start_time  # Calculate duration
                    
                    # Add note and duration to the list as a tuple
                    note_name = get_note_name(msg.note)  # Convert note number to note name
                    notes_and_durations.append((note_name, duration))


    return notes_and_durations
		
try:
    music_data = poll()
    [print(i) for i in music_data]









    # Create the I2C bus interface
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create a PCA9685 object at I2C address 0x40
    pca = PCA9685(i2c)
    pca.frequency = 50  # Set frequency to 50Hz for servos

    # Create servo objects for channels 0 to 9
    servos = [servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500) for i in range(12)]

    # Define the delay between steps and each servo's movement
    step_delay = 0.0005  # 20ms delay between steps (adjust as needed)
    step_size = 1      # Move 1 degree per step
    servo_delay = 0.3  # Delay between each servo's movement start



    #we gotta assign the keys accordingly based on the first key of the leftmost servo
    # we can start at the leftmost key and add up from there so if leftmost is E, E is assigned to servo_motor[0] then F is servo[1] and etc.

    #currently we have leftmost as the e on the physical keyboard
    #leftmost servo is servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)

    #have a tuple containing key (ex. 'E'), time held (int 3 ms), 
    num_fingers = 12


    #key mapping:
    leftmost = 'D3'
    notemapping = {}
    curr = leftmost

    for i in range(12):
	    notemapping[curr] = i


	    curr = chr(ord(curr[0])+1) + curr[1]
	    if curr[0] == 'H':
		    curr = 'A' + curr[1]
	    if curr[0] == 'C':
		    curr = curr[0] + str(int(curr[1])+1)




    #finger assignment
    servo_order = [11, 0, 9, 1, 7, 2, 10, 3, 8, 4, 12, 5]
    fingers = {i: servo.Servo(pca.channels[servo_order[i]], min_pulse=500, max_pulse=2500) for i in range(12)}


    for note in music_data:
	    process_note(note)
	
except KeyboardInterrupt:
    pca.deinit()


