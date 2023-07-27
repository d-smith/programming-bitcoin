from unittest import TestCase

class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:  # <1>
            error = 'Num {} not in field range 0 to {}'.format(
                num, prime - 1)
            raise ValueError(error)
        self.num = num  # <2>
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime 
    
    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different fields')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self,other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different fields')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)
    
    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different fields')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)
    
    def __pow__(self,exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)
    
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        # use Fermat's little theorem:
        # self.num**(p-1) % p == 1
        # this means:
        # 1/n == pow(n, p-2, p)
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)
    
    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)

    
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
        return not (self == other)
    
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
        
    def __rmul__(self, coefficient):
        coef = coefficient
        current = self  # <1>
        result = self.__class__(None, None, self.a, self.b)  # <2>
        while coef:
            if coef & 1:  # <3>
                result += current
            current += current  # <4>
            coef >>= 1  # <5>
        return result
        
class ECCTest(TestCase):

    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)  # <1>
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)  # <1>
    # end::source2[]

    def test_add(self):
        # tests the following additions on curve y^2=x^3-7 over F_223:
        # (192,105) + (17,56)
        # (47,71) + (117,141)
        # (143,98) + (76,66)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        additions = (
            # (x1, y1, x2, y2, x3, y3)
            (192, 105, 17, 56, 170, 142),
            (47, 71, 117, 141, 60, 139),
            (143, 98, 76, 66, 47, 71),
        )

        # loop over additions
        # initialize x's and y's as FieldElements
        # create p1, p2 and p3 as Points
        # check p1+p2==p3
        raise NotImplementedError

    def test_rmul(self):
        # tests the following scalar multiplications
        # 2*(192,105)
        # 2*(143,98)
        # 2*(47,71)
        # 4*(47,71)
        # 8*(47,71)
        # 21*(47,71)
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            # (coefficient, x1, y1, x2, y2)
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        # iterate over the multiplications
        for s, x1_raw, y1_raw, x2_raw, y2_raw in multiplications:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            # initialize the second point based on whether it's the point at infinity
            if x2_raw is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(x2_raw, prime)
                y2 = FieldElement(y2_raw, prime)
                p2 = Point(x2, y2, a, b)

            # check that the product is equal to the expected point
            self.assertEqual(s * p1, p2)