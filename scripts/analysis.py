from scripts.message import Message
import datetime

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

    def update_stats(self, message: Message):
        self["Weekday"][message.weekDayMessage] += 1
        # continue with other stuff

    def is_valid_message(self, line):
        '''
        Determines whether a line from the file is a valid message or the continuation of the previous message.
        A message is valid if the first characters are the date and the time of the message, otherwise it is the continuation
        of the previous message
        '''
        try: 
            if datetime.date(int(line[6:10]), int(line[3:5]), int(line[0:2])) and datetime.time(int(line[12:14]), int(line[15:17])):
                return True
        except:
            return False
    
    def __getitem__(self, st):
        if st in self.STATS.keys():
            return self.STATS[st]
        else:
            raise IndexError("Category not present in the stats.")

if __name__ == '__main__':
    a = Analysis()
    print(a["Weekday"])