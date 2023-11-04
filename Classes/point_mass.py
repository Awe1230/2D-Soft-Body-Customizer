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
        self.a = np.array([0.0,self.g])

    def applyF(self, F):
        self.a[0] += F[0]/self.m
        self.a[1] += F[1]/self.m
    
    def updateP(self, p):
        self.p = p

    def reflectV(self, v):
        # p = np.array([v[1], -v[0]])
        # if np.dot(self.v, -p) < 0:
        #     p = -p
        # p = p / np.linalg.norm(p)
        v = v * 0.995
        t = np.linalg.norm(v)
        if t != 0:
            v = v / t
        d = np.dot(self.v, v)
        y = self.v - 2 * d * v
        #self.applyF(p * d * -2 * 100 * self.m)
        self.v = y
    def round(self, m):
        y = 5
        for i in range(len(m)-1):
            m[i] = int(m[i] * 10 ** y) / 10 ** y
    def step(self, dt):
        if not self.l:
            self.round(self.a)
            self.p[0] += self.v[0]*dt
            self.p[1] += self.v[1]*dt
            self.v[0] += self.a[0]*dt
            self.v[1] += self.a[1]*dt
            if self.p[1] <= 0:
                self.p[1] = 0
                self.reflectV(np.array([0.0, 1.0]))
            elif self.p[1] >= 700:
                self.p[1] = 700
                self.reflectV(np.array([1.0, 0.0]))
            if self.p[0] <= 0:
                self.p[0] = 0
                self.reflectV(np.array([1.0, 0.0]))
            elif self.p[0] >= 1200:
                self.p[0] = 1200
                self.reflectV(np.array([1.0, 0.0]))

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
    
        