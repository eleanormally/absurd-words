from flask import Flask, jsonify
import requests
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import math
import psycopg2
import json
from nltk.corpus import wordnet as wn
import nltk

app = Flask(__name__)
api = Api(app)
CORS(app)


def calculateWordScore(word):
    
    #Phonemic Humour
    h = 0
    with open('letter_freq.json', 'r') as file:
      freq = json.loads(file.read())
    for l in word:
      h += freq[l]*math.log(freq[l], 2)
    h /= -1*len(word)

    #Word Utilization
    freqResp = requests.get("https://books.google.com/ngrams/json?content={}&year_start=1990&year_end=2019&corpus=26&smoothing=3".format(word)).json()[0]
    t = 0
    for n in freqResp['timeseries']:
      t += float(n)
    t /= len(freqResp['timeseries'])
    u = -math.log(t)

    #Word Ambiguity
    synsets = wn.synsets(word)
    q = 0
    for syn in synsets:
      q += len(syn.lemmas())
    
    #Related Word Abundance

    h1 = 0
    h2 = 0
    for syn in synsets:
      hyponyms = syn.hyponyms()
      h1 += len(hyponyms)
      for nym in hyponyms:
        h2 += len(nym.hyponyms())
    
    a = math.log(1+h1) + 0.5*math.log(1+h2)


    score = u*(1+(q-h+0.5*a)/100)

    return {
      'word': word,
      'score': score,
      'humour': h,
      'ambiguity': q,
      'relatives': a,
      'utilization': u
    }


def addWordToDatabase(data):
    conn = None

    try:
        conn = psycopg2.connect(
            os.environ['DATABASE_URL'],
            sslmode='require'
        )
        cur = conn.cursor()


        cur.execute('INSERT INTO words (word, score, humour, ambiguity, relatives, utilization) VALUES(%s, %s, %s, %s, %s, %s)', (data['word'], data['score'], data['humour'], data['ambiguity'], data['relatives'], data['utilization']))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def CheckExistingWord(word):
    conn = None

    try:
        conn = psycopg2.connect(
            os.environ['DATABASE_URL'],
            sslmode='require'
        )
        cur = conn.cursor()

        cur.execute(
          'SELECT * FROM words WHERE word = \'{}\''.format(word)
        )

        return cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

class GetWordData(Resource):
    def get(self, word):
        parser = reqparse.RequestParser()
        parser.add_argument('calculate', type=bool)
        args = parser.parse_args()

        valInDatabase = CheckExistingWord(word)
        if valInDatabase is not None:
          return {
            'word': word,
            'score': valInDatabase[1],
            'humour': valInDatabase[2],
            'ambiguity': valInDatabase[3],
            'relatives': valInDatabase[4],
            'utilization': valInDatabase[5]
          }

        elif args['calculate']:
            synsets = wn.synsets(word)
            if len(synsets) == 0:
                return '{error: word not found in Wordnet}'
            calculatedData = calculateWordScore(word)
            addWordToDatabase(calculatedData)
            return calculatedData

        else:
            return '{message: "not in database"}'

def getTopWords(method, rNum, offset):
  conn = None

  switcher = {
    'score': 'score',
    'scoreInverse': 'score desc',
    'a-z': 'word',
    'z-a': 'word desc',
    'humour': 'humour',
    'humourInverse': 'humour desc',
    'util': 'utilization',
    'utilInverse': 'utilization desc'
  }
  sort = switcher.get(method, 'invalid')
  if sort == 'invalid':
    return 'invalid'
  else: 
    try: 
        conn = psycopg2.connect(
            os.environ['DATABASE_URL'],
            sslmode='require'
        )
        cur = conn.cursor()
        cur.execute(
          'SELECT * FROM public.words ORDER BY {} OFFSET {} LIMIT {}'.format(sort, offset, rNum)
        )
        return cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if conn is not None:
            conn.close()

class TopWords(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sortMethod', type=str, default='score')
        parser.add_argument('results', type=int, default=20)
        parser.add_argument('startIndex', type=int, default=0)
        args = parser.parse_args()
        unparsed = getTopWords(args['sortMethod'], args['results'], args['startIndex'])
        parsed = [{ 'word': result[0], 'score': result[1], 'humour': result[2], 'ambiguity': result[3], 'relatives': result[4], 'utilization': result[5] }for result in unparsed ]
        return {'status': 'success', 'results': parsed}


api.add_resource(GetWordData, '/getWord/<word>')
api.add_resource(TopWords, '/words')

nltk.download('wordnet')

if __name__ == '__main__':
    app.run()
