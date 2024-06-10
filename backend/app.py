from flask import Flask 
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = 'Content-Type'


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/scores")
def find_score_summary():  
    score_summary = []
    url = "https://www.mlb.com/scores/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        search = soup.find_all('div', 'grid-itemstyle__GridItemWrapper-sc-cq9wv2-0 gmoPjI')

        for i in search:
            score = i.find('div','StatusLayerstyle__StatusLayerWrapper-sc-1s2c2o8-1 jkfZwE')
            score_summary.append(score['aria-label'])

    return(score_summary)

@app.route("/stats/<team>")
def find_stats(team):
    stats_results = []
    url= f"https://www.mlb.com/{team}/stats/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        search = soup.find('div', 'table-scroller-GsCM0EhI scroller').find_all('table', 'bui-table')

        for i in search:
            numbers = i.find('tbody').find_all('tr')

            for j in numbers:
                player_name = j.find('th').find('a')
                player_name = player_name['aria-label']
                position = j.find('div','position-SAxuJGcx')
                table = j.find_all('td') 
                stats_results.append(player_name)
                stats_results.append(position.string)
                
                for c in table:

                    stats_results.append(c.text)
        return(stats_results)
        
    
@app.route("/standings")
def find_standings():
    standings_results = []
    url = "https://www.mlb.com/cubs/standings/mlb"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        search = soup.find('div', 'section-container').find_all('table','tablestyle__StyledTable-sc-wsl6eq-0 cprRUf StandingsTablestyle__DataTableWrapper-sc-1l6jbjt-1 kCeyFZ auto-scroller')

        for i in search:
            table = i.find('tbody').find_all('tr')

            for j in table:
                found_standings = j.find('td','table-cellstyle__StyledTableCell-sc-xpntj7-2 fcmYDB').find('span')
                teamName = found_standings['aria-label']
                standings_results.append(teamName)

        return(standings_results)

@app.route("/roster/<team>")
def find_roster(team):

    roster_results = []
    #url that we are going to be getting the roster from 
    url = f"https://www.mlb.com/{team}/roster/40-man"
    #GET request to the url 
    response = requests.get(url)

    #If the request was good
    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        search = soup.find('div', 'players').find_all('table','roster__table')

        for i in search:
            table = i.find('tbody').find_all('tr')
            #ADD A SEARCH FOR THE POSITION
            for j in table:
                found_player = j.find('td','info').find('a')
                roster_results.append(found_player.string)
        return (roster_results)
    
