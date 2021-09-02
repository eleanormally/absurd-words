from flask import Flask, jsonify
import requests
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import math
import psycopg2
import json

app = Flask(__name__)
api = Api(app)
CORS(app)



def WordsAPIRequest(word):
    url = 'https://wordsapiv1.p.rapidapi.com/words/{}'
    headers = {'x-rapidapi-host': 'wordsapiv1.p.rapidapi.com'}

    key = os.environ['WORDSAPIKEY']
    headers['x-rapidapi-key'] = key
    response = requests.request('GET', url.format(word), headers=headers).json()
    if 'success' in response and response['success'] == False:
        return 'Error: ' + response['message']
    freqResponse = requests.request('GET', url.format(word) + '/frequency', headers=headers).json()
    defintionLength = len(response['results'][0]['definition'].split())
    if 'frequency' in freqResponse:
        perMil = float(freqResponse['frequency']['perMillion'])
    else:
        perMil = 0.0001
    averagePerMil = 0
    if 'synonyms' in response['results'][0]:
        topSynonyms = response['results'][0]['synonyms']
        # remove multi word synonyms
        topSynonyms = [s for s in topSynonyms if len(s.split()) == 1 and s.isalpha()]
        if len(topSynonyms) > 0:
            for s in topSynonyms[:3]:
                sResponse = requests.request('GET', url.format(s) + '/frequency', headers=headers).json()
                if 'success' in response and response['success'] == 'false':
                    return 'Synonym Error: ' + response['message']
                print(sResponse)
                if 'frequency' in sResponse:
                    averagePerMil += float(sResponse['frequency']['perMillion'])
            averagePerMil /= len(topSynonyms)
        else:
            averagePerMil = 1
    else:
        averagePerMil = 1
    return {
        'perMil': perMil,
        'dLength': defintionLength,
        'sPerMil': averagePerMil
    }

def calculateScore(perMil, dLength, sPerMil):
    return sPerMil/(math.log(perMil+1)*dLength)

def addWordToDatabase(data):
    conn = None

    try:
        conn = psycopg2.connect(
            os.environ['DATABASE_URL'],
            sslmode='require'
        )
        cur = conn.cursor()


        query = 'INSERT INTO words (word, score, datapoints) VALUES({},{},{})'.format(data['word'], data['score'], json.dumps(data['datapoints']))
        cur.execute(
          query
        )


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
          return valInDatabase

        elif args['calculate']:
            data = WordsAPIRequest(word)
            if type(data) == str:
                return '{{error: {message}}}'.format(message=data)
            score = calculateScore(data['perMil'], data['dLength'], data['sPerMil'])
            calculatedResult = {
                'word': word,
                'score': score,
                'datapoints': {
                    'usesPerMillionWords': data['perMil'],
                    'definitionLength': data['dLength'],
                    'SynonymAverageUsesPerMillionWords': data['sPerMil']
                }
            }
            addWordToDatabase(calculatedResult)
            return calculatedResult

        else:
            return '{message: "not in database"}'

class TopWords(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sortBy', type=str)
        parser.add_arg

api.add_resource(GetWordData, '/getWord/<word>')

if __name__ == '__main__':
    app.run()
