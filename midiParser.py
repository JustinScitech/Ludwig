import mido

# Map MIDI note numbers to note names
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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

# Main function to call the parser
if __name__ == "__main__":
    midi_file = "output.mid"  # Replace eith actual file
    notes_and_durations = parse_midi(midi_file)
    
    print("\nNotes and durations as tuples:")
    for note_tuple in notes_and_durations:
        print(note_tuple)
