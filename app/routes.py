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
bunkerbowl7sheet = "1v7QeeAKkV0y7GNDfpZntD4242YPo9jTeB-xLYjuLrFI"
#gsheet = client.open(bunkerbowl7sheet).worksheet("games")
gsheet = client.open_by_key(bunkerbowl7sheet).worksheet("games")


# --------------------------------------------------------------------------------
# Route functions
# --------------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
@app.route('/season')
@app.route('/regler')
@app.route('/statistik')
def index():

    # a_yaml_file = open('data/skills.yml')
    # parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

    # states = parsed_yaml_file['config']['states']
    # skills = parsed_yaml_file['skills']

    data = gsheet.get_all_records()
#    print(data)

    return render_template(
        'main.html',
        data=data)

# --------------------------------------------------------------------------------

