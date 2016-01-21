This python script will automatically collate votes for an MP3 music countdown.
The script must be run from a base directory, with votes for each person stored in individual sub-directories, named with the voter's name.

Example folder structure:
BASE_DIRECTORY
-top15_collator.py
	|---Sam
		|----01. AFI - Medicate.mp3
		|----02. Muse - Starlight.mp3
	|---Sally
		|----01. Alexisonfire - Adelleda.mp3
		|----02. Die Antwoord - Ugly Boy.mp3

All votes must be in Mp3 format and MUST be prepended with a number, starting from 01. For example: 01=Lowest vote, 15=Highest vote.
This is an example of what a file should look like: 15. Foo Fighters - Walk.mp3. This song would receive 15 votes from the person who's folder the Mp3 resides.

HOW IT WORKS:
The script will begin by running a simple check of file names. If there are more than two '.' detected in a filename, the script will terminate.
It will then scan for all Mp3 files, strip then vote count and song names from the file names and then store them into CSV files for further processing.
Matching songs will have their total votes added to a tally. I.e. if Sam gives a song five votes and Sally gives the same song eight votes, this will be tallied
and stored with a total of thirteen votes. Once the results have been recorded, the script will move the MP3 files to a directory and rename them according to
the order in which they finished. I.e. The song with the highest votes will be prepended with 01, song number two will be prepended with 02 etc etc.

I have also added the ability to have an 'announcer' commentate the countdown, through the use of Festival TTS. Festival 2.1 or higher needs to be installed 
for this to work. I have only tested this on a single Arch Linux system. It has not been tested on any other O/S.
top15_collator.py will generate a file called tts_script in the base directory. You can then run tts_processor.py which will read this script and output .wav
files to the Playlist directory.
