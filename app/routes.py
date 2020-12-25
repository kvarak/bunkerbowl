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
    # print(data)

    return render_template(
        'season.html',
        data=data,
        season=season)

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/regler')
def regler():

    return render_template(
        'regler.html')

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/statistik')
def statistik():

    return render_template(
        'statistik.html')

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

@app.route('/team')
def team():

    return render_template(
        'team.html')

# --------------------------------------------------------------------------------
