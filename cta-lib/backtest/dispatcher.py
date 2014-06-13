'''
Simple events dispatcher implementation. 
@author: julien.bernard
'''
import logging

class EventDispatcher(object):
    
    logger = logging.getLogger('EventDispatcher')
    
    def __init__(self):
        # Map event type and listeners
        self._events = {}
        
    def __del__(self):
        self._events = None
        
    def has_listener(self, event_type, listener):
        '''
        return true if event_type has a listener
        @param event_type: the type of event
        @param listener: the listener
        @return: true or false 
        '''
        
        if event_type in self._events:
            return listener in self._events[event_type]
        else:
            return False
        
    def add_event_listener(self, event_type, listener):
        '''
        add a listener to an event type
        @param event_type: the type of event
        @param listener: the listener 
        '''
        
        if not self.has_listener(event_type, listener):
            
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug('Adding listener for %s'%event_type)
                
            if event_type not in self._events:
                self._events[event_type] = []
                self._events[event_type].append(listener)
            else:
                listeners = self._events[event_type]
                listeners.append(listener)
                
    def dispatch_event(self,event):
        '''
        dispatch an event
        @param event: the event 
        '''
        
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Receive an event %s'%event.type) 
        
        if event.type in self._events:
            listeners = self._events[event.type]
            
            for listener in listeners:
                
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug('Dispatch an event %s'%event.type)
                
                listener.process_event(event)
        