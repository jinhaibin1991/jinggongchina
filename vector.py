import math

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
    def __str__(self):
        return 'Vector (%f, %f)' % (self.x, self.y)
    
    
   
    def __add__(self,other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self,other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def unit(self):
        if self.x**2+self.y**2 == 0:
            return Vector(0,0)
        else:
            
            return Vector(self.x/math.sqrt(self.x**2+self.y**2),self.y/math.sqrt(self.x**2+self.y**2))
    
    def __neg__(self):
        return Vector(-self.x,-self.y)
    
    def __mul__(self,other):
                    
        return Vector(self.x*other.x,self.y*other.y)
    
    def vector_mul_value(self,other):
        return Vector(self.x*other,self.y*other)
        
        
    
    

