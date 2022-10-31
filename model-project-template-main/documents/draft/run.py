from datetime import time
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf.operators import iff

#will be done graphically in final project
def input_people():
    print('Enter people')
    people = []
    finished_input = False
    while not finished_input:
        person_name = input('Enter person\'s name: ').lower()
        person_avail = input('Enter person\'s availability: ') #done through calendar 
        finished_input = input('Add another person? Y/N: ').lower() == "n"

        person = {
            'name': person_name,
            'avail': person_avail
        }

        people.append(person)
    
    return people

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

# Encoding that will store all of constraints
E = Encoding()

@proposition(E)
class ActivityPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

@proposition(E)
class TimingPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

@proposition(E)
class IndoorsPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

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
people = input_people()
activities = input_activities()
times = [] #range of available times

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

    # constraint where activity holds iff there is availibility at given time & weather clear or indoor activity
    for j in range(activities):
        for k in range(times):
            E.add_constraint(iff(x[j], availability[k] & (w[k] | q(j))))

    # constraint where a scheduled slot is valid when only one event is scheduled at that given time
    for k in range(times):
        E.add_constraint(iff(s[j], x[0] | x[1] | ... | x[len(activities)]))

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
