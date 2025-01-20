from datetime import date

class Note:
    def __init__(self, code, text):
        # constructor for creating a note instance
        self.code = code
        self.text = text
        # timestamp found in note is only up to day, does not include hour/minute/second
        time_stamp = date.today()
        # time_stamp = datetime.timestamp(date_time)
        self.time_stamp = time_stamp
    
    def __repr__(self):
        return "Note code: %r, text: %s, timestamp: %r" % \
        (self.code, self.text, self.time_stamp)
    
    def __eq__(self, other):
        # note that two notes can be identically equal with the same timestamp, 
        # but they are not exactly identical since no two notes can have the same creation time
        return self.code == other.code and self.text == other.text and self.time_stamp == other.time_stamp