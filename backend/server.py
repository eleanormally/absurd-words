from flask import Flask, jsonify
import requests
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import math

app = Flask(__name__)
api = Api(app)
CORS(app)



def WordsAPIRequest(word):
    url = 'https://wordsapiv1.p.rapidapi.com/words/{}'
    headers = {'x-rapidapi-host': 'wordsapiv1.p.rapidapi.com'}

    key = os.environ['WORDSAPIKEY']
    headers['x-rapidapi-key'] = key
    response = requests.request('GET', url.format(word), headers=headers).json()
    if 'success' in response and response['success'] == 'false':
        return 'Error: ' + response['message']
    freqResponse = requests.request('GET', url.format(word) + '/frequency', headers=headers).json()
    defintionLength = len(response['results'][0]['definition'].split())
    topSynonyms = response['results'][0]['synonyms']
    # remove multi word synonyms
    topSynonyms = [s for s in topSynonyms if len(s.split()) == 1]
    perMil = float(freqResponse['frequency']['perMillion'])
    averagePerMil = 0
    if len(topSynonyms) > 0:
        for s in topSynonyms:
            sResponse = requests.request('GET', url.format(s) + '/frequency', headers=headers).json()
            if 'success' in response and response['success'] == 'false':
                return 'Synonym Error: ' + response['message']
            averagePerMil += float(sResponse['frequency']['perMillion'])
        averagePerMil /= len(topSynonyms)
    else:
        averagePerMil = perMil
    return {
        'perMil': perMil,
        'dLength': defintionLength,
        'sPerMil': averagePerMil
    }

def calculateScore(perMil, dLength, sPerMil):
    return sPerMil/(math.log(perMil+1)*dLength)
class GetWordData(Resource):
    def get(self, word):
        parser = reqparse.RequestParser()
        parser.add_argument('calculate', type=bool)
        args = parser.parse_args()

        if args['calculate']:
            data = WordsAPIRequest(word)
            if type(data) == str:
                return '{{error: {message}}}'.format(message=data)
            score = calculateScore(data['perMil'], data['dLength'], data['sPerMil'])
            return {
                'score': score,
                'datapoints': {
                    'usesPerMillionWords': data['perMil'],
                    'definitionLength': data['dLength'],
                    'SynonymAverageUsesPerMillionWords': data['sPerMil']
                }
            }
        else:
            return '{message: "not in database"}'

api.add_resource(GetWordData, '/getWord/<word>')

if __name__ == '__main__':
    app.run()