import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select


app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/spanish_vocab'
db = SQLAlchemy(app)


class Noun(db.Model):
    __tablename__ = 'nouns'
    id = db.Column('ID', db.Integer, primary_key=True)
    spanish = db.Column('spanish', db.Unicode)
    english = db.Column('english', db.Unicode)
    phrase = db.Column('phrase', db.Unicode)


class Adj(db.Model):
    __tablename__ = 'adjectives'
    id = db.Column('ID', db.Integer, primary_key=True)
    spanish = db.Column('spanish', db.Unicode)
    english = db.Column('english', db.Unicode)
    phrase = db.Column('phrase', db.Unicode)


class Prep(db.Model):
    __tablename__ = 'prepositions'
    id = db.Column('ID', db.Integer, primary_key=True)
    spanish = db.Column('spanish', db.Unicode)
    english = db.Column('english', db.Unicode)
    phrase = db.Column('phrase', db.Unicode)


class Table:
    def __init__(self):
        self.current_table = None
        self.listOfWords = []

    def getTranslation(self, word):
        return tables[self.current_table].query.filter(
            tables[self.current_table].spanish == word).one().english

    def checkDuplicates(self, word):
        if not (word in self.listOfWords):
            self.listOfWords.append(word)
        else:
            self.checkDuplicates(self.randomWord())

    def randomWord(self):
        return tables[self.current_table].query.order_by(
            func.rand()).limit(1).one()


tables = {"Noun": Noun,
          "Adj": Adj,
          "Pre": Prep
          }

table = Table()


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        translation = request.form['trans']
        previousSpanish = request.args.get('prevS')
        previousEnglish = table.getTranslation(previousSpanish)
        if previousEnglish == translation:
            check = True
        else:
            check = False
        spanishObj = table.randomWord()
        table.checkDuplicates(spanishObj.spanish)
        print(table.listOfWords)
        return render_template('index.html', translation=translation, word=spanishObj, check=check, previousSpanish=previousSpanish, previousEnglish=previousEnglish, select=table.current_table)
    else:
        if 'mode' in request.args:
            table.current_table = request.args.get('mode')
        else:
            table.current_table = "Noun"
        spanishObj = table.randomWord()
        table.checkDuplicates(spanishObj.spanish)
        return render_template('index.html', word=spanishObj, select=table.current_table)


# @app.route('/', methods=['POST','GET'])
# def index():
#     if request.method == 'POST':
#         translation = request.form['trans']
#         return jsonify(({
#         'status': 'success',
#         'translation': translation
#     }))
#     else:
#         return render_template('index.html')

if __name__ == 'main':
    app.run(debug=True)
