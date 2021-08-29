from flask import Flask, jsonify
import requests
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os

app = Flask(__name__)
api = Api(app)
CORS(app)



def WordsAPIRequest(word):
    url = "https://wordsapiv1.p.rapidapi.com/words/{}".format(word)
    headers = {'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"}

    key = os.environ["WORDSAPIKEY"]
    headers['x-rapidapi-key'] = key
    response = requests.request("GET", url, headers=headers)
    freqResponse = requests.request("GET", url + '/frequency', headers=headers)
    print(response)
    print(freqResponse)

class GetWordData(Resource):
    def get(self, word):
        parser = reqparse.RequestParser()
        parser.add_argument('calculate', type=bool)
        args = parser.parse_args()

        if args['calculate']:
            parameters = WordsAPIRequest(word)


api.add_resource(GetWordData, '/getWord/<word>')

if __name__ == '__main__':
    app.run()