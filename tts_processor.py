#!/usr/bin/env python

## This is a python program that will perform TTS actions by utilizing the Festival TTS Engine: http://www.cstr.ed.ac.uk/projects/festival
## Festival 2.1 or higher must be installed for this script to function

import subprocess, csv, itertools, os

def process_tts():
	wavfolder = 'wavs'
	file = 'speaker_script'
	base_dir = os.getcwd()
	playlist_dir = 'Playlist'
	with open(file, 'r') as filein:
		for iteration, row in enumerate(csv.reader(filein, delimiter='|')):
			filename = '{}.Zzz.announce.wav'.format("%02d" % range(1, 1000, 1)[iteration])
			text = '"' + row[0] + '"'
			subprocess.call('echo ' +text+' | text2wave -o '+playlist_dir +'/' +filename, shell=True)

if __name__ == '__main__':
	process_tts()
