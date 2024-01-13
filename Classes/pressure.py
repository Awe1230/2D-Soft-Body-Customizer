import numpy as np
from Classes.point_mass import PointMass

class Pressure:
    def __init__(self, pts, b):
        self.pts = pts
        self.v = self.volume()
        self.b = 2*b*10**10
        self.constantp = self.b/self.v
    def volume(self):
        self.center = np.mean(np.array([pt.p for pt in self.pts]), axis = 0)
        totalr = 0.0
        for x in self.pts:
            totalr += np.linalg.norm(x.p-self.center)
        r = totalr/len(self.pts)
        return 3.1415926535859*r**2
    def inflate(self):
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0
        currentv = self.volume()
        for n in range(len(self.pts)):
            next = n + 1
            if next == len(self.pts):
                next = 0
            displacement = self.pts[n].p - self.pts[next].p
            distance = np.linalg.norm(displacement)
            pressure = self.constantp/currentv
            normal = np.array([displacement[1], -displacement[0]]) / distance
            if np.dot(normal, self.pts[n].p - self.center) < 0:
                normal = -normal
            self.pts[n].applyF(pressure*normal)
            self.pts[next].applyF(pressure*normal)
    
        