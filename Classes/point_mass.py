import numpy as np
class PointMass:
    """
    Class to model a point mass in the simulation.

    p: Position (vector)
    v: Velocity (vector)
    a: Acceleration (vector)
    m: Mass (scalar)
    g: Gravity (scalar)
    l: Lock (boolean)
    """
    def __init__(self, p, v, a, m, g, l, c):
        self.p = p
        self.v = v
        self.a = a
        self.m = m
        self.g = g
        self.a[1] = g
        self.l = l
        self.c = c

    def eraseA(self):
        self.a = np.array([0,self.g])

    def applyF(self, F):
        self.a[0] += F[0]/self.m
        self.a[1] += F[1]/self.m

    def reflectV(self, v):
        if np.linalg.norm(v) != 0:
            v = v / np.linalg.norm(v) * 0.995
        self.v = self.v - 2 * (np.dot(self.v,v)) * v

    def step(self, dt):
        if not self.l:
            self.p[0] += self.v[0]*dt
            self.p[1] += self.v[1]*dt
            self.v[0] += self.a[0]*dt
            self.v[1] += self.a[1]*dt
            if self.p[1] <= 0:
                self.p[1] = 0
                self.reflectV(np.array([0, 1]))

# k = 1
# d = 1
# L = 2
# A = PointMass(np.array([0.0, 0.0]), np.array([0.0, -0.1]), np.array([0.0, 0.0]), 1, -6)
# B = PointMass(np.array([0.0, 1.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, -6)
# v = A.p - B.p
# x = np.linalg.norm(v)
# y = x
# if not x == 0:
#     m = v * k * (L - x) / x
#     y = (np.dot(B.v - A.v, v / x) * d) * v / x
#     #x = m + y
#     #y = y - m
# print(m, y)
    
        