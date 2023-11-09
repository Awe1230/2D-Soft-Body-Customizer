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
        # total = 0
        # for i in range(len(initial)):
        #     difference = final[i]-initial[i]
        #     if difference<math.pi:
        #         print(round(180*difference/math.pi, 4))
        #         difference = difference + 2*math.pi
        #     total = total + difference
        # total = total / len(initial)
        # return total
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
            # f = (self.v / v - 1) * self.b
            # t = np.array([t[1], -t[0]]) / d
            # if np.dot(t, self.pts[n].p - self.center) < 0:
            #     t = -t
            # self.pts[n].applyF(f*t)
            # self.pts[next].applyF(f*t)
            # xx[n] += f*t
            # xx[next] += f*t
        # for i in range(4):
        #     print(i, self.pts[i].p, "=", xx[i])
            pass

#         v = self.volume()
#         for n in range(len(self.pts)):
#             next = n + 1
#             if next == len(self.pts):
#                 next = 0
#             t = self.pts[n] - self.pts[next]
#             d = np.linalg.norm(t)
#             f = (self.v / v - 1) * self.b / d
#             t = np.array([t[1], -t[0]]) / d
#             if np.dot(t, self.pts[n] - self.center) < 0:
#                 t = -t
#             print(f*t)


# p5 = [np.array([0.0, 0.0]), np.array([0.0, 1.0]), np.array([1.0, 1.0]), np.array([1.0, 0.0])]
# press = Pressure(p5,1)
# press.inflate()
# p5[:] = [np.array([0.0, 0.0]), np.array([0.0, 0.7]), np.array([0.7, 0.7]), np.array([0.7, 0.0])]
# press.inflate()


# k = 1
# d = 1
# L = 2
# A = PointMass(np.array([0.0, 0.0]), np.array([0.0, -0.1]), np.array([0.0, 0.0]), 1, -6)
# B = PointMass(np.array([0.0, 1.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, -6)
# v = A.pts - B.pts
# x = np.linalg.norm(v)
# y = x
# if not x == 0:
#     totalr = v * k * (L - x) / x
#     y = (np.dot(B.v - A.v, v / x) * d) * v / x
#     #x = totalr + y
#     #y = y - totalr
# print(totalr, y)
    
        