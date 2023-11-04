import numpy as np
from Classes.point_mass import PointMass

class Pressure:
    def __init__(self, pts, b):
        self.pts = pts
        self.v = self.volume()
        self.b = b*10**10
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
    
        