from Classes.point_mass import PointMass
from Classes.spring import Spring
from Classes.pressure import Pressure
from Classes.poly import Poly
import numpy as np
import pygame

class Run:
    def __init__(self, full_screen):
        self.full_screen = full_screen
        self.pts = []
        self.springs = []
        self.polys = []
        self.r = 25.0

        pygame.init()

        # Set up the drawing window
        if self.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode([1200, 700])

    def to_pygame(self, x):
        """Convert coordinates into pygame coordinates (lower-left => top left)."""
        height = self.screen.get_height()
        return (x[0], height - x[1])

    def draw_pt(self, x):
        blue = (40, 40, 40)
        radius = 5
        position = self.to_pygame([x.p[0], x.p[1]])
        pygame.draw.circle(self.screen, blue, position, self.r/2)
    
    def draw_poly(self, y):
        x = y.p.copy()
        black = (255, 255, 255)
        width = 2
        if y.i == None:
            for n in range(len(x)):
                z = n + 1
                if z == len(x):
                    z = 0
                px = self.to_pygame(x[n])
                py = self.to_pygame(x[z])
                pygame.draw.line(self.screen, black, px, py, width=width)


    def draw_spring(self, spring):
        red = (255, 255, 255)
        width = 2
        px = self.to_pygame([spring.A.p[0], spring.A.p[1]])
        py = self.to_pygame([spring.B.p[0], spring.B.p[1]])
        pygame.draw.line(self.screen, red, px, py, width=width)

    def initialize_pts(self):
        s = 40.0
        x = 400.0
        y = 200.0
        t = True
        f = False
        g = -5
        p1 = PointMass(np.array([x, y]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        p2 = PointMass(np.array([x, y + s]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, True)
        p3 = PointMass(np.array([x + s, y + s]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        p4 = PointMass(np.array([x + s, y]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        self.pts.append(p1)
        self.pts.append(p2)
        self.pts.append(p3)
        self.pts.append(p4)
        self.polys.append(Poly(np.array(p1.p.copy()), p1, self.r))
        self.polys.append(Poly(np.array(p2.p.copy()), p2, self.r))
        self.polys.append(Poly(np.array(p3.p.copy()), p3, self.r))
        self.polys.append(Poly(np.array(p4.p.copy()), p4, self.r))
    
    def initialize_polys(self):
        p1 = Poly(np.array([(200.0, 500.0), (700.0, 400.0), (200.0, 400.0)]), i = None, r = None)
        self.polys.append(p1)
        p2 = Poly(np.array([(700.0, 190.0), (1150.0, 190.0), (1150.0, 250.0), (700.0, 200.0)]), i = None, r = None)
        self.polys.append(p2)
        p3 = Poly(np.array([(200, -10.0), (300, -10.0), (250.0, 300.0)]), i = None, r = None)
        self.polys.append(p3)
        p4 = Poly(np.array([(650.0, 600.0), (1150.0, 600.0), (1150.0, 700.0), (600.0, 700.0)]), i = None, r = None)
        self.polys.append(p4)
        pass

    def initialize_springs(self):
        s = 0.0
        d = 0.0
        spring1 = Spring(self.pts[0], self.pts[1], s, d)
        self.springs.append(spring1)
        spring2 = Spring(self.pts[0], self.pts[3], s, d)
        self.springs.append(spring2)
        spring3 = Spring(self.pts[2], self.pts[3], s, d)
        self.springs.append(spring3)
        spring4 = Spring(self.pts[1], self.pts[2], s, d)
        self.springs.append(spring4)
    
    def initialize_body(self, x, y, s, m, n, k):
        g = -9.8
        f = False
        l = k/3
        for j in range(n):
            for i in range(m):
                p = PointMass(np.array([x + s*i, y - s*j]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
                self.pts.append(p)
                x1, y1 = p.p
                self.polys.append(Poly(np.array([x1, y1]), p, self.r))
        for d in range(len(self.pts)-1):
            i = d % m
            j = d // m
            if j < n - 1:
                self.springs.append(Spring(self.pts[j * m + i], self.pts[(j + 1) * m + i], k, l))
                if i > 0:
                    self.springs.append(Spring(self.pts[j * m + i], self.pts[(j + 1) * m + (i - 1)], k, l))
                if i < m - 1:
                   
                    self.springs.append(Spring(self.pts[j * m + i], self.pts[(j + 1) * m + (i + 1)], k, l))
            if i < m - 1:
                self.springs.append(Spring(self.pts[j * m + i], self.pts[j * m + (i + 1)], k, l))

    def update_frame(self):
        for p in self.polys:
            self.draw_poly(p)

        for pt in self.pts:
            pt.eraseA()

        for spring in self.springs:
            self.draw_spring(spring)
            spring.applyForce()
        for pt in self.pts:
            for p in self.polys:
                p.move(self.r)
                p.collide(pt)
            if (pt.l or pt.c) and pygame.mouse.get_pressed()[0]:
                pt.updateP(np.array(self.to_pygame(pygame.mouse.get_pos())))
            self.draw_pt(pt)
            dt = 0.05
            pt.step(dt)

    def run(self):

        # self.initialize_pts()

        # self.initialize_springs()
        self.initialize_body(400.0, 710.0, 40.0, 5, 6, 10.0)
        self.initialize_polys()

        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill((100, 100, 100))

            self.update_frame()
            # pygame.time.delay(200)
            pygame.time.Clock().tick(60)

            # Update the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()