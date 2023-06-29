import numpy as np
import Classes.point_mass
class Spring:
    """
    A, B: Point masses on ends of spring
    L: resting length of spring
    k: stiffness of spring
    d: damping factor of spring
    """
    def __init__(self, A, B, k, d):
        self.A = A
        self.B = B 
        self.L = np.linalg.norm(A.p - B.p)
        self.k = k
        self.d = d

    def applyForce(self):
        v = self.A.p - self.B.p
        x = np.linalg.norm(v)
        if not x == 0:
            x = v * self.k * (self.L - x) / x + (np.dot(self.B.v - self.A.v, v / x) * self.d) * v / x
        else:
            x = np.array([x, x])
        self.A.applyF(x)
        self.B.applyF(-x)