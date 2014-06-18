'''
Created on 21 juin 2011

@author: julien.bernard
'''
import unittest
from backtest.dispatcher import EventDispatcher

class MockEvent(object):
    type = 'TYPE'
    
class MockListener(object):
    
    def process_event(self, event):
        print 'Event dispatched'
    

class TestEventDispatcher(unittest.TestCase):


    def testHasListener(self):
        event_dispatcher = EventDispatcher()
        listener = MockListener()
        event_dispatcher._events['TYPE'] = [listener]
        
        response = event_dispatcher.has_listener('TYPE', listener)
        
        self.assertEqual(response, True, 'has a listener')
        
        # check with another object
        other_listener = MockListener()
        response = event_dispatcher.has_listener('TYPE', other_listener)
        
        self.assertEqual(response, False, 'does not have an other listener')
    
    def testAddEventListener(self):
        event_dispatcher = EventDispatcher()
        listener = MockListener()
        
        # check if impossible to add same object 2 times
        event_dispatcher.add_event_listener('TYPE', listener)
        event_dispatcher.add_event_listener('TYPE', listener)
        
        self.assertEqual(len(event_dispatcher._events['TYPE']), 1, 'good events map size')
        
        # check if possible to add another object
        other_listener = MockListener()
        event_dispatcher.add_event_listener('TYPE', other_listener)
        
        self.assertEqual(len(event_dispatcher._events['TYPE']), 2, 'good events map size after added one')
        
    def testDispatchEvent(self):
        event_dispatcher = EventDispatcher()
        listener = MockListener()
        event_dispatcher.add_event_listener('TYPE', listener)
        event = MockEvent()
        
        event_dispatcher.dispatch_event(event)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testHasListener']
    unittest.main()