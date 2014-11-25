MovieReviewGenerator
====================

Final Project for CS 73
====================
Data Files Hierarchy/Format:

The data directory contains a folder for each product ID. Each product ID folder contains:

	emissions.txt: stores all part-of-speech tags from the movie's reviews, along with the words that have that part-of-speech and their frequencies
	bg_emissions.txt: stores all (overlapping) part-of-speech bigrams from the movie's reviews, along with the two-word sequences that have those parts of speech and their frequencies
	tr_emissions.txt: stores all (overlapping) part-of-speech trigrams from the movie's reviews, along with the three-word sequences that have those parts of speech
	transitions.txt: stores all part-of-speeches, along with the part-of-speeches that immediately follow
	bg_transitions.txt: stores all (overlapping) part-of-speech bigrams, along with the part-of-speech bigrams that follow
	tr_transitions.txt: stores all (overlapping) part-of-speech trigrams, along with the part-of-speech trigrams that follow
	pos.txt: file containing a movie's reviews, each word tagged with its part-of-speech
	reviews.arpa: stores each word from a movie's reviews, and the part-of-speech tags that follow that word; for each part-of-speech tag, a list of words that have that part-of-speech tag is listed
	sentence_ids.txt: tags each word with the id of the sentence that the word comes from; the file is not actually used because sentence_id's did not improve the performance of our program
	texts.txt: the texts collected from a movie's reviews
	summaries.txt: the summaries collected from a movie's reviews

====================
How the Data Files were Obtained:

1. Download the data set file from https://snap.stanford.edu/data/web-Movies.html and name the file "movies.txt" in the same folder as parse_dataset.py

2. Call "python parse_dataset.py" to create the data directory, the folders for each product ID, and the summaries.txt and texts.txt files for each product ID. The allsummaries.txt file is also created.

3. Change directory into the stanford-postagger-2014-10-26 folder, and call "python annotate.py" to create the pos.txt file for each product ID. Then, go up a directory level, to where you originally were.

4. Call "python pos_tagger_file.py" to create all the emissions, transitions, and reviews.arpa files for each product ID.

5. Run a command like:

	python sentence_generator.py 078401115X "Angel Heart" 0 0 1

to generate a review for the movie, "Angel Heart". The command line arguments are explained in the sentence_generator.py file.

The website version of our program can be found at: http://www.cs.dartmouth.edu/~mbarragan