from datetime import time
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf.operators import iff
import requests
import lettucemeet_scape2 as lettuce

def input_activities():
    print('Enter activities')
    activities = []
    finished_input = False
    while not finished_input:
        activity_name = input('Enter activity name: ').lower()
        activity_duration = int(input('Enter duration of activity in hours: '))
        activity_indoors = input('Is the activity indoors? Y/N: ').lower() == 'y'
        finished_input = input('Add another activity? Y/N: ').lower() == "n"

        activity = {
            'name': activity_name,
            'duration': activity_duration,
            'indoors': activity_indoors
        }

        activities.append(activity)
    
    return activities

def get_weather():
    apiKey = "7310dd5bc23c33461ad6d71f286c1f05"
    rootUrl = "http://api.openweathermap.org/data/2.5/forecast?"

    cityName = input("Enter Your City: ")

    url = f"{rootUrl}appid={apiKey}&q={cityName}"


    allWeather = requests.get(url).json()

    filtWeather = {}

    list = allWeather['list']

    for dict in list:
        weatherList = dict['weather']
        weatherDict = weatherList[0]
        tempValue = weatherDict['description']
        tempKey = dict['dt_txt']
        filtWeather[tempKey] = tempValue

    dayDict = {}
    for k, v in filtWeather.items():
        if k[:10] in dayDict.keys():
            dayDict[k[:10]].append([k[-9:], v])
        else:
            dayDict[k[:10]] = [[k[-9:], v]]

    for v in dayDict.values():
        for i in v:
            if i[-1][-4:] == 'rain':
                goodWeather = 'F'
            elif i[-1][-4:] == 'snow':
                goodWeather = 'F'
            else:
                goodWeather = 'T'

            i.append(goodWeather)

    return dayDict

# Encoding that will store all of constraints
E = Encoding()

#Activity Proposition


@proposition(E)
class ActivityPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

#Timing propositions
times = [0,3,6,9,12,15,18,21]

@proposition(E)
class TimingPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

#Indoors Proposition
indoor = ['T','F']

@proposition(E)
class IndoorsPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

# weather propositions
weather = ['T','F']

@proposition(E)
class WeatherPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

@proposition(E)
class ScheduledPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


#get input from user
people = lettuce.input_people()
activities = input_activities()
times = [] #range of available times
weather = get_weather()

print(people)
print(activities)
print(weather)

# for all activities, create propositions
x = []
for j in range(activities):
    x.append(ActivityPropositions("x"+j))

# for all times, create propositions
t = []
for i in range(people):
    for k in range(times):
        t.append(TimingPropositions("t"+i+"j"+k))

# for all activities indoor/outdoor status, create propositions
q = []
for j in range(activities):
    q.append(IndoorsPropositions("q"+j))

# for all weather conditions, create propositions
w = []
for k in range(times):
    w.append(WeatherPropositions("w"+k))

# for all scheduled, create propositions
s = []
for k in range(times):
    s.append(ScheduledPropositions("s"+k))

# CONSTRAINTS
def example_theory():

    # constraint verifying availabilities for each hour, setting true if a person is free, false otherwise
    for k in range(times):
        for i in range(people):
            if t[i,k] == 'free':
                E.add_constraint(t[i,k])
            else:
                E.add_constraint(~ t[i,k])

    # checks for availability and only holds if everyone is free at a given time
    availability = []
    for k in range(times):
        count = 0
        for i in range(people):
            if t[i,k] == True:
                count += 1
        if count == len(people):
            availability.append(True)
        else:
            availability.append(False)
    
    # constraint where if activity holds but weather does not, then activity is indoors
    for j in range(activity):
        for k in range(times):
            E.add_constraint((x[j] & ~ w[k]) => q[j])
            
    # constraint where if activity holds but is not indoors, then weather holds (is clear)
    for j in range(activity):
        for k in range(times):
            E.add_constraint((x[j] & ~ q[j]) => w[k])

    # constraint where activity holds iff there is availibility at given time & weather clear or indoor activity
    for j in range(activities):
        for k in range(times):
            E.add_constraint(iff(x[j], availability[k] & (w[k] | q[j])))

    # constraint where a scheduled slot is valid when only one event is scheduled at that given time
    for k in range(times):
        E.add_constraint(iff(s[j], x[0] & (~ x[1] & ~ x[2] & ... & ~ x[len(activities)])))

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()


# STEP ONE: CREATE LIST OF AVAILABLE TIMES FOR EVERYONE (not done at the moment)
#note: for large calander databases, can just find first time where everyone's available and suggest activity
