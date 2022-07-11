class Analysis:

    STATS = {
        # Keeps track of the days in which the conversations happen
        "Weekday": {
            "Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday": 0
        },

        # Keeps track of the time at which the conversations happen
        "Time": {

        },

        # Keeps track of the number of conversations started by each participant
        "Started": {

        },

        # keeps track of the average message length for each user
        "AveLength": {

        },

        # keeps track of the types of each message
        "Type":{

        },

        # Keeps track of how many messages were sent on each day
        "Days": {

        }
    }

if __name__ == '__main__':
    a = Analysis()
    print(a.STATS["Weekday"])