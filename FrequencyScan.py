# Author: Max Cowan 2017

# Dependencies:
#   Beautiful Soup 4 (pip3 install beautifulsoup4)
#   Urllib3 (pip3 install urllib)
#   csv (builtin python libraries)

import csv
import ssl
import re
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

# Input filename
PHRASE_FILE = "phrases_of_interest.txt"
# Map string phrases to their integer frequency
frequency_dict = {}


def load_words():
    phrase_list = open(PHRASE_FILE).read().splitlines()
    # Set initial frequency of all phrases to 0
    for item in phrase_list:
        frequency_dict[item.lower()] = 0

def get_webpage_text(str_url):
    print("Loading Page...")
    return urllib.request.urlopen(str_url).read().lower()

def search_html_for_phrases(strHTML):
    print("Searching Page...")
    # Load raw html into bs4 for parsing
    soup = BeautifulSoup(strHTML, 'html.parser')
    # Extract all visible text (including menus that require hover over) from webpage
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # Store the phrase frequency in the dictionary
    try:
        for phrase in frequency_dict:
            frequency_dict[phrase] = len((re.findall(r'\b%s\b' % phrase, text)))
    # Error is thrown when non alphanumeric characters exist in the phrase list (#, @, -, *) are some examples
    except re.error:
        print("ERROR: Please remove any non alphanumeric characters from the words of interest file, then run the search again.")

def generate_csv(sorted_list, filename):
    with open(filename, 'w') as mycsv:
        wr = csv.writer(mycsv)
        for item in sorted_list:
            wr.writerow(item)


# Main

print("\n-Generate a phrase frequency by providing a URL in the format (www.example.com/something). Other domains (.edu, .org, etc)"
      " are also supported\n-The output CSV file will be located under OUTPUT_FILES/[web address]phrase_frequency.csv\n"
      "-To add or remove phrases, edit the phrases_of_interest text file in the same directory as this Python file")
while True:
    # Store the address to be searched
    user_site = input("\nEnter a URL in the previously specified format: ")
    # Output file name
    frequency_output_file = "OUTPUT_FILES/[" + user_site + "]phrase_frequency.csv"
    # Ensure ssl certificate warnings don't disturb execution
    ssl._create_default_https_context = ssl._create_unverified_context
    # Load the words into the dictionary from text file
    load_words()
    try:
        # Check page for occurrences of phrases
        search_html_for_phrases(get_webpage_text("http://" + user_site))
        # Sort the dictionary by the most frequent words, if there are any matches
        sorted_words = sorted(frequency_dict.items(), key=lambda x: int(x[1]), reverse=True)
        # Write the .csv file
        generate_csv(sorted_words, frequency_output_file)
        print("Frequency file location: " + frequency_output_file)
    except urllib.error.HTTPError:
        print("ERROR: This website indicates automated page requests are disabled. You must manually phrase check this website, sorry.")
    except urllib.error.URLError:
        print("ERROR: Please enter a valid URL (without http://)")
    # Generate another file?
    user_response = input("Would you like to search another webpage? (Enter y or n): ")
    if user_response != 'y':
        print("Goodbye.")
        break

