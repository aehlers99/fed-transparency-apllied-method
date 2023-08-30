import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from PyPDF2 import PdfReader
# Get the html from the webpage

url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"


#Request
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

content = soup.find_all("div", class_='col-xs-12 col-md-4 col-lg-2')

href_list = []

# Filtering links
for div in content:
    a_tag = div.find("a")
    if a_tag:
        href_value = a_tag.get('href')
        # Check if the href_value is not None and ends with .pdf
        if href_value and href_value.endswith('.pdf'):
            href_list.append('https://www.federalreserve.gov/' + href_value)

#Label + saveing the pdfs
label_list = []

for href in href_list:
    response = requests.get(href)
    filename = href.split("/")[-1]
    filepath = os.path.join("PDFs", filename)
    with open(filepath, "wb") as f:
        f.write(response.content)
    label_list.append(f'PDFs/{filename}')
 
