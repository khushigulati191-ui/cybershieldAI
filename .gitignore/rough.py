import urllib.request 
from urllib.parse import urlparse

url = urllib.request.urlopen("https://youtube.com")
for line in url:
    print(line.decode().strip())