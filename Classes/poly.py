import numpy as np
import Classes.point_mass
class Poly:
    def __init__(self, p, i, r):
        self.p = p
        
        self.i = i
        self.r = r
        if i == None:
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

    def move(self, r):
        if self.i != None:
            self.p = self.i.p

    def collide(self, P):

        if P != self.i:
            if self.i == None:
                m = P.p.copy()
                n = 0
                c = np.array([0.0,0.0])
                if m[0] <= self.h[0] and m[1] <= self.h[1] and m[0] >= self.l[0] and m[1] >= self.l[1]:
                        for x in range(len(self.p)):
                            z = x + 1
                            if z == len(self.p):
                                z = 0
                            xm, ym, x1, y1, x2, y2 = *m, *self.p[x], *self.p[z]
                            k = self.closestP(x1, y1, x2, y2, xm, ym)
                            if np.linalg.norm(c-m) > np.linalg.norm(k-m):
                                c = k.copy()
                            if (y2 <= ym and ym <= y1) or (y1 <= ym and ym <= y2):
                                if x1 <= xm and x2 <= xm:
                                    n += 1
                                
                                elif x1 <= xm:
                                    t = (ym >= self.getypoint(x1, y1, x2, y2, xm))
                                    if (y1 < ym):
                                        t = not t
                                    elif y1==ym:
                                        t = True
                                    n += t
                                elif x2 <= xm:
                                    t = (ym <= self.getypoint(x1, y1, x2, y2, xm))
                                    if (y2 > ym):
                                        t = not t
                                    elif y2 == ym:
                                        t = True
                                    n += t
                if n % 2 == 1:
                    P.reflectV(c-m)
                    P.p = c.copy()
            else:
                m = P.p.copy()
                t = m - self.p
                s = np.linalg.norm(t)
                if s < self.r:
                    if s == 0:
                        s = 1
                        t = np.array([1, 1])

                    P.reflectV(t)
                    P.p = self.p + t*self.r/s
    
# p1 = Poly(np.array([500, 400[]]))
# p1.collide(np.array([500.0, 300.0]))
# print(p1.closestP(600, 200, 200, 300, 500, 250))




