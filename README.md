MovieReviewGenerator
====================

Final Project for CS 73
====================
Data Files Hierarchy/Format:

The data directory contains a folder for each product ID. Each product ID folder contains the following files:

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
How the run program:
If you downloaded all files from GitHub, simply do steps 1 and 5. If you want to recreate the data files that we have preprocessed, then do steps 1 through 5.

1. Download the data set file from https://snap.stanford.edu/data/web-Movies.html and name the file "movies.txt" in the same folder as parse_dataset.py. We did not include the movies.txt file in our submission on Github because it is too large.

2. Call "python parse_dataset.py" to create the data directory and the folders for each product ID, inside of which contains the summaries.txt and texts.txt files. The summaries.txt file holds each review summary for a given movie, and the texts.txt file holds each review text for a given movie. The program also creates the allsummaries.txt file, which contains all the summaries for all movies. The ngram model for sentence extraction will be trained on allsummaries.txt, because the summaries contain phrases that convey the reviewer's response/opinion of a movie.

3. Change directory into the stanford-postagger-2014-10-26 folder, and call "python annotate.py" to create the pos.txt file for each product ID. Then, go up a directory level, to where you originally were.

4. Call "python pos_tagger_file.py" to create all the emissions, transitions, and reviews.arpa files for each product ID. The program parses the pos.txt file. 

To create the emissions files, the program accumulate counts for each unigram, bigram, and trigram, categorizing them under the appropriate part-of-speech sequence. The bigrams and trigrams are overlapping--as an example, if "the red house" appears in the text, there will be a line for "the red" and "red house" in the emissions file.

To create the transitions files, the program accumulates counts for each part-of-speech ngram that follows a particular part-of-speech ngram. As an example: if the following appears in the bg_transitions.txt file:

IN_NN
RB_VBZ	1
WDT_MD	1
IN_DT	1

then that means the review text has the part-of-speech bigram RB_VBZ following IN_NN once, WDT_MD following IN_NN once, and IN_DT following IN_NN once.

To create the reviews.arpa file, the program accumulates counts for each part-of-speech that follows a particular word, along with the actual words for that part-of-speech. As an example, if the following appears in the reviews.arpa file:

years
VBZ | is
VBP | make
RB | ago already

then in the review text, the word "years" is followed once by "is", once by "make", once by "ago", and once by "already". As you can see, the words that follow "years" are grouped by part-of-speech.

5. Run a command like:

	python sentence_generator.py 078401115X "Angel Heart" 0 0 1

to generate a review for the movie, "Angel Heart". Here is the format and implementation details:

Command to run program:
python sentence_generator.py [Product ID] [Movie Name] [Type of Review] [Type of Part-of-speech Template] [Word Choice Selection Method]

Input:      Product ID: specifies the movie for which a review will be generated
            Movie Name: Title of the movie (to be printed out, not actually used in generating review)
            Type of Review: 
                0: extract a set of sentences from user reviews that most closely matches review summaries
                	Train an ngram model on the summaries of all movies
                	Find the top 1/5th sentences that have the lowest perplexities
                	Reduce the top 1/5th to 10 sentences based on TF-IDF
                1: construct a computer-generated review
                	Pick a part-of-speech template
                	Pick a word choice selection method
                	Collect a set of 10 sentences based on part-of-speech template and word choice selection method
                	Compute the TFIDF scores for each sentence, and output the sentence with the highest TFIDF score
                	Repeat the process multiple times to generate more sentences
            Type of Part-of-speech Template
                0: randomly generate part-of-speech template based on an FSA
                	To determine each subsequent part-of-speech, use a ngram model based on the previous part-of-speech(es)
                1: select a sentence from the review to use as the part-of-speech template
                	Randomly select a sentence from the review, and use its part-of-speech sequence as the template
            Word Choice Selection Method
                0: select contiguous groups of words from user reviews for each triplet of part-of-speech tags
                	Divide the part-of-speech sequence into groups of three, overlap the groups, and three-word sequences for each part-of-speech triplet
                	Example of how overlap is achieved:
                		POS Template: "DET" "ADJ" "NN" "PRP" "DET" "NN"
                		Overlap: "DET_ADJ_NN" "NN_PRP_DET" "DET_NN"
			            Generate three words for "DET_ADJ_NN", i.e. "the red house"
			            Generate three words for "NN_PRP_DET", i.e. "car in the" //ignore the first part-of-speech, which will come from previous ngram
			            Generate two words for "DET_NN", i.e. "a neighborhood" //ignore the first part-of-speech, which will come from previous ngram
			            Combine the words into a sentence in the following manner: "the red house in the neighborhood"
                1: select one word at a time for each part-of-speech, using a bigram model based on the part-of-speech of the previous word
                	

The website version of our program can be found at: http://www.cs.dartmouth.edu/~mbarragan
