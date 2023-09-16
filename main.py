# https://math.stackexchange.com/questions/2305792/3d-projection-on-a-2d-plane-weak-maths-ressources
# https://en.wikipedia.org/wiki/Projection_(linear_algebra)
# https://en.wikipedia.org/wiki/3D_projection
# https://en.wikipedia.org/wiki/Painter%27s_algorithm
# https://free3d.com/3d-model/low-poly-male-26691.html
from dataclasses import dataclass
from typing import Tuple, List
from math import sin, cos
import pygame

def cartesian_to_pygame(
    x: int,
    y: int
) -> Tuple[int, int]:
    return (x + screen_size[0]//2,
            screen_size[1]//2 - y)

# FOVx = 5
# FOVy = 5
FOV = 1000

# screen_size = (640, 480)
# view_distance = 640*2
# vertex_size = 10

# camera = [0, 0, -200]
# scale = 50
# separation = 100

screen_size = (1280, 720)
view_distance = 640*8
vertex_size = 2

camera = [0, 15, -50]
scale = 100
separation = 200


pygame.init()
pygame.display.set_caption('obj')

# CMUSerif = pygame.font.Font("cmunbx.ttf", 32)
CMUSerif = pygame.font.Font("cmunbx.ttf", 64)
orthogonal_text = CMUSerif.render("Importación de archivos OBJ", True, (255, 255, 255))
solovertices_text = CMUSerif.render("(sólo vértices)", True, (255, 255, 255))
orthogonal_text_rect = orthogonal_text.get_rect()
orthogonal_text_rect.center = (screen_size[0]//2, screen_size[1]//12)
solovertices_text_rect = solovertices_text.get_rect()
solovertices_text_rect.center = (screen_size[0]//2, screen_size[1]//5)

# orthogonal_matrix_image = pygame.image.load("lerp.png")
# orthogonal_matrix_image = pygame.transform.scale(orthogonal_matrix_image, (orthogonal_matrix_image.get_width()*9//10,
#                                                                            orthogonal_matrix_image.get_height()*9//10))

screen = pygame.display.set_mode(screen_size)

@dataclass
class V(object):
    x: int
    y: int
    z: float

    def move(self,
             x: int,
             y: int,
             z: float) -> None:
        self.x += x
        self.y += y
        self.z += z

    def brightness(self,
                   camera: List[int]) -> float:
        return min(max(0, (-255/view_distance)*(self.z-camera[2]) + 255), 255)

    def project(self,
                camera: List[int]) -> Tuple[int, int]:
        # ORTHOGONAL PROJECTION
        # coordinates = (self.x - camera[0],
        #                self.y - camera[1])

        coordinates = (((self.x-camera[0]) * FOV) // (self.z-camera[2]),
                       ((self.y-camera[1]) * FOV) // (self.z-camera[2]))

        # coordinates = (((self.x - camera[0]) * ((self.z - camera[2])/self.z)) + camera[0],
        #                ((self.y - camera[1]) * ((self.z - camera[2])/self.z)) + camera[1])

        return cartesian_to_pygame(*coordinates)

    def render(self,
               camera: List[int]) -> None:
        if self.z <= camera[2]:
            return (0, 0)
        
        size = min(max(0, (-vertex_size/view_distance)*(self.z-camera[2]) + vertex_size), vertex_size)

        # print(self.project(camera), self.brightness(camera), size)
        pygame.draw.circle(screen,
                           (self.brightness(camera),
                            self.brightness(camera), 
                            self.brightness(camera)),
                           self.project(camera),
                           size)

def parse_obj_model(path: str) -> List[V]:
    with open(path, 'r') as object:
        data = object.read().replace('\n\n', '\n')
        # print(data.split('\n'))
        vertexes = []
        for line in data.split('\n'):
            if len(line) == 0:
                continue
            elif line[0] == 'v' and line[1] == ' ':
                params = line.split(' ')
                # print(params)
                vertexes.append(V(float(params[1]), float(params[2]), float(params[3])))
        return vertexes

model = parse_obj_model('model.obj')

speed = 1
# theta = .005
# theta = .01
theta = .015

running = True
clock = pygame.time.Clock()

while running:
    delta = clock.tick(30)
    screen.fill((0, 0, 0))
    screen.blit(orthogonal_text, orthogonal_text_rect)
    screen.blit(solovertices_text, solovertices_text_rect)
    # screen.blit(orthogonal_matrix_image, (screen_size[0]//2 - orthogonal_matrix_image.get_width()//2, 9*screen_size[1]//12))

    # for vertex_1 in model:
    #     for vertex_2 in model:
    #         if vertex_1 == vertex_2:
    #             continue
    #         coordinates_1 = vertex_1.project(camera)
    #         coordinates_2 = vertex_2.project(camera)
    #         if coordinates_1 == (0, 0) or\
    #            coordinates_2 == (0, 0):
    #             continue
    #         pygame.draw.line(screen, (255, 255, 255), coordinates_1, coordinates_2)

    for vertex in sorted(model, key=lambda v: v.brightness(camera)):
        vertex.render(camera)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera[0] -= speed*delta
    if keys[pygame.K_RIGHT]:
        camera[0] += speed*delta
    if keys[pygame.K_UP]:
        camera[2] += speed*delta
    if keys[pygame.K_DOWN]:
        camera[2] -= speed*delta
    if keys[pygame.K_w]:
        FOV += speed*delta
    if keys[pygame.K_s]:
        FOV -= speed*delta
    if keys[pygame.K_SPACE]:
        camera[1] += speed*delta
    if (keys[pygame.K_LSHIFT]) or \
       (keys[pygame.K_RSHIFT]):
        camera[1] -= speed*delta

    model = list(map(lambda vertex: V(
            vertex.z*sin(theta) + vertex.x*cos(theta),
            vertex.y,
            vertex.z*cos(theta) - vertex.x*sin(theta)
        ), model))
