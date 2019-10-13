import math


class Vector(object):
    """this is a general vector class"""

    def __init__(self, *args):   # (*) references a variable length as long as you like and is optional
        """
        processes arguments and assigns to Vector2 or Vector3 accordingly
        :param args: x, y, z or dimensions of a vector
        """
        self.data = []
        for a in args:
            self.data.append(float(a))

        self.dim = len(args)  # or len(self.data) / gives the initial length

        if self.dim == 2:
            self.__class__ = Vector2

        if self.dim == 3:
            self.__class__ = Vector3

    def __getitem__(self, index):  # __metehod name__ is a method not used directly
        """allows you to directly index the vector object"""
        return self.data[index]

    def __len__(self):
        """returns the length"""
        return self.dim

    def __setitem__(self, index, new_val):
        """like get item except you can set an item as well
        :param index: an integer
        :new val: value that can be converted to a float 
        : return none"""
        self.data[index] = float(new_val)

    def __str__(self):
        """returns a string representation of our vector(self)"""
        s = "<Vector" + str(self.dim) + ": "

        for i in range(self.dim):      # this for loop adds onto the string s 
            s += str(self.data[i])
            if i < self.dim-1:
                s += ","
        s += ">"
        return s

    def copy(self):
        """ creates a deep copy of this vector
        return: returns a new vector copy"""
        v = Vector(*self.data)
        v.__class__ = self.__class__
        return v

    def __eq__(self, other):
        """
        :param other: any value
        :return: a boolean True if other is a vector with same dimension and exactly the same entries
        """
        if isinstance(other,Vector) and len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        return False 

    def __mul__(self, scalar):
        """
        multiply a vector by a scalar
        the scalar is on the right of *
        :param scalar: the value to multiply by (int, or float)
        :return: a copy of this vector with all values multiplied by scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "vector" + str(self.dim)
            raise TypeError("You can only multiply this" + n + "and a scalar. You attempted to multiply by " + str(scalar) + ".")

        r = self.copy()
        for i in range(self.dim):
            r[i] *= scalar
        return r

    def __rmul__(self, scalar):
        """
        can multiply with the scalar on the left side
        :param scalar: same as mul
        :return: same as mul
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "vector" + str(self.dim)
            raise TypeError("You can only multiply this" + n + "and a scalar. You attempted to multiply by " + str(scalar) + ".")

        r = self.copy()
        for i in range(self.dim):
            r[i] *= scalar
        return r

    def __add__(self, other_vec):
        """
        can add two vectors together
        :param other_vec: is a vector with the same dim as self
        :return: a new vector of self and other_vec added together
        """
        if not isinstance(other_vec, self.__class__) or self.dim != other_vec.dim:
            n = " vector" + str(self.dim)
            raise TypeError("You can only add this " + n + " and another vector. you attempted to add by " + str(other_vec) + ".")

        r = self.copy()
        for i in range(self.dim):
            r[i] += other_vec[i]
        return r

    def __sub__(self, other):
        """
        :param other:
        :return:
        """
        if self.dim != other.dim:
            n = "vector" + str(self.dim)
            raise TypeError("You can only subtract this" + n + "and another vector. you attempted to subtract by " + str(other) + ".")
        r = self.copy()
        for i in range(self.dim):
            r[i] -= other[i]
        return r

    def __neg__(self):
        """
        allows you to print(-v)
        :return: returns a vector with each element multiplied by negative 1
        """
        r = self.copy()
        for i in range(self.dim):
            r[i] *= -1
        return r

    def __truediv__(self, scalar):
        """
        :param other: vector with same dim as self
        :return:
        """
        n = "vector" + str(self.dim)
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            raise TypeError ('You can only divide this ' + n + ' by an int and float. You tried to divide by ' + scalar + '.')

        r = self.copy()
        for i in range(self.dim):
            r[i] /= scalar
        return r

    @property
    def mag(self):
        """
        :return: returns the Euclidean norm of vector
        """
        l = 0
        for i in range(self.dim):
            l = l + (abs(self[i])**2)
        return l ** (1/2)

    @property
    def mag_squared(self):
        """
        finds the length squared
        :return:
        """
        l = 0
        for i in range(self.dim):
            l = l + (abs(self[i])**2)
        return l

    @property
    def normalize(self):
        """
        :return: returns a unit vector in the same direction as self
        """
        return self * (1/self.mag)

    @property
    def is_zero(self):
        """
        :return: Flase if vector is not equal to zero vector and true if it is
        """
        for i in range(self.dim):
            if self[i] != 0:
                return False
        return True

    @property
    def i(self):
        """
        :return: reurns a touple of the coordinates of vector self converted to integers
        """
        l = []
        for i in range(self.dim):
            l.append(int(self[i]))
        t = tuple(l)
        return t

