import os
import time

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
			print('File created')
			
		prev = curr
		
		time.sleep(1)
		
poll()
	
penis
