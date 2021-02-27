from flask import Flask, render_template, request
from mytools import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/password', methods=['POST', 'GET'])
def second():
    if request.method == "POST":
        if request.form.get("submit_a"):
            torneios = DataBase('', '', '', '', '', '', '', '', '')
            checklogs('https://freerollpasswords.com/poker/888poker/')
            checklogs('https://freerollpasswords.com/poker/pokerstars/')
            return render_template('password.html', torneios=torneios.ler())
    elif request.method == 'GET':
        return render_template('password.html')


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
