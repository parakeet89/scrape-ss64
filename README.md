# About
The website we’re scraping is https://ss64.com. The final output will be a .txt file that contains commands, definitions and a link to the dedicated page for each command. If you're downloading a page of Mac commands, for example, you will get a list of ~299 terms.

# How It Works
Here is a step by step summary of how the program should run:
1. The program begins by asking the user for the operating system path. Expected responses: mac, bash (for Linux), nt (for Windows), etc.
2. The program determines the page to scrape based on the user’s input from the previous question. This page lists most of the available commands by operating system in an A-Z index.
3. From this page, the program collects terms, definitions and a specific URL for the dedicated page. The program creates a dictionary and stores a definition and URL as a list of values for each term.
4. The program counts the number of terms in the dictionary, omitting linked pages that are not in the A-Z index.
5. The program asks the user if the user would like to update a definition, prompting the user with a yes/no question, then prompting the user for the term and definition and repeating this step until the user indicates that they are done updating definitions.
* Because each term should already have a definition, the program will warn the user that the user would be changing an existing definition.
* If a term doesn’t exist, the program will indicate an error and will prompt the user for a different term.
6. The user is asked for a filename to save the file as.
7. The program writes the output to the designated text file and saves this file.
8. This output contains three columns: Term, Definition and URL. An example file is one created for Mac, which should contain 299 terms, definitions and URLs.
