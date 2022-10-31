import json
import requests

apiKey = "7310dd5bc23c33461ad6d71f286c1f05"
rootUrl = "http://api.openweathermap.org/data/2.5/forecast?"

cityName = input("Enter Your City: ")

url = f"{rootUrl}appid={apiKey}&q={cityName}"


allWeather = requests.get(url).json()

filtWeather = {}

count = 0

list = allWeather['list']

for dict in list:
    weatherList = dict['weather']
    weatherDict = weatherList[0]
    tempValue = weatherDict['description']
    tempKey = dict['dt_txt']
    filtWeather[tempKey] = tempValue

dayDict = {}
for k, v in filtWeather.items():
    if k[:10] == '2022-10-31':
        if k[:10] in dayDict.keys():
            dayDict[k[:10]].append([k[-9:], v])
        else:
            dayDict[k[:10]] = [[k[-9:], v]]
    elif k[:10] == '2022-11-01':
        if k[:10] in dayDict.keys():
            dayDict[k[:10]].append([k[-9:], v])
        else:
            dayDict[k[:10]] = [[k[-9:], v]]
    elif k[:10] == '2022-11-02':
        if k[:10] in dayDict.keys():
            dayDict[k[:10]].append([k[-9:], v])
        else:
            dayDict[k[:10]] = [[k[-9:], v]]
    elif k[:10] == '2022-11-03':
        if k[:10] in dayDict.keys():
            dayDict[k[:10]].append([k[-9:], v])
        else:
            dayDict[k[:10]] = [[k[-9:], v]]
    elif k[:10] == '2022-11-04':
        if k[:10] in dayDict.keys():
            dayDict[k[:10]].append([k[-9:], v])
        else:
            dayDict[k[:10]] = [[k[-9:], v]]



print(dayDict)
