from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

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

#for all activities indoor/outdoor status, create propositions
q = []
for j in range(activities):
    q.append(IndoorsPropositions("q"+j))

#for all weather conditions, create propositions
w = []
for k in range(times):
    w.append(WeatherPropositions("w"+k))

#for all scheduled, create propositions
s = []
for k in range(times):
    s.append(ScheduledPropositions("s"+k))

def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 

    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula

    # this doesn't work?!
    # E.add_constraint((x & y).negate())


    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

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