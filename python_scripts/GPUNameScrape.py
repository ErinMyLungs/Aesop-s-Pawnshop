import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html5lib')

# This finds all the GPU names on the page. Time to try and limit this to within a section
names = soup.find_all('th', style='text-align:left;')

nvidia = pd.DataFrame([name.text for name in names]).to_csv('/home/erin/PycharmProjects/HardwareScrape/data/nvidia_gpu_names.csv')