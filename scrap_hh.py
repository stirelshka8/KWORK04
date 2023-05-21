from bs4 import BeautifulSoup as bs
from random import choice
import requests
import csv

user_agents = []
with open('user_agents.txt', 'r') as file:
    for line in file.readlines():
        user_agents.append(line.replace('\n', ''))
random_user_agents = choice(user_agents)
