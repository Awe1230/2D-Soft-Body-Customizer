import numpy as np
import Classes.point_mass
class Poly:
    def __init__(self, p):
        self.p = p
        self.h = p[0]
        self.l = p[1]
        for x in p:
            self.h = max(self.h[0], x[0]), max(self.h[1], x[1])
            self.l = min(self.l[0], x[0]), min(self.l[1], x[1])



    def getypoint(self, x1, y1, x2, y2, mx):
        m = (y2-y1)/(x2-x1)
        return m*(mx-x1)+y1


    def closestP(self, x1, y1, x2, y2, mx, my):
        #Normal is y - my = ((x1-x2)/(y2-y1))*(x - mx)
        #Line is y - y1 = ((y2-y1)/(x2-x1)) * (x - x1)
        #Slope of line is m
        a = np.array([x2, mx])
        if x1 - x2 == 0:
            return a
        else:
            m = (y2-y1)/(x2-x1)
        #(x - mx) = -m**2 * (x - x1) + m(my - y1)
        #(x-mx) + m**2 * (x - x1) = m(my-y1)
        #(m**2+1)x = m(my-y1) + mx + m**2 * x1
            x = (m * (my - y1) + mx + m**2 * x1) / (m**2 + 1)
            y = m * (x - x1) + y1
            if not (((x1 <= x and x <= x2) or (x2 <= x and x <= x1)) or ((y1 <= y and y <= y2) or (y2 <= y and y <= y1))):
                if ((x2 - mx) ** 2 + (y2 - my) ** 2) ** (1/2) > ((x1 - mx) ** 2 + (y1 - my) ** 2) ** (1/2):
                    a = np.array([x1, y1])
                else:
                    a = np.array([x2, y2])
            else:
                a = np.array([x, y])
        return a


    def collide(self, P):
        m = P.p
        n = 0
        c = np.array([0,0])
        if m[0] <= self.h[0] and m[1] <= self.h[1]:
            if m[0] >= self.l[0] and m[1] >= self.l[1]:
                for x in range(len(self.p)):
                    z = x + 1
                    if z == len(self.p):
                        z = 0
                    xm, ym, x1, y1, x2, y2 = *m, *self.p[x], *self.p[z]
                    k = self.closestP(x1, y1, x2, y2, xm, ym)
                    if np.linalg.norm(c-m) > np.linalg.norm(k-m):
                        c = k
                    if (y2 <= ym and ym <= y1) or (y1 <= ym and ym <= y2):
                        if x1 <= xm and x2 <= xm:
                            n += 1
                        elif x1 <= xm:
                            n += (ym <= self.getypoint(x1, y1, x2, y2, xm))
                        elif x2 <= xm:
                            n += (ym >= self.getypoint(x1, y1, x2, y2, xm))
        if n % 2 == 1:
            P.reflectV(c-m)
            P.p = c
            
# p1 = Poly(np.array([(200, 200), (200, 250), (800, 300), (800, 200)]))
# x = np.array([500, 300])
# # p1.collide(x)
# print(p1.closestP(200, 250, 800, 300, 500, 300))
    
    




