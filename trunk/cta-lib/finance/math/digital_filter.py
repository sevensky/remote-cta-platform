'''
Compute a digital filter
@author: julien.bernard
'''
from numpy import arctan

class DigitalFilter(object):
    
    @staticmethod
    def _get_w_c(period):
        # return the angular frequency related to a period
        return 8*arctan(1)/period
    
    @staticmethod
    def get_butterworth_lpf(input, period):
        '''
        compute and return a two poles digital Butterworth low pass filter
        @param input: the input
        @param w_c: the cut frequency 
        @return: the output 
        '''
        
        output = input[:]
        for i in range(2,len(input)):
            output[i] = DigitalFilter.get_butterworth_lpf_value(period, input[i], input[i-1], input[i-2], output[i-1], output[i-2])
        
        return output 
            
    @staticmethod
    def get_butterworth_lpf_value(period, input_0, input_1, input_2, output_1, output_2):
        '''
        return the Butterworth filter new output
        @param period: the cut period
        @param input_0: input t
        @param input_1: input t-1
        @param input_2: input t-2
        @param output_1: output t-1
        @param output_2: output t-2
        @return: the new output      
        '''
        w_c = DigitalFilter._get_w_c(period)
        
        numerator = (w_c**2+2**1.5*w_c+4)
        a_0 = w_c**2/numerator
        a_1 = 2*a_0
        a_2= a_0
        b_1=(2*w_c**2-8)/numerator
        b_2=(w_c**2-2**1.5*w_c+4)/numerator
        
        return a_0*input_0+a_1*input_1+a_2*input_2-b_1*output_1-b_2*output_2
    
    @staticmethod
    def get_bessel_lpf(input, period):
        '''
        compute and return a two poles digital Bessel low pass filter
        @param input: the input
        @param w_c: the cut frequency
        @return: the output 
        '''
        output = input[:]
        for i in range(2,len(input)):
            output[i] = DigitalFilter.get_bessel_lpf_value(period, input[i], input[i-1], input[i-2], output[i-1], output[i-2])
        
        return output
    
    @staticmethod
    def get_bessel_lpf_value(period, input_0, input_1, input_2, output_1, output_2):
        '''
        return the Bessel filter new output
        @param period: the cut period
        @param input_0: input t
        @param input_1: input t-1
        @param input_2: input t-2
        @param output_1: output t-1
        @param output_2: output t-2
        @return: the new output      
        '''
        w_c = DigitalFilter._get_w_c(period)
        
        numerator = (3*w_c**2+6*w_c+4)
        a_0 = 3*w_c**2/numerator
        a_1 = 2*a_0
        a_2= a_0
        b_1=(6*w_c**2-8)/numerator
        b_2=(3*w_c**2-6*w_c+4)/numerator
        
        return a_0*input_0+a_1*input_1+a_2*input_2-b_1*output_1-b_2*output_2
    
    @staticmethod
    def get_chebyschev_lpf(input, period):
        '''
        compute and return a two poles digital Chebyschev low pass filter
        @param input: the input
        @param w_c: the cut frequency
        @return: the output 
        '''
        output = input[:]
        for i in range(2,len(input)):
            output[i] = DigitalFilter.get_chebyschev_lpf_value(period, input[i], input[i-1], input[i-2], output[i-1], output[i-2])
        
        return output
    
    @staticmethod
    def get_chebyschev_lpf_value(period, input_0, input_1, input_2, output_1, output_2):
        '''
        return the Chebyschev filter new output
        @param period: the cut period
        @param input_0: input t
        @param input_1: input t-1
        @param input_2: input t-2
        @param output_1: output t-1
        @param output_2: output t-2
        @return: the new output      
        '''
        w_c = DigitalFilter._get_w_c(period)
        
        numerator = (w_c**2+2*w_c+4)
        a_0 = w_c**2/numerator
        a_1 = 2*a_0
        a_2= a_0
        b_1=(2*w_c**2-8)/numerator
        b_2=(w_c**2-2*w_c+4)/numerator
        
        return a_0*input_0+a_1*input_1+a_2*input_2-b_1*output_1-b_2*output_2