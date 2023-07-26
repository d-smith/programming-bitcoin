class Point:
    
    def __init__(self, x,y,a,b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        
        # For the point at infinity we can skip the on the curve check. We use None to denote infinity
        if self.x is None and self.y is None:
            return
        
        if self.y**2 != self.x**3 + a*x + b:
            raise ValueError('({},{}) is not on the curve'.format(x,y))
            
    def __str__(self):
        return 'Point({},{},{},{})'.format(self.x, self.y, self.a, self.b)
            
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b
    
    def __ne__(self, other):
        return not __eq__(self, other)
    
    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise ValueError('Points {},{} are not on the same curve'.format(self,other))
            
        # Identity
        if self.x is None:
            return other
        if other.x is None:
            return self
        
        # Invertabilitu
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        
        # x not equal to y
        if self.x != other.x:
            s = (other.y - self.y)/(other.x - self.x)
            x = s**2 -self.x - other.x
            y = s*(self.x - x) - self.y

            return self.__class__(x,y,self.a, self.b)
        
        # tangent is vertical
        if self == other and self.y == 0*self.x:
            return self.__class__(None,None,a,b)

        # p1 = p2 => find the intersection of the tangent to the point
        if self == other:
            s = (3*self.x**2 + self.a)/(2*self.y)
            x = s**2 - 2*self.x
            y = s*(self.x - x) - self.y

            return self.__class__(x,y,self.a, self.b)
        