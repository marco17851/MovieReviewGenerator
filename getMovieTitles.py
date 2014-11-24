"""
# Author: 	Marco Barragan
# Date: 	November 16, 2014

# Input: 	None
# Output: 	The file NameIDs.txt that contains the movie titles and their
			respective IDs.

# Description: 	This program uses the Amazon Product API to obtain the
				titles of the movies that we are using for our sentence
				generator.
"""


from amazonproduct import API
import os
import sys

if __name__ == "__main__":
	api = API(locale='de')

	# Opens the root directory that contains all of the movie ID and
	# outputs a file that contains the movie ID and the respective movie titles
	rootdir = "data/"
	output = open("NameIDs.txt", "w")

	# Loops through the directory
	for subdir, dirs, files in os.walk(rootdir):
		for dirNum in dirs:

			# Looks up the product.
			try:
				product = api.item_lookup(ItemId=dirNum)
			except:
				#print "Error: The file %s was not found." %dir
				continue

			# Obtains the name of the movie
			for item in product.Items.Item:
				try:
					title = item.ItemAttributes.Title.__str__()
				except:
					continue

				# Outputs the title and the movie ID
				print (title + "|" + dirNum + "\n")
				output.write(title.encode('UTF-8') + "|" + dirNum + "\n")
