#!/usr/bin/env python

## This python script will automatically collate votes for an MP3 music countdown.
## The script must be run from a base directory, with votes for each person stored in individual sub-directories, named with the voter's name.
## All votes must be in Mp3 format and MUST be prepended with a number, starting from 01. For example: 01=Lowest vote, 15=Highest vote.
## This is an example of what a file should look like: 15. Foo Fighters - Walk.mp3. This song would receive 15 votes from this person.

## HOW IT WORKS:
## The script will begin by checking all MP3 files for matching strings, ie. song names.
## When matches are found, the script will check the start of each file for the number, to determine how many votes that song has received.
## The script will add the numbers together to get the total number of votes for that song, whilst recording who voted and how many votes they gave.
## Once the results have been recorded, the script will copy the MP3 files to a directory and renamed according to the order in which they finished.
## I.e. The song with the highest votes will be prepended with 01, song number two will be prepended with 02 etc etc.

import os, sys, csv, operator, itertools, shutil
from collections import Counter, defaultdict

print("*****Welcome to the MP3 Vote Collator*****" + '\n')

# Global variables and lists
file_extension = (".mp3", ".MP3", ".Mp3", ".mP3")
results_file = "results_out.csv"
tts_script = "tts_script"
votes = defaultdict(list)
tally = Counter()
speaker_text = ()
base_dir = os.getcwd()
ignore_list = ["Playlist"] # Ignore this dir to avoid issues when copying MP3 files(I.e. src/dst are the same). This dir must be empty prior to running script

""" Check to see if Playlist directory is present. If not, create it """

for subdir, dirs, files in os.walk(base_dir):
	if not os.path.exists("Playlist"):
		os.makedirs("Playlist")
	else:
		break

def check_mp3s():
	""" Checks all MP3 files to ensure they are in the correct format """

	print("STAGE 1. Preliminary check to ensure all MP3 files are in the correct format...")
	for subdir, dirs, files in os.walk(base_dir):
		dirs[:] = [d for d in dirs if d not in ignore_list]
		for file in files:
			format_check = file.count('.')
			sub_dir = str(os.path.split(subdir))
			if (file.endswith(file_extension) and
				format_check > 2):
				print('\n' + "Incorrect file format detected! " + "FOLDER: " + sub_dir + " FILE: " + file + '\n')
				sys.exit("!!Aborting Script!! Please ensure file names are correct before proceeding.")
			else:
				break

def tally_votes():
	""" The tally_votes function is responsible for searching for all .mp3 files, retrieving the vote count for each song and
	    storing the results in the 'tally' counter. """

	global votes
	global tally
	global speaker_text
	print('\n' + "STAGE 2. Processing Votes..." + '\n')
	for subdir, dirs, files in os.walk(base_dir):
		dirs[:] = [d for d in dirs if d not in ignore_list]
		for file in files:
			if file.endswith(file_extension):
				vote_count, song, _ = file.lower().split('.')
				_, voter_name = os.path.split(subdir)
				voice_script = (vote_count + " votes from " + voter_name + ".")
				try:
					tally[song] += int(vote_count) # Adds song to tally. If song already exists, adds votes to that song
					votes[song].append((voice_script))
					#votes[song].append((voter_name, int(vote_count))) # Adds voter name and vote count to votes dict
				except:
					break


def write_tally():
	""" The write_tally function will write the results to a CSV file called 'results_out.csv' in the base directory """

	tally_list = sorted(list((tally).items()),key=operator.itemgetter(1), reverse=True) # Converts tally counter to a list and sorts songs based on highest votes
	votes_list = sorted(list((votes).items()),key=operator.itemgetter(0)) # Converts votes dict to a list and sorts in alphabetical order
	with open(results_file, 'w') as resultsout, open('vote_list.csv', 'w') as votelistout:
		resultswriter = csv.writer(resultsout)
		votelistwriter = csv.writer(votelistout)
		resultswriter.writerows(tally_list)
		votelistwriter.writerows(votes_list)


def process_result():
	""" The process_result function will read the results from the CSV and print them to output """

	print("STAGE 3. Listing Top 3 Songs:" + '\n')
	with open(results_file, 'r') as results:
		reader = csv.reader(results)
		for iteration, row in enumerate(csv.reader(results)):
			print("The number {} song for this year's count is: {}, with a total of {} votes!".format(
					["one", "two", "three"][iteration], row[0], row[1]))
			if iteration >= 2:
				break
		print('\n' + "There are a total number of " + str(len(tally)) + " songs in this year's count.")


def speaker_script():
	""" This function will write the script for festival TTS """

	print("Creating script for festival TTS" + '\n')
	with open(results_file, 'r') as results, open(tts_script, 'w') as speakerscript:
		reader = csv.reader(results)
		for iteration, row in enumerate(csv.reader(results)):
			text = ("Song number {} is, {}, with a total number of {} votes".format(range(1, 1000, 1)[iteration], row[0], row[1]) + '. ' + '|' + '\n')
			speakerscript.write(text)


def process_mp3s():
	""" The process_mp3 function will read the CSV file line by line, rename MP3 files accordingly and then copy them
    	to the 'Playlist' directory """

	print('\n' + "STAGE 4. Grouping and Renaming MP3 Files...")
	for subdir, dirs, files in os.walk(base_dir):
		dirs[:] = [d for d in dirs if d not in ignore_list]
		for file in files:
			if file.endswith(file_extension):
				file_name = file.split('.')[1]
				with open(results_file, 'r') as results:
					reader = csv.reader(results)
					for iteration, row in enumerate(csv.reader(results)):
						song_name = row[0].title() # Capitalize song names for cleaner look
						mp3_file = os.path.join(os.path.join(subdir), file)
						new_name = ("{}".format("%02d" % range(1, 1000, 1)[iteration]) + "." + song_name + ".mp3") # Rename MP3 files according to correct order
						playlist_dir = ("Playlist")
						if not os.path.exists(playlist_dir): # For storing renamed MP3 files
							os.mkdir(playlist_dir)
						if (file_name.lower() == song_name.lower() and
							song_name not in playlist_dir):
							shutil.copy(mp3_file, playlist_dir) # Currently copies for testing purposes. Probably best to change this to shutil.move
							os.chdir(playlist_dir)
							os.rename(file, new_name)
							os.chdir(base_dir) # Return to base directory for restart of function

if __name__ == '__main__':
	check_mp3s()
	tally_votes()
	write_tally()
	speaker_script()
	process_result()
	process_mp3s()
