import numpy as np
import math

class ADReverse:
    '''
    This class is used for Automatic Differentiation in Reverse Mode.
    
    Every variable will be initiated as an ADReverse with its value.
    
    Two ADReverse instances could carry out many basic operations, and elemetanry functions if following the instuction of each function below.
    
    After each operation, we get a new ADReverse instance, which will store the new value, as well as references to its two children ADReverse instances,
    and their corresponding local derivatives according to that simple operation.
    
    At the end, when we implemente the whole function, we will get a final ADReverse object representing this function,
    and then we could get values using function "get_values([func1,func2...])",
    and get Jocabian using function "get_gradients([func1,func2,...], [x,y,....])"
    
    In the Jocabian calculation, we go through the graph from parent to children recursively, 
    multiply the local derivatives together and store each possible ADReverse object's derivatives in a dictionary.
    
    See more details in each function below.
       
    
    || ADReverse Class || 
    =====================
    
    Parameters
    ==========
    value:  (int or float) store this ADReverse obeject's value   
            eg: x = ADReverse(3)
    
    local_gradients: (tuple) store this ADReverse obeject's two children objects and their corresponding local derivatives             
            When we are intiating an ADReverse instance for a variable at the begining, we could use its default value as an empty tuple
            eg: x = ADReverse(3) , x.local_gradients == ()
                       
            After we carry out operations, it would be a tuple of two tuples which store the information of its children objects
            eg: ADReverse(3, ((child1, local_derivative1), (child2, local_derivative2)))
                
                    
    Attributes:  
    ==========
    value:  store this ADReverse obeject's value
            eg: x.value = 3 (int or float)    
    
    local_gradients: store this ADReverse obeject's two children objects and their corresponding local derivatives
            eg: x.local_gradients = ((child1, local_derivative1), (child2, local_derivative2))
    
    
    Examples: 
    ==========           
    #Scalar input (x) 

        # create ADReverse object for each variable, the argument is its value
        x = ADReverse(3) 

        # construct the function
        func = x*2 + 3  

        #get values: put functions in a list
        get_values([func])
        >>> array([[9]])

        #get Derivative: put functions in a list, 
        # and put the variables of which you want to see the derivatives in a list
        get_gradients([func], [x])
        >>> array([[2]])


    #Vector input (x,y)

        # create ADReverse object for each variable, the argument is its value
        x = ADReverse(3) 
        y = ADReverse(2) 

        # construct the function
        func = x*2 + x*y 

        #get values: put functions in a list
        get_values([func])
        >>> array([[12]])

        #get Derivative: put functions in a list, 
        # and put the variables of which you want to see the derivatives in a list
        get_gradients([func], [x,y])
        >>> array([[4, 3]])  
        # the order of derivatives is corresponding to the variable order you entered [x,y]


    # Vector input (x,y) and Vector output (f1,f2)

        # create ADReverse object for each variable, the argument is its value
        x = ADReverse(3) 
        y = ADReverse(2) 

        # construct the function
        func1 = x*2 + x*y 
        func2 = x + y**2

        #get values: put functions in a list
        get_values([func1,fun2])
        >>> array([[12],
                   [ 3]])
        # Each row is the value of one function, which is corresponding to the function list you entered [fun1,fun2]

        #get Derivative: put functions in a list, 
        # and put the variables of which you want to see the derivatives in a list
        get_gradients([func1,func2], [x,y])
        >>> array([[4., 3.],
                   [1., 4.]])
        #Each row is the derivatives of one function, which is corresponding to the order in "functions" list user entered.
        #In each row, the order of derivatives is corresponding to the variable order in the "variables" list user entered.


    Methods: 
    ==========   
    # ADReverse object-related methods
        __init__(self, value, local_gradients):  Constructs the necessary attributes of an ADReverse object
        __str__(self):  Return the string representation of the ADReverse object.
    
    # Basic operations
        __add__(self, other):  Perform addition on an ADReverse object.
        __radd__(self, other):  Perform reverse addition on an ADReverse object.
        __mul__(self, other):  Perform multiplication on an ADReverse object.
        __rmul__(self, other):  Perform reverse multiplication on an ADReverse object.
        __neg__(self):  Perform negation on ADReverse objects.
        __sub__(self, other):  Perform subtraction on an ADReverse object.
        __rsub__(self, other):  Perform reverse subtraction on an ADReverse object.
        __truediv__(self, other):  Perform true division on an ADReverse object.
        __rtruediv__(self, other):  Perform reverse true division on an ADReverse object.
        __pow__(self, n):  Raise an ADReverse object to the power of n.
        __rpow__(self, other):  Raise a number to the power of an ADReverse object.
        
        Note: the object seems to be able do __inv__ naturally.
        
    # Comparisons
        __gt__(self, other):  Perform "greater than" comparison on an ADReverse object.
        __lt__(self, other):  Perform "less than" comparison on an ADReverse object.
        __ge__(self, other):  Perform "greater or equal than" comparison on an ADReverse object.
        __le__(self, other):  Perform "less or equal than" comparison on an ADReverse object.
  
        Note: the object seems to be able do __eq__ and __ne__ naturally.
      
        
    || Elementary functions || (outside the ADReverse class)
    ===========================
        sin(self):  Compute the sine of an ADReverse object.
        sinh(self):  Compute the hyperbolic sine of an ADReverse object.
        arcsin(self):  Compute the arcsine (inverse of sine) of an ADReverse object.
        cos(self):  Compute the cosine of an ADReverse object.
        cosh(self):  Compute the hyperbolic cosine of an ADReverse object.
        arccos(self):  Compute the arccosine (inverse of cosine) of an ADReverse object.        
        tan(self):  Compute the tangent of an ADReverse object.
        tanh(self):  Compute the hyperbolic tangent of an ADReverse object.       
        arctan(self):  Compute the arctangent (inverse of tangent) of an ADReverse object.
        exp(self):  Compute the exponential of an ADReverse object.
        ln(self):  Compute the natural logarithm of an ADReverse object.
        log(self, base):  Compute the base-specific logarithm of an ADReverse object (default base is 10)
        sqrt(self): Compute the square root of an ADReverse object.
        logistic(self):  Apply the sigmoid function to an ADReverse object, defined as: sigmoid(x) =  1/(1+e**(-x))

    
    || Get Derivatives || (outside the ADReverse class)
    ======================
        get_gradients(functions, variables = []): Calculate the derivatives with respect to each of the variables of every function, return the Jocabian matrix
        
        
    || Get Values || (outside the ADReverse class)
    ==================
        get_values(functions): Calculate the values of each function 
        We could also use the ADReverse's attribute to get the value  eg: func.value
          
    '''
    
    
    
    
    def __init__(self, value, local_gradients=()):
        
        '''
        Constructs the necessary attributes of an ADReverse object representing a variable or a function.
        
        Parameters
        -----------
        value:  (int or float) store this ADReverse obeject's value   
                eg: x = ADReverse(3)
        
        local_gradients: (tuple) store this ADReverse obeject's two children objects and their corresponding local derivatives             
                When we are intiating an ADReverse instance for a variable at the begining, we could use its default value as an empty tuple
                eg: x = ADReverse(3) , x.local_gradients == ()
                        
                After we carry out operations, it would be a tuple of two tuples which store the information of its children objects
                eg: ADReverse(3, ((child1, local_derivative1), (child2, local_derivative2)))
                
        Returns
        -----------
        ADReverse object representing a variable or a function
        
        Examples
        -----------      
        #Scalar input (x) 
        
            x = ADReverse(3) 
            
            func = x*2 + 3
            
            func.value
            >>> 9
            
            func.local_gradients
            >>> ((<__main__.ADReverse at 0x7fd4e65b1dd0>, 1),)
                    
            get_values([func])
            >>> array([[9]])

            get_gradients([func], [x])
            >>> array([[2]])


        #Vector input (x,y)

            x = ADReverse(3) 
            y = ADReverse(2) 
            
            func = x*2 + x*y 
            
            func.value
            >>> 12
            
            func.local_gradients
            >>> ((<__main__.ADReverse at 0x7fd4e65bfb90>, 1),
                 (<__main__.ADReverse at 0x7fd4e65b07d0>, 1))

            get_values([func])
            >>> array([[12]])

            get_gradients([func], [x,y])
            >>> array([[4, 3]])  


        # Vector input (x,y) and Vector output (f1,f2)

            x = ADReverse(3) 
            y = ADReverse(2) 

            func1 = x*2 + x*y 
            func2 = x + y**2
            
            func1.value
            >>> 12
            func2.value
            >>> 7.0
            
            func1.local_gradients
            >>> ((<__main__.ADReverse at 0x7fd4e65b7390>, 1),
                (<__main__.ADReverse at 0x7fd4e65b7210>, 1))
            func2.local_gradients
            >>> ((<__main__.ADReverse at 0x7fd4e651ea10>, 1),
                (<__main__.ADReverse at 0x7fd4e651e050>, 1))

            get_values([func1,fun2])
            >>> array([[12],
                      [ 3]])

            get_gradients([func1,func2], [x,y])
            >>> array([[4., 3.],
                      [1., 4.]])
                        
        '''
        
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('Invalid input type for value.')  
    
        if not isinstance(local_gradients, tuple):
            raise TypeError('Invalid input type for local_gradients.')      
            
        self.value = value       
        self.local_gradients = local_gradients  
        #this object's children and their corresponding local derivative  
        #eg: ((child1, local_derivative1), (child2, local_derivative2))      

        
    def __str__(self):
        
        '''
        Get a string representation of the ADReverse object.
        
        Returns:
        -----------  
        -  value of the variable or funtion that this ADReverse object represents
        -  the local graidents of this ADReverse object
        
        Examples:
        -----------  
        x =  ADReverse(3) 
        print(x)
        >>> Value of this node is:3, its local gradients are:().
        
        func = 3*x+ 2 
        print(func)
        >>> Value of this node is:11, its local gradients are:((<__main__.ADReverse object at 0x7fd4e65b0f50>, 1),).
             
        '''
        return f"Value of this node is:{self.value}, its local gradients are:{self.local_gradients}."
        
    
    def __add__(self, other):
        
        '''
        Perform addition on an ADReverse object 
        
        Parameters:
        -----------
        other: int, float, or ADReverse, other types will raise error.
        
        Returns:
        -----------
        ADReverse object representing the result of self+other
        
        Examples:
        ----------- 
        # add constant
        x = ADReverse(3)
        func =  x +3
        
        func.value
        >>> 6
        get_values(func)
        >>> array([[6]])
        
        get_gradients([func],[x])
        >>> array([[1]])
        
        func.local_gradients == ((x,1),)
        >>> True
        
        # add ADReverse
        x = ADReverse(3)
        y = ADReverse(5)
        z = x + y
        z.value
        >>> 8
        z.local_gradients == ((x,1),(y,1))
        >>> True
        get_gradients([z],[x,y])
        >>> array([[1, 1]])
                   
        '''
        
        if isinstance(other, int) or isinstance(other, float):
            value = self.value + other
            local_gradients = ((self, 1),) # the local derivative with respect to self is 1
        
        elif isinstance(other, ADReverse):
            value = self.value + other.value    
            local_gradients = (
                (self, 1),  # the local derivative with respect to self is 1
                (other, 1))   # the local derivative with respect to other is 1           
        else:
            raise TypeError('Invalid input type.')
            
        return ADReverse(value, local_gradients)
    
    
    def __radd__(self, other):
        
        '''
        Perform reverse addition on an ADReverse object 
        
        Parameters:
        -----------
        other: int, float, other types will raise error.
        
        Returns:
        -----------
        ADReverse object representing the result of other + self
        
        Examples:
        ----------- 
        # add constant
        x = ADReverse(3)
        func =  3 + x
        
        func.value
        >>> 6
        get_values(func)
        >>> array([[6]])
        
        get_gradients([func],[x])
        >>> array([[1]])
        
        func.local_gradients == ((x,1),)
        >>> True
        
        '''
        
        return self.__add__(other)
    
    
    def __mul__(self, other):
        
        '''
        Perform multiplication on an ADReverse object 
        
        Parameters:
        -----------
        other: int, float, or ADReverse, other types will raise error.
        
        Returns:
        -----------
        ADReverse object representing the result of self*other
        
        Examples:
        ----------- 
        # multiply constant
        x = ADReverse(3)
        func =  x * 3
        
        func.value
        >>> 9
        get_values(func)
        >>> array([[9]])
        
        get_gradients([func],[x])
        >>> array([[3]])
        
        func.local_gradients == ((x,3),)
        >>> True
        
        # multiply ADReverse
        x = ADReverse(3)
        y = ADReverse(5)
        func = x * y
        func.value
        >>> 15
        func.local_gradients == ((x,5),(y,3))
        >>> True
        get_gradients([func],[x,y])
        >>> array([[5, 3]])
                   
        '''        
        
        if isinstance(other, int) or isinstance(other, float):
            value = self.value * other
            local_gradients = ((self, other),)
            
        elif isinstance(other, ADReverse):
            value = self.value * other.value
            local_gradients = (
                (self, other.value), # the local derivative with respect to self is other.value
                (other, self.value))  # the local derivative with respect to other is self.value  
        else:
            raise TypeError('Invalid input type.')
            
        return ADReverse(value, local_gradients)
    
    
    def __rmul__(self, other):

        '''
        Perform reverse multiplication on an ADReverse object 
        
        Parameters:
        -----------
        other: int, float, other types will raise error.
        
        Returns:
        -----------
        ADReverse object representing the result of self*other
        
        Examples:
        ----------- 
        # multiply constant
        x = ADReverse(3)
        func =   3 * x
        
        func.value
        >>> 9
        get_values(func)
        >>> array([[9]])
        
        get_gradients([func],[x])
        >>> array([[3]])
        
        func.local_gradients == ((x,3),)
        >>> True
        '''
        
        return self.__mul__(other)
    
    
    def __neg__(self):  
        '''
        Perform negation on ADReverse objects.
                
        Returns:
        -----------
        ADReverse object representing the result of -self
        
        Examples
        -----------
        x = ADReverse(3)
        z = -x 
        
        z.value
        >>> -3
        z.local_gradients == ((x,-1),)
        >>> True
        get_gradients([z],[x])
        >>> array([[-1]])
        '''       
                 
        return self.__mul__(-1)
     
        
    def __sub__(self, other):
             
        '''
        Perform subtraction on ADReverse objects.
        
        Parameters:
        -----------
        other: int, float, or ADReverse, other types will raise error.
                
        Returns:
        -----------
        ADReverse object representing the result of self - other
        
        Examples:
        ----------- 
        # sub constant
        x = ADReverse(3)
        func =  x - 3
        
        func.value
        >>> 0       
        get_gradients([func],[x])
        >>> array([[1]])
        
        func.local_gradients == ((x,1),)
        >>> True
        
        # sub ADReverse
        x = ADReverse(3)
        y = ADReverse(5)
        func = x - y
        func.value
        >>> -2
        func.local_gradients == ((x,1),(y,-1))
        >>> True
        get_gradients([func],[x,y])
        >>> array([[ 1, -1]])
                   
        '''   
    
        if isinstance(other, int) or isinstance(other, float):
            value = self.value - other
            local_gradients = ((self, 1),)
            
        elif isinstance(other, ADReverse):
            value = self.value - other.value
            local_gradients = (
                (self, 1), 
                (other, -1)) 
        else:
            raise TypeError('Invalid input type.')
            
        return ADReverse(value, local_gradients)
    
    
    def __rsub__(self, other):
        
        '''
        Perform reverse subtraction on ADReverse objects.
        
        Parameters:
        -----------
        other: int, float, other types will raise error.
                
        Returns:
        -----------
        ADReverse object representing the result of other - self
        
        Examples:
        ----------- 
        # sub constant
        x = ADReverse(3)
        func =  3 - x
        
        func.value
        >>> 0       
        get_gradients([func],[x])
        >>> array([[-1]])
        
        func.local_gradients == ((x,-1),)
        >>> True

        '''
        
        if ((not isinstance(other, int)) and not (isinstance(other, float))):
            raise TypeError('Invalid input type.')
        value = other -  self.value
        local_gradients = ((self, -1),)
        return ADReverse(value, local_gradients)

    
    
    def __truediv__(self, other):
        
        '''
        Perform true division on ADReverse objects.
        
        Parameters:
        -----------
        other: int, float, or ADReverse, other types will raise error.
                
        Returns:
        -----------
        ADReverse object representing the result of self / other
        
        Examples:
        ----------- 
        # truediv constant
        x = ADReverse(3)
        func =  x / 3
        
        func.value
        >>> 1.0       
        get_gradients([func],[x])
        >>> array([[0.33333333]])
        
        func.local_gradients == ((x,1/3),)
        >>> True
        
        # truediv ADReverse
        x = ADReverse(3)
        y = ADReverse(5)
        func = x / y
        func.value
        >>> 0.6
        func.local_gradients ==((x, 1/5),(y,-3/25))
        >>> True
        get_gradients([func],[x,y])
        >>> array([[ 0.2 , -0.12]])
                
        '''
        
        if isinstance(other, int) or isinstance(other, float):
            if other ==0:
                raise ZeroDivisionError
            else:
                value = self.value / other
                local_gradients = ((self, 1/other),)
                return ADReverse(value, local_gradients) 
            
        elif isinstance(other, ADReverse):
            if other.value == 0:
                raise ZeroDivisionError
            else:
                value = self.value / other.value
                local_gradients = ((self, 1/other.value),(other, - self.value / other.value**2))
                return ADReverse(value, local_gradients)      
        else:
            raise TypeError('Invalid input type.')   
    
    
    def __rtruediv__(self, other):  #other can only be int or float
        
        '''
        Perform reverse true division on ADReverse objects.
        
        Parameters:
        -----------
        other: int, float, other types will raise error.
                
        Returns:
        -----------
        ADReverse object representing the result of  other/self
        
        Examples:
        ----------- 
        # rtruediv constant
        x = ADReverse(3)
        func =   3 /x
        
        func.value
        >>> 1.0       
        get_gradients([func],[x])
        >>> array([[-0.33333333]])
        
        func.local_gradients ==((x, -1/3),)
        >>> True
                
        '''
        
        
        if (not isinstance(other, int)) and (not isinstance(other, float)): 
            raise TypeError('Invalid input type.')
            
        else:
            if self.value == 0:
                raise ZeroDivisionError
            else:
                value = other / self.value
                local_gradients = ((self, -other / self.value**2 ),)
                return ADReverse(value, local_gradients) 
                 
                    
    def  __pow__(self, n):
        
        '''
        Raise an ADRevese object to the power of n.
        
        Parameters:
        -----------
        other: int, float, or ADReverse, other types will raise error.
                
        Returns:
        -----------
        ADReverse object representing the result of self ** other
        
        Examples:
        ----------- 
        # pow constant
        x = ADReverse(3)
        func =  x ** 2
        
        func.value
        >>> 9.0       
        get_gradients([func],[x])
        >>> array([[6.]])
        
        func.local_gradients == ((x, 6),)
        >>> True
        
        # pow ADReverse
        x = ADReverse(3)
        y = ADReverse(3)
        func = x ** y
        func.value
        >>> 27

        get_gradients([func],[x,y])
        >>> array([[27.        , 29.66253179]])
                
        '''        
        
        if isinstance(n, int) or isinstance(n, float):
            n = float(n)
            val = self.value
            if val < 0 and (0 < n < 1 or -1 < n < 0):
                raise ValueError('Square Root can not be negative.')
            if val == 0 and n < 0:
                raise ZeroDivisionError
            if val ==0  and n ==0: 
                raise ValueError('Function has no meaning')
           
            value = val** n
            local_gradients = ((self,  n *  (val ** (n - 1)) ),)
            return ADReverse(value, local_gradients) 
            
        elif isinstance(n, ADReverse):  # n is an ADReverse object 
            val_base = self.value
            val_exponent = n.value             
            if val_base <= 0:
                raise ValueError('The base of exponential function need to be greater than 0')
                
            value = val_base ** val_exponent
            local_gradients = ((self,  val_exponent *  (val_base ** (val_exponent - 1)) ), 
                               (n, val_base ** val_exponent * np.log(val_base)) )

            return ADReverse(value, local_gradients) 
        
        else: 
            raise TypeError('Invalid Input Type for the exponent')
            
        
    def __rpow__(self, other):
        
        '''
        Raise a number to the power of an ADReverse object.
        
        Parameters:
        -----------
        other: int, float, other types will raise error.
                
        Returns:
        -----------
        ADReverse object representing the result of other ** self
        
        Examples:
        ----------- 
        # pow constant
        x = ADReverse(3)
        func =  2 ** x
        
        func.value
        >>> 8      
        get_gradients([func],[x])
        >>> array([[5.54517744]])
        
        '''  
        
        
        if isinstance(other, int) or isinstance(other, float):
            if other <= 0:
                raise ValueError('The base of exponential function need to be greater than 0')
            value = other ** self.value
            local_gradients = ((self, other ** self.value * np.log(other)),)
            return ADReverse(value, local_gradients) 
            
        else:
            raise TypeError('Invalid input type')
       

    def __gt__(self, other):

        '''
        Perform "greater than" comparison on value of an ADReverse object.
        Parameters:
        -----------
        other : int, float, or ADReverse, other types will raise error.
                Value to compare with self, which is an ADReverse object.
                
        Returns:
        -----------
        Boolean representing the result of self > other
        
        Examples: 
        -----------
        x = ADReverse(3)
        y = ADReverse(5)
        x > 4
        >>> False
        x > y
        >>> False
                
        '''        
        
        if isinstance(other, int) or isinstance(other, float):
            compare = other
        elif isinstance(other, ADReverse):  
            compare = other.value
        else:
            raise TypeError('Invalid input type')
        if self.value > compare:
            return True
        else:
            return False 
            
            
    def __lt__(self, other):
        
        '''
        Perform "less than" comparison on value of an ADReverse object.
        Parameters:
        -----------
        other : int, float, or ADReverse, other types will raise error.
                Value to compare with self, which is an ADReverse object.
                
        Returns:
        -----------
        Boolean representing the result of self < other
        
        Examples: 
        -----------
        x = ADReverse(3)
        y = ADReverse(5)
        x < 4
        >>> True
        x < y
        >>> True
                
        '''   
        
        if isinstance(other, int) or isinstance(other, float):
            compare = other
        elif isinstance(other, ADReverse):  
            compare = other.value
        else:
            raise TypeError('Invalid input type')
        if self.value < compare:
            return True
        else:
            return False
 

    def __ge__(self, other):
        

        '''
        Perform "greater than or equal to" comparison on value of an ADReverse object.
        Parameters:
        -----------
        other : int, float, or ADReverse, other types will raise error.
                Value to compare with self, which is an ADReverse object.
                
        Returns:
        -----------
        Boolean representing the result of self >= other
        
        Examples: 
        -----------
        x = ADReverse(3)
        y = ADReverse(5)
        x >= 4
        >>> False
        x >= y
        >>> False
                
        ''' 
        
        if isinstance(other, int) or isinstance(other, float):
            compare = other
        elif isinstance(other, ADReverse):  
            compare = other.value
        else:
            raise TypeError('Invalid input type')
        if self.value >= compare:
            return True
        else:
            return False 
            
            
    def __le__(self, other):
        
        '''
        Perform "less than or equal to" comparison on value of an ADReverse object.
        Parameters:
        -----------
        other : int, float, or ADReverse, other types will raise error.
                Value to compare with self, which is an ADReverse object.
                
        Returns:
        -----------
        Boolean representing the result of self <= other
        
        Examples: 
        -----------
        x = ADReverse(3)
        y = ADReverse(5)
        x <= 4
        >>> True
        x <= y
        >>> True
                
        '''  
    
        if isinstance(other, int) or isinstance(other, float):
            compare = other
        elif isinstance(other, ADReverse):  
            compare = other.value
        else:
            raise TypeError('Invalid input type')
        if self.value <= compare:
            return True
        else:
            return False        
  
    
