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
                        ],
                        "2022-12-02":[
                            ['12:00:00','T'],
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
                ],
                '2022-12-02': [
                    ['12:00:00','light rain', 'F'],
                    ['15:00:00', 'few clouds', 'T']
                ]
            }
        }

    return sample

if __name__ == "__main__":
    # using_sample_input = input("Enter sample number to use sample input. For manual input, press Enter: ")
    # if using_sample_input == "1":
    #     samples = get_sample_by_no(1)
    #     print(samples['attendees'])
    # else:
    #     print('manual')

    samples = get_sample_by_no(1)

    # weather props
    time_idx = 0
    for date in samples['weather']:
        for time in samples['weather'][date]:
            print(time_idx, time)
            time_idx += 1

            #Assume WeatherProp(date, time, index, is_clear)
            #PROPS.append(WeatherProp(date, time[0], idx, time[2] == 'T'))
    
    # timing props
    time_idx = 0
    for personidx, person in enumerate(samples['attendees']):
        for date in person['avail']:
            for time in person['avail'][date]:
                print(time_idx, time)
                time_idx += 1

                # Assume TimingProp(date, time, time_index, person, is_available)
                #PROPS.append(TimingProp(date, time[0], time_idx, personidx, time_idx[1]))

    # indoor/outdoor props
    for idx, activity in enumerate(samples['activities']):
        print(idx, activity)

        # Assume IndoorsProps(activity_name, activity_index, is_indoors)
        #PROPS.append(IndoorsProps(activity['name'], activity['indoors'] = True))