#################################################################################################################


class Vector2(Vector):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def x(self):
        """
        allows you to call x like an attribute
        :return: returns the x value when you call the function
        """
        return self[0]

    @x.setter
    def x(self, newval):
        """
        allows you to call x like an attribute and set it to a new value
        :return: resets the x value to the new value
        """
        if not isinstance(newval, int) and not isinstance(newval, float):
            raise TypeError("You can only input an int or float for argument (newval). You input " + str(newval) + ".")
        self[0] = float(newval)

    @property
    def y(self):
        """
        allows you to call y like an attribute
        :return: returns the y value when you call the function
        """
        return self[1]

    @y.setter
    def y(self, newval):
        """
        allows you to call y like an attribute and set it to a new value
        :return: resets the y value to the new value
        """
        if not isinstance(newval, int) and not isinstance(newval, float):
            raise TypeError("You can only input an int or float for argument (newval). You input " + str(newval) + ".")
        self[1] = float(newval)

    @property
    def degrees(self):
        """
        converts square coordinates to polar coordinates and returns an angle theta in degrees
        :param x: the x coordinate of the vector
        :param y: the y value of the vector
        :return: returns the angle theta
        """
        t = math.atan2(self.y, self.x)
        return math.degrees(t)

    @property
    def degrees_inv(self):
        """
        flips the y axis to negate pygames y axis
        :return: negates the y value
        """
        t = math.atan2(-self.y, self.x)
        return math.degrees(t)

    @property
    def radians(self):
        """
        :return: returns the radian measure of this vector in polar space
        """
        t = math.atan2(self.y, self.x)
        return t

    @property
    def radians_inv(self):
        """
        flips the y value to negate pygames y axis
        :return: negates the y value
        """
        t = math.atan2(-self.y, self.x)
        return t

    @property
    def perpendicular(self):
        """
        :return: returns a vector 2 perpendicular to this one
        """
        perp = [-self.y, self.x]
        return perp

#################################################################################################


class Vector3(Vector):
    def __init__(self, x, y, z):
        super(). __init__(x, y, z)

    @property
    def x(self):
        """
        allows you to call x like an attribute
        :return: returns the x value when you call the function
        """
        return self[0]

    @x.setter
    def x(self, newval):
        """
        allows you to call x like an attribute and set it to a new value
        :return: resets the x value to the new value
        """
        if not isinstance(newval, int) and not isinstance(newval, float):
            raise TypeError("You can only input an int or float for argument (newval). You input " + str(newval) + ".")
        self[0] = newval

    @property
    def y(self):
        """
        allows you to call y like an attribute
        :return: returns the y value when you call the function
        """
        return self[1]

    @y.setter
    def y(self, newval):
        """
        allows you to call y like an attribute and set it to a new value
        :return: resets the y value to the new value
        """
        if not isinstance(newval, int) and not isinstance(newval, float):
            raise TypeError("You can only input an int or float for argument (newval). You input " + str(newval) + ".")
        self[1] = newval

    @property
    def z(self):
        """
        allows you to call z like an attribute
        :return: returns the z value when you call the function
        """
        return self[2]

    @z.setter
    def z(self, newval):
        """
        allows you to call z like an attribute and set it to a new value
        :return: resets the z value to the new value
        """
        if not isinstance(newval, int) and not isinstance(newval, float):
            raise TypeError("You can only input an int or float for argument (newval). You input " + str(newval) + ".")
        self[2] = newval

