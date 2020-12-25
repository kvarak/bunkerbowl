import os
from flask import Flask, request, render_template, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

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


@app.route('/')
def index():
    # reset data
    sheet = client.open_by_key('1v7QeeAKkV0y7GNDfpZntD4242YPo9jTeB-xLYjuLrFI').worksheet("games")
    all_values = sheet.get_all_values()
    # All session['questions']
    return render_template('base.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    all_values = sheet.get_all_values()
    if request.method == 'GET':
        session['current_values'] = [[int(i[0]),0] for i in all_values[1:]]
        session['questions'] = all_values[0][7:-1]

        question_index = random.randint(0, len(session['questions'])-1)
        question = session['questions'][question_index]

        return render_template('quiz.html', q = question, qi = question_index, cv = len(session['current_values']))

    elif request.method == 'POST':
        answered_index = int(request.values.get('qi'))
        session['questions'][answered_index] = "-"

        answer = int(request.values.get('result'))
        if answer == 0:
            session['current_values'] = [i for i in session['current_values'] if all_values[i[0]][answered_index+7] != "0"]
        elif answer == 1:
            session['current_values'] = [[i[0],i[1]+1] if all_values[i[0]][answered_index+7] != "0" else [i[0],i[1]] for i in session['current_values']]
        elif answer == 2:
            session['current_values'] = session['current_values']
        elif answer == 3:
            session['current_values'] = [[i[0],i[1]+1] if all_values[i[0]][answered_index+7] != "2" else [i[0],i[1]] for i in session['current_values']]
        elif answer == 4:
            session['current_values'] = [i for i in session['current_values'] if all_values[i[0]][answered_index+7] != "2"]

        # sort the list in point order
        newlist = [[all_values[i[0]][1] + " - " + all_values[i[0]][2], i[1]] for i in session['current_values']]
        newlist.sort(key=lambda x: x[1], reverse = True)

        question_index = random.randint(0, len(session['questions'])-1)
        while session['questions'][question_index] == "-":
            question_index = random.randint(0, len(session['questions'])-1)
            if ''.join(session['questions']) == "-" * len(session['questions']):
                return render_template('quiz.html', a = newlist, v = answer, cv = len(session['current_values']))

        question = session['questions'][question_index]

        return render_template('quiz.html', allq = session['questions'], q = question, qi = question_index, a = newlist, v = answer, cv = len(session['current_values']))
