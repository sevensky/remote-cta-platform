'''
Created on 28 juin 2011

@author: julien.bernard
'''
import unittest
from numpy import cos, arctan
from finance.math.digital_filter import DigitalFilter

class TestDigitalFilter(unittest.TestCase):


    def testGetButterworthLpf(self):
        time = range(500)
        fundamental = 8*arctan(1)/30
        noise = 8*arctan(1)/4
        
        input = time[:]
        for t in time:
            input[t]=cos(fundamental*t) + cos(noise*t)
            
        output = DigitalFilter.get_butterworth_lpf(input, 20)

        self.assertEqual(len(input), len(output), 'good length')
        self.assertAlmostEqual(output[499], -0.89911731,msg='good Butterworth')

    def testGetBesselLpf(self):
        time = range(500)
        fundamental = 8*arctan(1)/30
        noise = 8*arctan(1)/4
        
        input = time[:]
        for t in time:
            input[t]=cos(fundamental*t) + cos(noise*t)
            
        output = DigitalFilter.get_bessel_lpf(input, 20)

        self.assertEqual(len(input), len(output), 'good length')
        self.assertAlmostEqual(output[499], -0.94269355,msg='good Bessel')
    
    def testGetChebyschevLpf(self):
        time = range(500)
        fundamental = 8*arctan(1)/30
        noise = 8*arctan(1)/4
        
        input = time[:]
        for t in time:
            input[t]=cos(fundamental*t) + cos(noise*t)
            
        output = DigitalFilter.get_chebyschev_lpf(input, 20)

        self.assertEqual(len(input), len(output), 'good length')
        self.assertAlmostEqual(output[499], -1.15550766,msg='good Chebyschev') 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetButterworthLpf']
    unittest.main()