'''
Elementary Functions
'''
    
def sin(self):
    
    '''
    Compute the sine of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of sin(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = sin(x)
    
    z.value
    >>> 0.479425538604203
    get_gradients([z],[x])
    >>> array([[0.87758256]])
   
    '''
        
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')       
    value = np.sin(self.value)
    local_gradients = ((self, np.cos(self.value)),)
    return ADReverse(value, local_gradients)


def sinh(self):
    
    '''
    Compute the hyperbolic sine of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of sinh(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = sinh(x)
    
    z.value
    >>> 0.5210953054937474
    get_gradients([z],[x])
    >>> array([[1.12762597]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')  
    value = np.sinh(self.value)
    local_gradients = ((self, np.cosh(self.value)), )
    return ADReverse(value, local_gradients)


def arcsin(self):
    
    '''
    Compute the arcsine (inverse of sine) of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of arcsin(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = sinh(x)
    
    z.value
    >>> 0.5235987755982988
    get_gradients([z],[x])
    >>> array([[1.15470054]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')  
    if (self.value < -1) or (self.value > 1):
        raise ValueError("Cannot take derivative of arcsin of value outside of range [-1, 1]")
    if self.value == -1 or self.value == 1:
        raise ZeroDivisionError
    value = np.arcsin(self.value)
    local_gradients = ((self, (1 - self.value ** 2) ** (-0.5) ), )
    return ADReverse(value, local_gradients)


def cos(self):
    
    '''
    Compute the cosine of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of cos(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = cos(x)
    
    z.value
    >>> 0.8775825618903728
    get_gradients([z],[x])
    >>> array([[-0.47942554]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')  
    value = np.cos(self.value)
    local_gradients = ((self, -np.sin(self.value)),)
    return ADReverse(value, local_gradients)


def cosh(self):
        
    '''
    Compute the hyperbolic cosine of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of cosh(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = cosh(x)
    
    z.value
    >>> 1.1276259652063807
    get_gradients([z],[x])
    >>> array([[0.52109531]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')  
    value = np.cosh(self.value)
    local_gradients = ((self, np.sinh(self.value)), ) 
    return ADReverse(value, local_gradients)


def arccos(self):
    
    '''
    Compute the arccosine (inverse of cosine) of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of arccos(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = arccos(x)
    
    z.value
    >>> 1.0471975511965976
    get_gradients([z],[x])
    >>> array([[-1.15470054]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')  
    if self.value < -1 or self.value > 1:
        raise ValueError("Cannot take derivative of arcsin of value outside of range [-1, 1]")
    if self.value == -1 or self.value == 1:
        raise ZeroDivisionError
    value = np.arccos(self.value)
    local_gradients = ((self,  -1 * ((1 - self.value ** 2) ** (-0.5))  ),)
    return ADReverse(value, local_gradients)


def tan(self):
    
    '''
    Compute the tangent of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of tan(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = tan(x)
    
    z.value
    >>> 0.5463024898437905
    get_gradients([z],[x])
    >>> array([[1.29844641]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    if( ((self.value / np.pi) - 0.5) % 1 == 0.00 ):
        raise ValueError("Math error, Tangent cannot handle i*0.5pi ")
    value = np.tan(self.value)
    local_gradients = ((self,  1. / np.power(np.cos(self.value), 2) ), )
    return ADReverse(value, local_gradients)


def tanh(self):
    
    '''
    Compute the hyperbolic tangent of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of tanh(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = tanh(x)
    
    z.value
    >>> 0.46211715726000974
    get_gradients([z],[x])
    >>> array([[0.78644773]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    value = np.tanh(self.value)
    local_gradients = ((self, 1 - (np.tanh(self.value))**2 ), )    
    return ADReverse(value, local_gradients)


def arctan(self):

    '''
    Compute the arctangent (inverse of tangent) of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of arctan(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = arctan(x)
    
    z.value
    >>> 0.46364760900080615
    get_gradients([z],[x])
    >>> array([[0.8]])
   
    '''
        
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    value = np.arctan(self.value)
    local_gradients = ((self,  (1 + self.value ** 2) ** (-1) ), )
    return ADReverse(value, local_gradients)


def exp(self):

    '''
    Compute the exponential of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of exp(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = exp(x)
    
    z.value
    >>> 1.6487212707001282
    get_gradients([z],[x])
    >>> array([[1.64872127]])
   
    '''
    
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    value = np.exp(self.value)
    local_gradients = ((self, np.exp(self.value)),)
    return ADReverse(value, local_gradients)


def ln(self):
    
    '''
    Compute the natural logarithm of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of ln(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = ln(x)
    
    z.value
    >>> -0.6931471805599453
    get_gradients([z],[x])
    >>> array([[2.]])
   
    '''
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    if self.value <= 0:
        raise ValueError("Cannot take natural log of zero or negative values")
    value = np.log(self.value)
    local_gradients = ((self, 1. / self.value),)
    return ADReverse(value, local_gradients)


def log(self, base=10):
    
    '''
    Compute the base-specific logarithm of an ADReverse object,  default is 10.
    
    Returns
    -----------
    ADReverse object representing the result of log(self, base)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = log(x,2)
    
    z.value
    >>> -1.0
    get_gradients([z],[x])
    >>> array([[2.88539008]])
   
    '''    

    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    if self.value <= 0:
        raise ValueError("Cannot take log of zero or negative values")
    value = math.log(self.value,base)
    local_gradients = ((self, 1. / (self.value*np.log(base)) ), )  
    return ADReverse(value, local_gradients)


def sqrt(self):
    
    '''
    Compute the square root of an ADReverse object.
    
    Returns
    -----------
    ADReverse object representing the result of sqrt(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = sqrt(x,2)
    
    z.value
    >>> 0.7071067811865476
    get_gradients([z],[x])
    >>> array([[0.70710678]])
   
    '''    
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    return self.__pow__(0.5)


def logistic(self):
    
    '''
    Compute the sigmoid function of an ADReverse object.
    
    The sigmoid function of x is defined as:
    sigmoid(x) =  1/(1+e**(-x))
    
    Returns
    -----------
    ADReverse object representing the result of sigmoid(self)
    
    Examples
    -----------
    x = ADReverse(0.5)
    z = logistic(x)
    
    z.value
    >>> 0.6224593312018546
    get_gradients([z],[x])
    >>> array([[0.23500371]])
   
    '''   
    
    if not isinstance(self, ADReverse):
        raise TypeError('Invalid input type')
    value = 1. / (1 + np.exp(-self.value))
    local_gradients = ((self, np.exp(-self.value) / ((1 + np.exp(-self.value)) ** 2) ), )
    return ADReverse(value, local_gradients)




#compute gradients and get the Jocabian matrix

def get_gradients(functions, variables = []):
    
    '''
    Calculate Jacobian Matrix of multiple functions with mulvariables.
    
    In the Jocabian calculation, we go through the graph from parent to children recursively, 
    multiply the local derivatives alonge each path. If two paths have the same variable, we add together the different paths,
    and store each possible ADReverse object's derivative in a dictionary, like { ADReverse1 : deriv1 ,ADReverse2 : deriv2 }
    Then from the dictionary we find the derivatives of target variables in the list of "variables" and construct the Jocabian matrix.
           
    Parameters
    ----------- 
    functions:  ADReverse obeject or a list of ADReverse obejects, each one represents one function
    
    variables:  A list of ADReverse objects, each one represents a variable whose derivative the user want to obtain.
    
    Returns
    -----------
    a numpy.ndarray which shows the Jocabian matrix.
    Each row is the derivatives of one function, which is corresponding to the order in "functions" list user entered.
    In each row, the order of derivatives is corresponding to the variable order in the "variables" list user entered.
    
    Note: if one of the ADReverse object in the variable list is not found in one function, its derivative will be shown as 0.
        
    Examples
    -----------  
    x = ADReverse(2)
    y = ADReverse(3)
    z = ADReverse(-1)
    fun1 = x*y +z 
    get_gradients(fun1,[x,y,z])   / get_gradients([fun1],[x,y,z])  
    >>> array([[3, 2, 1]])
    
    fun2  = x*y + x**y
    get_gradients([fun1,fun2],[x,y,z])
    >>> array([[ 3. ,  2. ,  1.  ],
            [15.,  7.54517744,  0.]])
            
    '''
    
    if isinstance (functions, ADReverse):
        functions = [functions]
    if not isinstance (functions, list):
        raise TypeError("The functions need to be a list")
    for i in functions:
        if not isinstance(i, ADReverse ):
            raise TypeError("All the elements in function list should be an ADReverse object.")

    if not isinstance (variables, list):
        raise TypeError("The variables need to be a list")
            
    for i in variables:
        if not isinstance(i, ADReverse ):
            raise TypeError("All the elements in variable list should be an ADReverse object.")
       
    Jocabian = [] 
    for func in functions:
        gradients = {}

        def compute_gradients(ad_reverse, path_value):
            for child_variable, local_gradient in ad_reverse.local_gradients:
                # "Multiply the edges of a path":
                value_of_path_to_child = path_value * local_gradient
                # "Add together the different paths":
                if gradients.get(child_variable, None ) == None:
                    gradients[child_variable] = value_of_path_to_child
                else:
                    gradients[child_variable] += value_of_path_to_child
                # recurse through graph:
                compute_gradients(child_variable, value_of_path_to_child)

        compute_gradients(func, path_value=1)
        # (path_value=1 is from `variable` differentiated w.r.t. itself)
        
        grad = []
        for var in variables:
            grad.append(gradients.get(var, 0))  
            
        Jocabian.append(grad)
        
    return np.array(Jocabian)
               

def get_values(functions):
    
    '''
    Calculate the values of vector functions
    
    Parameters
    ----------- 
    functions:  ADReverse obeject or a list of ADReverse obejects, each one represents one function
    
    Returns
    ----------- 
    a numpy.ndarray which shows the values of multiple functions
    Each row is the value of one function, which is corresponding to the order in "functions" list user entered. 
    
    Note: if there is only one fucntion, user could also print "func.value" instead of using this "get_values" function     

    Examples
    -----------  
    x = ADReverse(2)
    y = ADReverse(3)
    z = ADReverse(-1)
    fun1 = x*y +z 
    get_values(fun1)  / get_values([fun1])
    >>> array([[5]])
    
    fun2  = x*y + x**y
    get_values([fun1,fun2])
    >>> array([[ 5],
               [14]])
                
    '''
    
    if isinstance (functions, ADReverse):
        functions = [functions]
    if not isinstance (functions, list):
        raise TypeError("The functions need to be a list")
    for i in functions:
        if not isinstance(i, ADReverse ):
            raise TypeError("All the elements in functions list should be an ADReverse object.")
        
    value_output = []
    for func in functions:
        value_output.append([func.value])
    return np.array(value_output)


#demo
# x = ADReverse(2)
# y = ADReverse(3)
# z = ADReverse(-1)
# fun3 = 1+ 3*x + y +  z **2
# fun4 = x*y  + x/z
# print(get_gradients([fun3,fun4], [x,y,z]))
# print(get_values([fun3,fun4]))