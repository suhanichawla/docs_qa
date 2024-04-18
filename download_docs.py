import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# The URL to scrape
url = "https://gpt-index.readthedocs.io/en/stable"

# The directory to store files in
output_dir = "./llamindex-docs/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Fetch the page
response = requests.get(url)
print("Response status code:", response.status_code) 
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links to .html files
links = soup.find_all('a', href=True)

# Debug statement to check the number of links found
print("Number of links found:", len(links))

# Loop over each link
for link in links:
    href = link['href']

    # If it's a .html file or a full URL
    if href.endswith('.html') or (href.startswith('http://') or href.startswith('https://')):
        if not href.startswith('http://') and not href.startswith('https://'):
            href = urllib.parse.urljoin(url, href)
        print("Final href:", href)  # Debug statement

        try:
            # Fetch the .html file
            print("Downloading:", href)  # Debug statement
            file_response = requests.get(href)
            print("File response status code:", file_response.status_code)  # Debug statement
            # print("File response content:", file_response.content)  # Debug statement

            # Write it to a file
            file_dir = href[:-1] if href.endswith('/') else href
            file_name = os.path.join(output_dir, os.path.basename(file_dir))
            print("Saving to file:", file_name)  # Debug statement
            with open(file_name, 'wb') as file:
                file.write(file_response.content)
            print("Downloaded:", href)
        except Exception as e:
            print("Error downloading:", href)
            print("Exception:", e)
    else:
        # Join URL with base URL if href is not a full URL
        href = urllib.parse.urljoin(url, href)
        print("Final href:", href)  # Debug statement

        try:
            # Fetch the .html file
            print("Downloading:", href)  # Debug statement
            file_response = requests.get(href)
            print("File response status code:", file_response.status_code)  # Debug statement
            # print("File response content:", file_response.content)  # Debug statement

            # Write it to a file
            file_dir = href[:-1] if href.endswith('/') else href
            file_name = os.path.join(output_dir, os.path.basename(file_dir))
            print("Saving to file:", file_name)  # Debug statement
            with open(file_name, 'wb') as file:
                file.write(file_response.content)
            print("Downloaded:", href)
        except Exception as e:
            print("Error downloading:", href)
            print("Exception:", e)