from bs4 import BeautifulSoup
import requests
import pandas


URL = 'https://www.metacritic.com/browse/games/release-date/new-releases/all/date'
headers = {'Accept-Language':'en-us',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
titles = soup.find_all(name='a', class_="title")
ratings = soup.find_all(name='div', class_="clamp-score-wrap")
where_to_pay = soup.find_all(name='span', class_="data")

game_titles = [title.getText() for title in titles]
print(game_titles)
consoles = [console.getText().translate(str.maketrans('', '', '\n \xa0')) for console in where_to_pay][:len(game_titles)]
print(consoles)
meta_scores = [rating.getText().translate(str.maketrans('', '', '\n ')) for rating in ratings]
print(meta_scores)

game_table = {
    'Game title': game_titles,
    'Platform': consoles,
    'Meta Score': meta_scores,
}

data = pandas.DataFrame(game_table)
data.to_csv('metascores.csv')
