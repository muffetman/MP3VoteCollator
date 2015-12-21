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
