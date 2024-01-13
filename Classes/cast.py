import numpy as np
from Classes.point_mass import PointMass
import copy
import math
class Cast:
    def __init__(self, pts):
        self.pts = pts
        self.casted = copy.deepcopy(self.pts)
        self.coords = np.array([pt.p for pt in self.pts])
        self.c = self.center()
        self.a = self.tan(self.coords-self.c)
        self.l = self.length(self.coords)
        self.previousfinal = sum(self.a)-2*math.pi
        self.rotations = 0.0
    def center(self):
        return np.mean(np.array([pt.p for pt in self.pts]), axis = 0)
    def round(m, digit):
        m = (m*10**(digit+1))//10
        if m % 100 == 99:
            m = m + m/abs(m)
        return m/10**digit
    def tan(self, coords):
        angles = []
        for coord in coords:
            x, y = coord
            angle = math.pi/2
            if x > 0:
                angle = math.atan(y/x)
            elif x < 0:
                angle = math.pi + math.atan(y/x)
            elif y < 0:
                angle = 3 * math.pi/2
            angles.append(angle)
        return np.array(angles)
    def length(self, coords):
        lengths = []
        x, y = self.center()
        for coord in coords:
            lengths.append(((coord[0]-x)**2+(coord[1]-y)**2)**(1/2))
        return np.array(lengths)
    def angle(self, initial, final):
        i = sum(initial) - 2*math.pi
        f = sum(final) - 2*math.pi
        if f - self.previousfinal > 3*math.pi/2:
            self.rotations = self.rotations + 1
        elif self.previousfinal - f > 3*math.pi/2:
            self.rotations = self.rotations - 1
        difference = f - i - 2*math.pi*self.rotations
        difference = difference / len(initial)
        self.previousfinal = f
        return difference
    def caster(self, angles, lengths):
        coordinates = []
        for i in range(len(angles)):
            coordinates.append((round(lengths[i]*math.cos(angles[i]), 4), round(lengths[i]*math.sin(angles[i]), 4)))
        return np.array(coordinates)
    def solid(self):
        center = self.center()
        currentangle = self.tan(np.array([pt.p for pt in self.pts])-center)
        newangle = self.a + self.angle(self.a, currentangle)
        x = self.caster(newangle, self.l) + center
        return x
    
        