#############################################################################


def dot(v, w):
    """
    function does the dot product between 2 vectors (v) and (w) of the same dimension
    :param v: vector object
    :param w: vector object same dimension as v
    :return: returns a scalar
    """
    if v.dim != w.dim:
        x = str(v.dim)
        f = str(w.dim)
        raise TypeError('You can only find the dot product between 2 vectors of the same dimension. You input the dimensions ' + x +
                        ' and ' + f + '.')
    dot = 0
    for i in range(v.dim):
        dot = dot + v[i] * w[i]
    return dot


def cross(v, w):
    """
    accepts 2 vector3's (v) and (w) and returns a vector3
    :param v: 3 dimensional Vector
    :param w: 3 dimensional Vector
    :return: returns a vector3
    """
    if not isinstance(v, Vector3) or not isinstance(w, Vector3):
        x = str(v.dim)
        f = str(w.dim)
        raise TypeError('You can only find the cross product between 2 vector3. You input the dimensions ' + x +
                        ' and ' + f + '.')

    x = []
    x.append(v.y*w.z - w.y*v.z)
    x.append(-(v.x*w.z - w.x*v.z))
    x.append(v.x*w.y - w.x*v.y)
    return x


def polar_to_Vector2(r, theta, flip):
    """
    accepts coordinates in polar coordinates and converts to cartesian coordinate
    :param r: looking for the distance to the point
    :param theta: the angle (radians) that (r) is at from 0
    :return: returns cartesian coordinates or square coordinates
    """
    r,t,f = r,theta,flip
    if not isinstance(r, int) and not isinstance(r, float):
        raise TypeError("You can only input an int or float for the argument (r). You input " + str(r) + ".")
    if not isinstance(theta, int) and not isinstance(theta, float):
        raise TypeError("You can only input an int or float for the argument (theta). You input " + str(t) + ".")
    x = r * math.cos(theta)
    y = r * math.sin(theta)

    if flip is True:
        return [x, -y]
    return [x, y]


def pnorm(v, p=2):
    """
    input a vector and a positive integer for (p). if p is not given it is set to 2 as default
    :param v: Vector
    :return: returns the P-norm
    """
    if not isinstance(p, int):
        if not isinstance(p, float):
            raise TypeError("You can only input a float or integer, for argument (p). You put in " + str(p) + ".")
    ans = 0
    for i in range(v.dim):
        ans = ans + (abs(v[i]) ** p)
    return ans ** (1/p)

# v = Vector(1, 2, 3)
# w = Vector(-4, 5)
# z = v + w


"""
print(z) # <Vector3: 5.0, 7.0, 9.0>
#print("v + 5 =", v + 5) # TypeError: You can only add another
# Vector3 to this Vector3 (You passed
# '5'.)
q = v - w
print(q) # <Vector3: -3.0, -3.0, -3.0>
a = v * -2
print(a) # <Vector3: -2.0, -4.0, -6.0>
a = -2 * v
print(a) # <Vector3: -2.0, -4.0, -6.0>
b = a + (v + w)
print(b) # <Vector3: 3.0, 3.0, 3.0>
d = v + (v + v) + w
print(d) # <Vector3: 7.0, 11.0, 15.0>
n = -v
print(n) # <Vector3: -1.0, -2.0, -3.0>
s = Vector2(3, -2)
print(s) # <Vector2: 3.0, -2.0)
print(s.x) # 3.0
t = Vector(3, -2)
print(t) # <Vector2: 3.0, -2.0>
print(t.y) # -2.0
print(s == t) # True"""


# v = Vector(13.7, 1.414)
# print(v.perpendicular)
# print(v.degrees)
# print(v.degrees_inv)
# print(v.normalize)
# w = v.normalize
# print(w.mag)
# print(v.i)
# print(dot(v,w))
# print(cross(v,w))
# print(pnorm(v,'j'))
# print(v.mag)
# print(polar_to_Vector2(1, math.pi/4, True))
# print(math.degrees(math.pi/4))
# print(v.z)
# v.z = "jack"
# print(pnorm(w))
# print(abs(-7))
