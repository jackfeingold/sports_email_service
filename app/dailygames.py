from datetime import date
import requests
from dotenv import load_dotenv
import os
from app.standings import get_standings
from pprint import pprint



def load_schedule():

    load_dotenv()

    # sets today's date
    today = date.today()

    # Sets today's date variables automatically // calls API key from .env
    day = str(today.day)
    month = str(today.month)
    year = str(today.year)
    api_key = os.getenv('SPORTSRADAR_NHL_API')


    # code to get API data, syntax courtesy of Plotly
    schedule_url = 'http://api.sportradar.us/nhl/trial/v7/en/games/' + year + '/'+ month + '/'+ day + '/schedule.json?api_key=' + api_key
    schedule_r = requests.get(schedule_url)
    schedule_data = schedule_r.json()
    print('\n')
    #print(len(schedule_data["games"]))
    return schedule_data


# still need to resolve how to show the time of the game, looks wonky af in the data
def show_schedule(schedule_data):

    print(schedule_data["date"], "SCHEDULE:")
    for game in schedule_data["games"]:
        print(game["home"]["name"], "host the", game["away"]["name"])
        print(game["away"]["alias"], "@", game["home"]["alias"])
        print("Scheduled for:", game["scheduled"])
        broadcasts = []
        for broadcast in game["broadcasts"]:
            broadcasts.append(broadcast["network"])
        
        #there is a weird comma that shows up after "Watch on:" but I don't know how to get rid of it and still print the networks on the same line
        print("Watch on:", *broadcasts, sep = ", ")
        print(" ")
        print("-----")
        print(" ")



if __name__ == "__main__":

    schedule_data = load_schedule()

    # imports standings
    standings = get_standings()

    # Loops through days' games and prints home and away teams
    for game in schedule_data['games']:
        # prints teams playing
        print(' - ' + game['away']['name'] + ' at ' + game['home']['name'])

        
        
        # prints the teams' records
        for i in range(len(standings)):
            if standings[i][0] in game['away']['name']: #away team
                # each team has this [team name, win #, loss #] in standings
                record_msg = '   - Record: ' + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L) // '
        for i in range(len(standings)):
            if standings[i][0] in game['home']['name']: #home team
                # each team has this [team name, win #, loss #] in standings
                # adds home team to away team standings
                record_msg = record_msg + standings[i][0] + ' (' + str(standings[i][1]) + 'W-' + str(standings[i][2]) + 'L)'
        print(record_msg)   
    
        # prints info about the boradcast
        broadcast_msg = '   - Broadcasts: '
        for i in range(len(game['broadcasts'])):
            broadcast_msg = broadcast_msg + (game['broadcasts'][i]['network'])
            # if statements make sure to format the list correctly
            if 'locale' in game['broadcasts'][i].keys():
                broadcast_msg = broadcast_msg + ' (' + game['broadcasts'][i]['locale'].lower() + ')'
            if i < (len(game['broadcasts'])-2):
                broadcast_msg = broadcast_msg + ', '
            if i == (len(game['broadcasts'])-2):
                broadcast_msg = broadcast_msg + ' and ' 
        print(broadcast_msg)
        
        print('')
