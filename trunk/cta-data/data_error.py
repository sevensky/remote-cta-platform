'''
Data error, exception on data layer
@author: julien.bernard
'''

class DataError(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
