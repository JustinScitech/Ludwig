import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Create the I2C bus interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create a PCA9685 object at I2C address 0x40
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 50Hz for servos

# Create servo objects for channels 0 to 9
servos = [servo.Servo(pca.channels[i], min_pulse=500, max_pulse=2500) for i in range(10)]

# Define the delay between steps and each servo's movement
step_delay = 0.0005  # 20ms delay between steps (adjust as needed)
step_size = 1      # Move 1 degree per step
servo_delay = 1  # Delay between each servo's movement start


music_data = []
#we gotta assign the keys accordingly based on the first key of the leftmost servo
# we can start at the leftmost key and add up from there so if leftmost is E, E is assigned to servo_motor[0] then F is servo[1] and etc.

#currently we have leftmost as the e on the physical keyboard
#leftmost servo is servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)

#have a tuple containing key (ex. 'E'), time held (int 3 ms), 
leftmost_key = "A4"
default_key = leftmost_key
num_fingers = 11

#finger assignment
servo_order = [11, 0, 9, 1, 7, 2, 10, 3, 8, 4, 12, 5]
fingers = {i: servo.Servo(pca.channels[servo_order[i]], min_pulse=500, max_pulse=2500) for i in range(12)}

def play_note(servo, play_time, rest_time):
	servo.angle = 90
    time.sleep(0.2)
    servo.angle = 170
    time.sleep(play_time)
    servo.angle = 0

#This is where we find whichever finger this note should be corresponding to
def find_servo(key):
	letter = key[0]
	leftmost_letter = leftmost_key[0]
	#do like key - leftmost_key to find the finger it should be
	finger = 
	
	return finger
	

def process_note(note):
	#note is a tuple containing the key, playTime, and rest time data
	key, play_time, rest_time = note
	servo = find_servo(key)
	#here we need to determine which servo to play and for how long
	move_servo(servo, play_time, rest_time)

#loop through music array data
for note in music_data:
	process_note(note)

# Function to move a servo from 0 to 180 and back to 0
def move_servo(servo):
    # Move from 0 to 180 degrees
    servo.angle = 90
    time.sleep(0.2)
    servo.angle = 170
    time.sleep(0.2)
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
try:
    while True:
        for s in servos:
            #servo_chord_start(servos[0], servos[1], servos[6])
            #servo_chord_end(servos[0], servos[1], servos[6])
            move_servo(s)
            time.sleep(servo_delay)  # Delay between moving each servo

except KeyboardInterrupt:
    pca.deinit()  # Clean up on exit
