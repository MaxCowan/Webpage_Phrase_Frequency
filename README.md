# Webpage_Phrase_Frequency

Given a URL or list of URLS, output the frequency of phrases specified in a text file in a CSV format
-----
This small command line application was designed for a friend doing research on e-sports.

## 1. Dependencies:
* Python 3.X 
* Beautiful Soup 4 ```pip3 install beautifulsoup4```
* Urllib ```pip3 install urllib```

## 2. Instructions for operation:

* i.) Edit the ```phrases_of_interest.txt``` file to reflect the phrases you want to search for
* ii.) Edit the ```webpage_list.txt``` file to reflect the URLs you want to scan (following the http://)
* iii.) Open a terminal or command prompt session
* iv.) Navigate to the 'Webpage_Phrase_Frequency' project folder
* v.) Run the command ```Python3 FrequencyScan.py```
* vi.) Follow onscreen instructions, and view the resultant CSV files in the ```OUTPUT_FILES/``` directory

##### **NOTE: Each time you run this script, files in the OUTPUT_FILES directory will be overwritten**