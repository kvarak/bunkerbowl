from flask import render_template, request
from flask_bootstrap import Bootstrap
import yaml

from app import app

bootstrap = Bootstrap(app)

# --------------------------------------------------------------------------------
# Google Sheets
# --------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials

credential = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    ["https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)

bunkerbowlsheet = {}
bunkerbowlsheet[7] = "1v7QeeAKkV0y7GNDfpZntD4242YPo9jTeB-xLYjuLrFI"
bunkerbowlsheet[6] = "1GWV0D0LdhuokvxsgO38MYLQmbhndLbpOAaC79HLCQYU"
bunkerbowlsheet[5] = "1kJS7jsdvfCkvO07HCmQybbqpn9wmX58wOqhshoLUZ6U"
bunkerbowlsheet[4] = "1qwYVySOod7C1JfXmNWytCkkI9IQQS2M6u25epmOsPzs"
bunkerbowlsheet[3] = "http://holdtheground.blogspot.se/2017/11/bunker-bowl-season-3.html"
bunkerbowlsheet[2] = "1BY2FAPiFnEqDB84bnnga4nSfoeN7R7AHWQjFi2xGEYI"
bunkerbowlsheet[1] = "1c_ksQ5azUB0YsW2u_uait0Aty4crIR6qy1dSMVXoxSU"

bunkerbowlhistory = "1WKhsUERByCLcnOqSHWgJimNav7wY-QNvtCATINZzYIg"

currentseason = 7

# --------------------------------------------------------------------------------
# Help functions
# --------------------------------------------------------------------------------

def unique(list1):

    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return(unique_list)

# --------------------------------------------------------------------------------
# Route functions
# --------------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():

    try:
        gsheet = client.open_by_key(bunkerbowlhistory).worksheet("seasons")
    except:
        return render_template(
            'main.html')

    data = gsheet.get_all_records()

    return render_template(
        'main.html',
        data=data,
        season=season)

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/season', methods=['GET', 'POST'])
def season():

    season = int(request.values.get('s'))

    # -------------------
    # Get the matches
    # -------------------

    try:
        gsheet = client.open_by_key(bunkerbowlsheet[season]).worksheet("games")
    except:
        if season == 3:
            text = bunkerbowlsheet[season]
        else:
            text = ""
        return render_template(
            'season.html',
            text=text,
            season=season)

    data = gsheet.get_all_records()

    teams = {}

    for d in data:
        if d['type'] == "league":
            if d['home'] not in teams:
                tmp = {}
                tmp['name'] = d['home']
                tmp['matches'] = 0
                tmp['td'] = 0
                tmp['tdminus'] = 0
                tmp['tdtot'] = 0
                tmp['cas'] = 0
                tmp['casminus'] = 0
                tmp['castot'] = 0
                tmp['points'] = 0
                teams.update({d['home'] : tmp})
            if d['away'] not in teams:
                tmp = {}
                tmp['name'] = d['away']
                tmp['matches'] = 0
                tmp['td'] = 0
                tmp['tdminus'] = 0
                tmp['tdtot'] = 0
                tmp['cas'] = 0
                tmp['casminus'] = 0
                tmp['castot'] = 0
                tmp['points'] = 0
                teams.update({d['away'] : tmp})

    for d in data:
        if d['winner'] != "" and d['type'] == "league":

            teams[d['home']]['matches'] += 1
            teams[d['home']]['td'] += int(d['home TD'])
            teams[d['home']]['tdminus'] += int(d['away TD'])
            teams[d['home']]['tdtot'] += int(d['home TD'])
            teams[d['home']]['tdtot'] -= int(d['away TD'])
            teams[d['home']]['cas'] += int(d['home CAS'])
            teams[d['home']]['casminus'] += int(d['away CAS'])
            teams[d['home']]['castot'] += int(d['home CAS'])
            teams[d['home']]['castot'] -= int(d['away CAS'])
            if d['home'] == d['winner']:
                teams[d['home']]['points'] += 3
            elif "<tie>" == d['winner']:
                teams[d['home']]['points'] += 1

            teams[d['away']]['matches'] += 1
            teams[d['away']]['td'] += int(d['away TD'])
            teams[d['away']]['tdminus'] += int(d['home TD'])
            teams[d['away']]['tdtot'] += int(d['away TD'])
            teams[d['away']]['tdtot'] -= int(d['home TD'])
            teams[d['away']]['cas'] += int(d['away CAS'])
            teams[d['away']]['casminus'] += int(d['home CAS'])
            teams[d['away']]['castot'] += int(d['away CAS'])
            teams[d['away']]['castot'] -= int(d['home CAS'])
            if d['away'] == d['winner']:
                teams[d['away']]['points'] += 3
            elif "<tie>" == d['winner']:
                teams[d['away']]['points'] += 1


    sort_order = ['name', 'matches', 'castot', 'tdtot', 'points']

    teamstosort = teams
    for sortx in sort_order:
        sorted_teams = sorted(teamstosort, key=lambda x: (teamstosort[x][sortx]), reverse=True)
        newteams = {}
        for t in sorted_teams:
            newteams.update({t : teams[t]})
        teamstosort = newteams

    matchtype = ['final', 'bronsmatch', 'semifinal', 'league', 'jumbo', 'friendly']
    slutspel = ['final', 'bronsmatch', 'semifinal']

    dates = []
    for d in data:
        if d['Datum'] != "" and d['Datum'] != "#REF!":
            dates.append(d['Datum'])

    return render_template(
        'season.html',
        currentseason=currentseason,
        start=(min(dates)),
        end=(max(dates)),
        sorted_teams=sorted_teams,
        teams=teams,
        matchtype=matchtype,
        slutspel=slutspel,
        data=data,
        season=season)

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/regler')
def regler():

    try:
        gsheet = client.open_by_key(bunkerbowlhistory).worksheet("regler")
    except:
        return render_template(
            'regler.html')

    data = gsheet.get_all_records()

    groups = []
    for d in data:
        if d['grupp'] != "":
            groups.append(d['grupp'])
    unique_groups = unique(groups)

    return render_template(
        'regler.html',
        data=data,
        groups=unique_groups,
        season=season)

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/statistik')
def statistik():

    return render_template(
        'statistik.html')

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/team', methods=['GET', 'POST'])
def team():

    season = int(request.values.get('s'))
    team = request.values.get('team')
    print(team)

    # Get the team

    try:
        gsheet = client.open_by_key(bunkerbowlsheet[season]).worksheet(team)
        print("success for " + team + " season " + str(season))
        teamdetails = gsheet.get_all_records()

    except:
        print("failed for " + team + " season " + str(season))
        return render_template(
            'team.html',
            team=team,
            season=season)

    players = {}
    # Players roster
    for row in teamdetails:
        if row['Nr'] != "" and row['Position'] != "":
            tmp = {
                'Nr': row['Nr'],
                'Name': row['Name'],
                'Position': row['Position'],
                'MA': row['MA'],
                'ST': row['ST'],
                'AG': row['AG'],
                'PA': row['PA'],
                'AV': row['AV'],
                'Skills': row['Skills & Traits'],
                'COMP': row['COMP'],
                'DEFL': row['DEFL'],
                'INT': row['INT'],
                'CAS': row['CAS'],
                'TD': row['TD'],
                'MVP': row['MVP'],
                'SPPearned': row['SPP\nEARNED'],
                'SPPspent': row['SPP\nSPENT'],
                'SPP': row['SPP'],
                'BaseCost': row['Base Cost'],
                'ValueIncrease': row['Value increase'],
                'Value': row['Value'],
                'MNG': row['MNG'],
                'TR': row['TR'],
                'CurrentValue': row['Current Value'],
                'Nigg': row['Nigg'],
                'Special': row['Special']
                }
            players.update({row['Nr'] : tmp})

    teamdata = {}

    for row in teamdetails:
        if row['Name'] == "Team":
            teamdata.update({'team': row['Position']})
        elif row['Name'] == "Ägare":
            teamdata.update({'owner': row['Position']})
        elif row['Name'] == "Name":
            teamdata.update({'name': row['Position']})
        elif row['Name'] == "Hemmaplats":
            teamdata.update({'place': row['Position']})
        elif row['Name'] == "Hemmapitch":
            teamdata.update({'pitch': row['Position']})
        elif row['Name'] == "Special Rules":
            teamdata.update({'rules': row['Position']})
        elif row['Name'] == "ShortName":
            teamdata.update({'shortname': row['Position']})
        elif row['Name'] == "Re-rolls":
            teamdata.update({'rerolls': row['MA']})
        elif row['Name'] == "Dedicated Fans":
            teamdata.update({'dedicatedfans': row['MA']})
        elif row['Name'] == "Cheerleaders":
            teamdata.update({'cheerleaders': row['MA']})
        elif row['Name'] == "Assistant Coaches":
            teamdata.update({'assistantcoaches': row['MA']})
        elif row['Name'] == "Apothecaries":
            teamdata.update({'apothecaries': row['MA']})
        elif row['Name'] == "Treasury":
            teamdata.update({'treasury': row['Position']})
        elif row['Name'] == "Team Value (TV)":
            teamdata.update({'tv': row['Position']})
        elif row['Name'] == "Current Team Value (CTV)":
            teamdata.update({'ctv': row['Position']})
        elif row['Name'] == "Link to logo":
            teamdata.update({'logo': row['Position']})
        elif row['Name'] == "Summa SPP":
            teamdata.update({'spp': row['Position']})
        elif row['Name'] == "Antal spelbara spelare":
            teamdata.update({'spelbara': row['Position']})

    print(teamdata)

    return render_template(
        'team.html',
        teamdata=teamdata,
        team=team,
        season=season,
        players=players)

# --------------------------------------------------------------------------------
