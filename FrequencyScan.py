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

# Phrases filename
PHRASE_FILE = "phrases_of_interest.txt"
# Sites filename
SITES_FILE = "webpage_list.txt"
# Map string phrases to their integer frequency
frequency_dict = {}
# Array to hold websites in webpage_list text file
sites = []

def load_words():
    phrase_list = open(PHRASE_FILE).read().splitlines()
    # Set initial frequency of all phrases to 0
    for item in phrase_list:
        frequency_dict[item.lower()] = 0

def load_sites():
    sites_list = open(SITES_FILE).read().splitlines()
    for page in sites_list:
        sites.append(page)

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

def generate_csv(sorted_list, filename, website):
    with open(filename, 'w') as mycsv:
        wr = csv.writer(mycsv)
        wr.writerow(["Site: " + website])
        for item in sorted_list:
            wr.writerow(item)

def single_page_mode():
    print(
        "\n\n-Generate a phrase frequency by providing a URL in the format (www.example.com/something). Other domains (.edu, .org, etc)"
        " are also supported\n-The output CSV file will be located under OUTPUT_FILES/[site number]phrase_frequency.csv\n"
        "-To add or remove phrases, edit the phrases_of_interest text file in the same directory as this Python file")

    file_counter = 1
    while True:
        # Store the address to be searched
        user_site = input("\nEnter a URL in the previously specified format: ")
        # Output file name
        frequency_output_file = "OUTPUT_FILES/[" + str(file_counter) + "]phrase_frequency.csv"
        # Ensure ssl certificate warnings don't disturb execution
        ssl._create_default_https_context = ssl._create_unverified_context
        # Load the words into the dictionary from text file
        load_words()
        if len(frequency_dict) == 0:
            print("There are no phrases in 'phrases_of_interest.txt' to load.")
        try:
            # Check page for occurrences of phrases
            search_html_for_phrases(get_webpage_text("http://" + user_site))
            # Sort the dictionary by the most frequent words, if there are any matches
            sorted_words = sorted(frequency_dict.items(), key=lambda x: int(x[1]), reverse=True)
            # Write the .csv file
            generate_csv(sorted_words, frequency_output_file, user_site)
            print("SUCCESS - Frequency file location: " + frequency_output_file)
        except urllib.error.HTTPError:
            print(
                "ERROR: This website indicates automated page requests are disabled. You must manually phrase check this website, sorry.")
        except urllib.error.URLError:
            print("ERROR: Please enter a valid URL (without http://)")
        file_counter += 1
        # Generate another file?
        user_response = input("Would you like to search another webpage? (Enter y or n): ")
        if user_response != 'y':
            print("Goodbye.")
            break

def multi_page_mode():
    print("\nLoading and scanning all pages listed in 'webpage_list.txt'\n")
    load_sites()
    load_words()
    if len(sites) == 0:
        print("There are no URLS in 'webpage_list.txt' to load.")
    if len(frequency_dict) == 0:
         print("There are no phrases in 'phrases_of_interest.txt' to load.")
    else:
        file_counter = 1
        # Ensure ssl certificate warnings don't disturb execution
        ssl._create_default_https_context = ssl._create_unverified_context
        for webpage in sites:
            # Output file name
            frequency_output_file = "OUTPUT_FILES/[" + str(file_counter) + "]phrase_frequency.csv"
            print("------------------------------------------------------------------\nTrying to scan http://" + webpage)
            try:
                # Check page for occurrences of phrases
                search_html_for_phrases(get_webpage_text("http://" + webpage))
                # Sort the dictionary by the most frequent words, if there are any matches
                sorted_words = sorted(frequency_dict.items(), key=lambda x: int(x[1]), reverse=True)
                # Write the .csv file
                generate_csv(sorted_words, frequency_output_file, webpage)
                print("SUCCESS - Frequency file location: " + frequency_output_file)
            except urllib.error.HTTPError:
                print(
                    "ERROR: This website indicates automated page requests are disabled. You must manually phrase check this website, sorry.")
            except urllib.error.URLError:
                print("ERROR: Please enter a valid URL (without http://)")
            file_counter += 1


# Main
user_choice = input("1 - Scan a single webpage for phrases\n2 - Scan multiple pages listed in 'webpage_list.txt'\n"
                    "\nEnter Selection (1 or 2): ")
if user_choice == "1":
    single_page_mode()
elif user_choice == "2":
    multi_page_mode()
else:
    print("'" + user_choice + "' is not a valid selection.")