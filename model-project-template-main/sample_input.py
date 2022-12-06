def get_sample_by_no(number):
    if number == 1:
        sample = {
            'attendees':[
                {
                    'name':'adam', 
                    'avail': {
                        "2022-12-01":[
                            ['12:00:00','F'],
                            ['15:00:00','T']
                        ]
                    }
                }
            ],

            'activities':[
                {'name':'workout', 'duration': 3,'indoors': 'T'}
            ],

            'weather':{
                "2022-12-01":[
                    ['12:00:00','light rain', 'F'],
                    ['15:00:00', 'few clouds', 'T']
                ]
            }
        }

    return sample

if __name__ == "__main__":
    using_sample_input = input("Enter sample number to use sample input. For manual input, press Enter: ")
    if using_sample_input == "1":
        samples = get_sample_by_no(1)
        print(samples['attendees'])
    else:
        print('manual')

    xd = {
        'item1':'hi',
        'item2':'hi'
    }

    for count, val in enumerate(xd):
        print(count, val)
