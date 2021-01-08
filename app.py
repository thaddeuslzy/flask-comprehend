from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

import boto3

comprehend = boto3.client('comprehend')

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sentiment', methods=['POST'])
def sentiment():
    req = request.get_json()
    if 'text' in req.keys():
        text = str(req['text'])
        res = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        del res['ResponseMetadata']
        sentiment = res['Sentiment']
        sentiment_score = res['SentimentScore']
        res = jsonify(res)
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    return "Error: no text specified"

if __name__ == '__main__':
    app.run()

