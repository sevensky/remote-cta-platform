'''
Exception of core layer
@author: julien
'''
class CoreError(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message