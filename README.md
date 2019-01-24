# BeautifulSoupHTMLReplace
Simple Python 3 scripts to parse and update html files using BeautifulSoup

## Introduction
The repository contains several python 3 scripts that can be used for parsing html files and updating some common elements as well checking 
html files for broken links. 

* html_footer_replace.py can update the year and copyright information in html file. 
* html_ahref_replace.py adds the rel="noopener noreferrer" to all &lt;a&gt; tag that contains target="_blank"
* html_check_broken_links.py check for broken and invalid links in html files

The scripts require BeautifulSoup library. The broken link checker script which can be used to check and find broken or invalid links
in html files requires both BeautifulSoup and the Requests library. 

## Installing the Dependencies

> pip3 install beautifulsoup4

> pip3 install requests


## Running the scripts

Obtain a copy of the scripts 

> git clone https://github.com/ngchianglin/BeautifulSoupHTMLReplace.git

Each scripts have certain configuration variables defined at the top. Open up the relevant with a text editor, read through the script to 
understand what it does. Change the configuration variables accordingly to your needs. Then run the script.  

**Warning: Always backup your files first before running the scripts to avoid data corruption or data loss !**
**The scripts will replace and change your files !**

> python3 <script name>

## Further Details

Refer to 
[https://www.nighthour.sg/articles/2019/replacing-updating-html-files-beautifulsoup.html](https://www.nighthour.sg/articles/2019/replacing-updating-html-files-beautifulsoup.html) 
for an in-depth article on how the scripts are implemented and how it can be used.

## Source signature
Gpg Signed commits are used for committing the source files. 

> Look at the repository commits tab for the verified label for each commit, or refer to [https://www.nighthour.sg/git-gpg.html](https://www.nighthour.sg/git-gpg.html) for instructions on verifying the git commit. 

> A userful link on how to verify gpg signature [https://github.com/blog/2144-gpg-signature-verification](https://github.com/blog/2144-gpg-signature-verification)


