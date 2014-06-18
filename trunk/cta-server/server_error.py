'''
Error on web service side
@author: julien
'''

class ServerError(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message