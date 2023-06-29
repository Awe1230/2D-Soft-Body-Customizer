from Classes.point_mass import PointMass
from Classes.spring import Spring
from Classes.poly import Poly
import numpy as np
import pygame

class Run:
    def __init__(self, full_screen):
        self.full_screen = full_screen
        self.pts = []
        self.springs = []
        self.polys = []

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
        blue = (0, 0, 255)
        radius = 5
        position = self.to_pygame([x.p[0], x.p[1]])
        pygame.draw.circle(self.screen, blue, position, radius)
    
    def draw_poly(self, x):
        x = x.p
        black = (0, 0, 0)
        width = 2
        for n in range(len(x)):
            z = n + 1
            if z == len(x):
                z = 0
            px = self.to_pygame(x[n])
            py = self.to_pygame(x[z])
            pygame.draw.line(self.screen, black, px, py, width=width)


    def draw_spring(self, spring):
        red = (255, 0, 0)
        width = 2
        px = self.to_pygame([spring.A.p[0], spring.A.p[1]])
        py = self.to_pygame([spring.B.p[0], spring.B.p[1]])
        pygame.draw.line(self.screen, red, px, py, width=width)

    def initialize_pts(self):
        s = 150.0
        x = 575.0
        y = 375.0
        f = False
        g = -5
        x1 = PointMass(np.array([x, y]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        self.pts.append(x1)
        x2 = PointMass(np.array([x+s, y+s]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        self.pts.append(x2)
        x3 = PointMass(np.array([x+s, y]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        self.pts.append(x3)
        x4 = PointMass(np.array([x, y+s]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), 1, g, f, f)
        self.pts.append(x4)
    
    def initialize_polys(self):
        p1 = Poly(np.array([(200, 200), (200, 300), (800, 300), (800, 200)]))
        self.polys.append(p1)
        # p2 = Poly(np.array([(700, 200), (900, 200), (900, 300), (700, 250)]))
        # self.polys.append(p2)

    def initialize_springs(self):
        d = 0.3
        spring1 = Spring(self.pts[0], self.pts[1], 1, d)
        self.springs.append(spring1)
        spring2 = Spring(self.pts[0], self.pts[2], 1, d)
        self.springs.append(spring2)
        spring3 = Spring(self.pts[0], self.pts[3], 1, d)
        self.springs.append(spring3)
        spring1 = Spring(self.pts[1], self.pts[2], 1, d)
        self.springs.append(spring1)
        spring2 = Spring(self.pts[1], self.pts[3], 1, d)
        self.springs.append(spring2)
        spring3 = Spring(self.pts[2], self.pts[3], 1, d)
        self.springs.append(spring3)

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
                p.collide(pt)
            if (pt.l or pt.c) and pygame.mouse.get_pressed()[0]:
                pt.P = np.array(self.to_pygame(pygame.mouse.get_pos()))
            self.draw_pt(pt)
            dt = 0.05
            pt.step(dt)

    def run(self):

        self.initialize_pts()
        self.initialize_polys()
        self.initialize_springs()

        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            self.update_frame()
            # pygame.time.delay(200)
            pygame.time.Clock().tick(60)

            # Update the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()