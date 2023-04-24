import math
import numpy as np

class AD:
    """
    This class is used to represent functions and their variables for automatic differentiation.
    Only consider scalar for milestone2
    """
    
    def __init__(self, value, deriv=0., name = 'x'):
        
        '''
        The 'value' should be int or float, derivative should be int or float, and the name is a 'str'. 
        For this milestone, we only consider scalar input, so for the name attribute here, we just store the name of 'self' instance after the operations,
        and use default name attribute in the test file, which would be all 'x', but we will improve this part for next milestone.
        For the next milestone, we will store all the sorted unique variable names, like ['x','y','z'] and calculate their corresponding derivatives, like [[1,0,0],[0,1,0],[0,0,1]].      
        '''
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Invalid input type for value.')  
           
        if not isinstance(deriv, int) and not isinstance(deriv, float):
            raise TypeError('Invalid input type for derivative.')
        
        if not isinstance(name, str):
            raise TypeError('Invalid input type for value.') 
    
        self.value = value
        self.deriv = deriv 
        self.name = name
    
    
    def __str__(self):
        return f'Value is:{self.value}, derivative is:{self.deriv}, Name is:{self.name}'
    
    
    
    #Basic operations: addition, multiplication, subtraction, division, 
    #power with reverse modes, and unary operations like negation

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            value = self.value + other
            deriv = self.deriv
            name =  self.name   
            
        elif isinstance(other, AD):
            value = self.value + other.value
            deriv = self.deriv + other.deriv
            name =  self.name  # TODO: simply record the name of 'self' instance here, will adjust for future work 
        else:
            raise TypeError('Invalid input type.')
        
        return AD(value, deriv, name)
    
    
    def __radd__(self, other):
        return self.__add__(other)
    
    
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            value = self.value * other
            deriv = self.deriv * other
            name =  self.name  
            
        elif isinstance(other, AD):
            value = self.value * other.value
            deriv = self.deriv * other.value + self.value * other.deriv
            name =  self.name   # TODO: simply record the name of 'self' instance here, will adjust for future work 
        else:
            raise TypeError('Invalid input type.')
        
        return AD(value, deriv, name)
    
    
    def __rmul__(self, other):
        return self.__mul__(other)
 

    def __neg__(self):
        value = -1*self.value
        deriv = -1*self.deriv
        name = self.name  
        
        return AD(value, deriv, name)

    
    def __sub__(self, other):
        return self.__add__(-other)
    
    
    def __rsub__(self, other):
        return -(self.__sub__(other))
    
    
    def __truediv__(self, other):  #divisor can not be 0
        
        if isinstance(other, int) or isinstance(other, float): 
            if other ==0:
                raise ZeroDivisionError
            else:
                value = self.value / other
                deriv = self.deriv / other
                name = self.name
                
        elif isinstance(other, AD):
            if other.value == 0:
                raise ZeroDivisionError           
            else:
                value = self.value / other.value
                deriv = (self.deriv * other.value - other.deriv * self.value) / (other.value ** 2)
                name = self.name  # TODO: simply record the name of 'self' instance here, will adjust for future work 
               
        else:
            raise TypeError('Invalid input type.')
            
        return AD(value, deriv, name)
    
    
    def __rtruediv__(self, other):
        
        if self.value ==0:
            raise ZeroDivisionError        
        
        if (not isinstance(other, int)) and (not isinstance(other, float)): 
            raise TypeError('Invalid input type.')
        else:
            value = other / self.value
            deriv = -other * self.deriv / (self.value ** 2)
            name = self.name
            return AD(value, deriv, name)

    
    def __pow__(self, n):
        if isinstance(n, int) or isinstance(n, float):
            n = float(n)
            val = self.value
            if val < 0 and 0 < n < 1:
                raise ValueError('Illegal value and exponent')
            if val == 0 and n < 0:
                raise ZeroDivisionError
            if val == 0 and ((n == 1) or (n == 0)):
                raise ZeroDivisionError
                
            value = val** n
            deriv = n * self.deriv * (val ** (n - 1))
            name = self.name
            
        elif isinstance(n, AD):  # n is an AD object
            val_base = self.value
            val_exponent = n.value

            if val_base < 0 and 0 < val_exponent < 1:
                raise ValueError('Illegal value and exponent')
            if val_base == 0 and val_exponent < 0:
                raise ZeroDivisionError
            if val_base == 0 and ((val_exponent == 1) or (val_exponent == 0)):
                raise ZeroDivisionError
                
            value = val_base ** val_exponent
            deriv =  (n.deriv * np.log(val_base) + val_exponent * self.deriv / val_base) * value
            name = self.name  # TODO: simply record the name of 'self' instance here, will adjust for future work 
            
        else: 
            raise TypeError('Invalid Input Type for the exponent')
        
        return AD(value, deriv, name)
    
    
    def __rpow__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            if (other < 0):
                raise ValueError('Inconsistent value found for the base.')
            if other == 0 and self.value < 0:
                raise ZeroDivisionError
            if other == 0 and ((self.value == 1) or (self.value == 0)):
                raise ZeroDivisionError
            value = other ** self.value
            deriv = self.deriv * np.log(other) * value
            name = self.name
            return AD(value, deriv, name)

        else:
            raise TypeError('Invalid Input Type for the exponent')
            
            
    
    
    ##Elemental Functions
    def sin(self):
        value = np.sin(self.value)
        deriv = np.cos(self.value) * self.deriv
        return AD(value, deriv, self.name)
    
    
    def sinh(self):
        value = np.sinh(self.value)
        deriv = np.cosh(self.value) * self.deriv
        return AD(value, deriv, self.name)
    
    
    def arcsin(self):
        if (self.value < -1) or (self.value > 1):
            raise ValueError("Cannot take derivative of arcsin of value outside of range [-1, 1]")
        value = np.arcsin(self.value)
        deriv = self.deriv * ((1 - self.value ** 2) ** (-0.5))
        return AD(value, deriv, self.name)
    
    
    def cos(self):
        value = np.cos(self.value)
        deriv = -np.sin(self.value) * self.deriv
        return AD(value, deriv, self.name)
    
    
    def cosh(self):
        value = np.cosh(self.value)
        deriv = np.sinh(self.value) * self.deriv
        return AD(value, deriv, self.name)  
    
    
    def arccos(self):
        if self.value < -1 or self.value > 1:
            raise ValueError("Cannot take derivative of arcsin of value outside of range [-1, 1]")
        value = np.arccos(self.value)
        deriv = -self.deriv * ((1 - self.value ** 2) ** (-0.5))   
        return AD(value, deriv, self.name)
    
    
    def tan(self):
        if( ((self.value / np.pi) - 0.5) % 1 == 0.00 ):
            raise ValueError("Math error, Tangent cannot handle i*0.5pi ")
        value = np.tan(self.value)
        deriv = 1 / np.power(np.cos(self.value), 2) * self.deriv
        return AD(value, deriv, self.name)
 

    def tanh(self):
        value = np.tanh(self.value)
        deriv = (1 - (np.tanh(self.value))**2 )* self.deriv      
        return AD(value, deriv, self.name)
 

    def arctan(self):
        value = np.arctan(self.value)
        deriv = self.deriv * ((1 + self.value ** 2) ** (-1))
        return AD(value, deriv, self.name)
 

    def exp(self):
        value = np.exp(self.value)
        deriv = np.exp(self.value)*self.deriv
        return AD(value, deriv, self.name)
    
    
    def ln(self):
        if self.value <= 0:
            raise ValueError("Cannot take natural log of zero or negative values")
        value = np.log(self.value)
        deriv = self.deriv / self.value
        return AD(value, deriv, self.name)
    
    
    def ln_base(self, base):
        if self.value <= 0:
            raise ValueError("Cannot take log of zero or negative values")
        value = math.log(self.value,base)
        deriv = self.deriv / (self.value*np.log(base))  
        return AD(value, deriv, self.name) 
    
    
    def sqrt(self):
        return self.__pow__(0.5)
        
    
    def logistic(self):
        value = 1 / (1 + np.exp(-self.value))
        deriv = self.deriv * np.exp(-self.value) / ((1 + np.exp(-self.value)) ** 2)
        return AD(value, deriv, self.name) 
    
    
   