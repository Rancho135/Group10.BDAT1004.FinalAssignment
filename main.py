from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from plotly.graph_objs import Scattergeo, Layout
import plotly.graph_objects as go
from plotly import offline
from plotly.graph_objs import Bar, Layout
import logging
import json

import pandas as pd
import plotly
import plotly.express as px

from output_data import get_weather
from api_to_db import api_to_db
#from chat1 import chat1

app = Flask('app')


@app.route('/')
def index():
    try:

        output = get_weather()
        data = list(output.find({}, {'_id': False}))
        #Save file in json format
        with open("output.json", "w") as outfile:
            json.dump(data, outfile)

        get_api_data = api_to_db()

        pass
    except AttributeError:
        pass

    return render_template("index.html")


@app.route('/chart1')
def chart1():
    filename1 = 'output.json'

    with open(filename1) as file_object:
        all_eq_data = json.load(file_object)

        #Building a world map
    temperatures, long, lats = [], [], []
    for eq_dict in all_eq_data:

        #Extracting the location using lons and lats
        temp = eq_dict['main']['temp']
        lon = eq_dict['coord']['lon']
        lat = eq_dict['coord']['lat']
        temperatures.append(temp)
        long.append(lon)
        lats.append(lat)

        #print(temperatures)

    my_layout = Layout(title='CITIES TEMPERATURES')

    data = [{
        'type': 'scattergeo',
        'lon': long,
        'lat': lats,
        'marker': {
            'size': [0.05 * temmp for temmp in temperatures],
            'color': temperatures,
            'colorscale': 'Plasma',
            'reversescale': True,
            'colorbar': {
                'title': 'Temperature in Kelvin'
            },
        }
    }]
    #using
    fig1 = {'data': data, 'layout': my_layout}

    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    header1 = "Cities Temperature"
    description1 = """
    Cities Temperature in Kelvin 
    """

    #chart 2 starts from here

    montreal_dic = {}  #creating a dictionary

    montreal_dic = all_eq_data[1]

    windsppeed = []  #creating a list

    windsppeed = montreal_dic["wind"]["speed"]  #extracting wind and speed
    #creating a gauge chart
    data_mont = [
        go.Indicator(mode="gauge+number",
                     value=windsppeed,
                     domain={
                         'x': [0, 1],
                         'y': [0, 1]
                     },
                     title={'text': "Montreal Wind Speed in Km/H "})
    ]

    fig2 = {'data': data_mont}

    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    header2 = "Montreal Wind Speed"
    description2 = """
    Montreal Wind Speed in Km/H
    """

    #Chart 3 starts from here

    weather_descs = []  #opening an empty list
    frequencies = {}  #opening an empty dictionary

    for eq_dict in all_eq_data:

        weather_desc = eq_dict['weather'][0]['description']
        weather_descs.append(weather_desc)
    #print(weather_descs)
    for item1 in weather_descs:
        # checking the element in dictionary
        if item1 in frequencies:
            # incrementing the count
            frequencies[item1] += 1
        else:
            # initializing the count
            frequencies[item1] = 1

    #Extracting keys and value of weat and ffee
    key = frequencies.keys()
    value = frequencies.values()

    w, f = [], []
    for keys in key:
        w.append(keys)

    for valuess in value:
        f.append(valuess)

    data_1 = [{
        'type': 'bar',
        'x': w,
        'y': f,
    }]

    my_layout_1 = {
        'title': "Unique Weather Descriptions and frequencies",
        'xaxis': {
            'title': 'Descriptions of Unique Weather'
        },
        'yaxis': {
            'title': 'frequencies'
        },
    }

    fig3 = {'data': data_1, "layout": my_layout_1}

    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    header3 = "Unique Weather Conditions"
    description3 = """
   Unique Weather Descriptions in Canadian Cities
    """

    #storing temperature, long, lats and humidity in an empty list
    Temperatures, long, lats, humidity = [], [], [], []
    for eq_dict in all_eq_data:
        #Extracting data in all_eq_data
        temmp = eq_dict['main']['temp']
        lon = eq_dict['coord']['lon']
        lat = eq_dict['coord']['lat']
        hum = eq_dict['main']['humidity']
        temperatures.append(temmp)
        long.append(lon)
        lats.append(lat)
        humidity.append(hum)

    #plot
    my_layout1 = Layout(title='CITIES HUMIDITY')

    data1 = [{
        'type': 'scattergeo',
        'lon': long,
        'lat': lats,
        'marker': {
            'size': [0.25 * humi for humi in humidity],
            'color': humidity,
            'colorscale': 'Turbo',
            'reversescale': True,
            'colorbar': {
                'title': 'Humidity level (grams per meter cubic)'
            },
        }
    }]

    fig4 = {'data': data1, 'layout': my_layout1}

    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    header4 = "Canada Citys Humidities"
    description4 = """
    Canada Citys Humidity level (grams per meter cubic) 
    """

    return render_template(
        'notdash2.html',
        graphJSON1=graphJSON1,
        graphJSON2=graphJSON2,
        graphJSON3=graphJSON3,
        graphJSON4=graphJSON4,
        header1=header1,
        description1=description1,
        header2=header2,
        description2=description2,
        header3=header3,
        description3=description3,
        header4=header4,
        description4=description4,
    )


app.run(host='0.0.0.0', port=8080)
