# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600


def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices

class myPolygon():
    def __init__(self, nvertices = 3, radius=70, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.nvertices = nvertices
        self.vertices = getRegularPolygon(self.nvertices, radius=self.radius)

        self.color = color
        self.color_org = color

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position

        pygame.draw.polygon(screen, self.color, points)
#

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T
    pygame.draw.polygon(screen, color=color,
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine

    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 100
    h = 20
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]
    jointangle1 = 10
    jointangle2 = -30

    tick1 = 0
    tick2 = 0
    pinch = 0
    done = False
    while not done:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
           # jointangle1 += 1
            tick1 += 1
        elif keys[pygame.K_RIGHT]:
           # jointangle1 += 1
            tick2 += 1
        elif keys[pygame.K_SPACE] and pinch == 0:
           pinch += 5

        elif  keys[pygame.K_SPACE] and pinch != 0:
        #  input handling
            pinch*=-1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # drawing
        screen.fill( (200, 254, 219))

        # base
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(X, H0, screen, (0,0,0)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)
        x, y = H1[0,2], H1[1,2] # joint position
        H11 = H1 @ Rmat(-90) @ Tmat(0,-h/2)
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        #draw(X, H11, screen, (100,100,0)) # arm 1, 90 degree
        jointangle1 = 40 * np.sin(np.deg2rad(tick2)) #
        H12 = H11 @ Tmat(0, h/2) @ Rmat(jointangle1) @ Tmat(0, -h/2)
        draw(X, H12, screen, (200,200,0)) # arm 1, 90 degree

        # arm 2
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        jointangle2 = 40 * np.sin(np.deg2rad(tick1)) #
        H21 = H2 @ Rmat(jointangle2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0,0, 200))

        # arm 3
        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 3
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        jointangle3 = 40 * np.sin(np.deg2rad(tick1)) #
        H22 = H3 @ Rmat(jointangle3) @ Tmat(0, -h/2)
        draw(X, H22, screen, (0,0, 200))

        # pincher base
        Y = np.array([ [0,0], [20, 0], [20, 60], [0, 60] ])
        H4 = H22 @ Tmat(w, 0) @ Tmat(0, -h/2) # joint 4
        jointangle3 = 40 * np.sin(np.deg2rad(0)) #
        H23 = H4 @ Rmat(jointangle3) @ Tmat(0, -h/2)
        draw(Y, H23, screen, (0,0, 200))

        # pincher arm 1
        T = np.array([ [0,0], [30, 0], [30, 20], [0, 20] ])
        H5 = H23 @ Tmat(20, 0) @ Tmat(0, 50) # joint 4
        jointangle3 = 40 * np.sin(np.deg2rad(0)) #
        H24 = H5 @ Rmat(jointangle3) @ Tmat(0, -h/2 - pinch)
        draw(T, H24, screen, (0,0, 200))

        # pincher arm 2
        T = np.array([ [0,0], [30, 0], [30, 20], [0, 20] ])
        H5 = H23 @ Tmat(20, 0) @ Tmat(0, 10) # joint 4
        jointangle3 = 40 * np.sin(np.deg2rad(0)) #
        H24 = H5 @ Rmat(jointangle3) @ Tmat(0, -h/2 + pinch)
        draw(T, H24, screen, (0,0, 200))


        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()
