# Run : $ python -m flask --app app.py --debug run
# Import google credential


import googleapiclient.discovery as connect
import pandas as pd
import seaborn as sns
import urllib.request as server
# import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

api = 'AIzaSyAQo0zutTNb6nXiuYSJ9_p_Pjx5mr1nHBw'  # API SOFYAN
youtube = connect.build('youtube', 'v3', developerKey=api)


def getChannelID(url, file='result.txt'):
    # if url is not a channel url, then return None
    if 'youtube.com/@' not in url:
        return None

    server.urlretrieve(url, file)
    with open(file, 'r', encoding="utf-8") as f:
        for line in f:
            if '"channelId":' in line:
                channel_id = line.split('"channelId":')[1].split(':')[0].strip('"')
                channel_id = channel_id[:-8]

                # Split whenever there is a comma
                channel_id = channel_id.split(',')
                channel_id = channel_id[0]
                channel_id = channel_id.replace('"', '')

                return channel_id

def getChannelStat(url, file='statistic.txt'):
    server.urlretrieve(url, file)
    copy = False
    data = []
    with open(file, 'r', encoding="utf-8") as f:
        # read from '"statistics": ' to '}'
        for line in f:
            if line.strip() == '"statistics": {':
                copy = True
                continue
            elif line.strip() == '}':
                copy = False
                continue
            elif copy:
                line = line.replace("'", "").replace(",", "").replace("\"", "")
                data.append(line.strip())

        return data


def requestFrom(channel_id, api):
    reqUrl = []
    x = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id="
    y = "&key="
    reqUrl.append(x)
    reqUrl.append(channel_id)
    reqUrl.append(y)
    reqUrl.append(api)
    reqUrl = ''.join(reqUrl)
    return reqUrl


def fitData(variable, value):
    if variable > value:
        return 1
    else:
        return 0

def getChannelName(url):
    url = url.split('@')[1]
    url = url.split('/')[0]
    return url

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        channel_url = request.form['input_url']

        if channel_url == '':
            return render_template('index.html', prediction_text='Please input a channel URL!', x='false')


        channel_name = getChannelName(channel_url)
        channel_id = getChannelID(channel_url, 'data/result.txt')

        if channel_id is None:
            return render_template('index.html', prediction_text='This is not a channel URL!', x='false')

        data = getChannelStat(
            requestFrom(channel_id, api), 
            'data/statistic.txt'
        )

        result = []

        # Debugging ~
        # print('Debug >\nData: ', data,  '\nID: ', channel_id, '\nURL: ', channel_url)
        # exit()

        # Cleaning the data
        views = data[0].split(':')[1]
        result.append(views) # Index 0 - Views
        view = fitData(int(views), 100000000)

        subs = data[1].split(':')[1]
        result.append(subs) # Index 1 - Subscribers
        subs = fitData(int(subs), 5000000)

        videos = data[3].split(':')[1]
        result.append(videos) # Index 2 - Videos
        videos = fitData(int(videos), 350)

        # Convert result array with formatter ','
        result = [format(int(i), ',d') for i in result]

        df = pd.DataFrame({'Videos': [videos], 'Subscribers': [subs], 'Views': [views]})

        # Split the test data y using views
        test_df = df.drop('Views', axis=1)

        # use the model to predict the input
        model = pd.read_pickle('data/model.pkl')
        prediction = model.predict(test_df)

        # if prediction is 1, then the channel is a Good Channel
        if (prediction == 1 & subs == 1 & videos == 1) | (view == 1 | subs == 1 | videos == 1) | (videos == 0 & subs == 1):
            return render_template( 
                'index.html', 
                prediction_text='This channel is a Good Channel',
                name=channel_name,
                indicator='green', 
                result=result,
                x='true')
        else:
            return render_template(
                'index.html', 
                prediction_text='This channel is not a Good Channel', 
                name=channel_name,
                result=result, 
                indicator='red',
                x='true')

    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)


