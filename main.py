# https://math.stackexchange.com/questions/2305792/3d-projection-on-a-2d-plane-weak-maths-ressources
# https://en.wikipedia.org/wiki/Projection_(linear_algebra)
# https://en.wikipedia.org/wiki/3D_projection
# https://en.wikipedia.org/wiki/Painter%27s_algorithm
# http://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm
# https://cs418.cs.illinois.edu/website/text/obj.html
# https://free3d.com/3d-model/low-poly-male-26691.html
from dataclasses import dataclass
from typing import Tuple, List, Callable
from functools import reduce
from math import sin, cos
import pygame

def cartesian_to_pygame(
    x: int,
    y: int
) -> Tuple[int, int]:
    return (x + screen_size[0]//2,
            screen_size[1]//2 - y)

FOV = 1000

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
solovertices_text = CMUSerif.render("(vértices y caras)", True, (255, 255, 255))
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
    x: float
    y: float
    z: float

    def move(self,
             x: float,
             y: float,
             z: float) -> None:
        self.x += x
        self.y += y
        self.z += z

    def brightness(self,
                   camera: List[float]) -> float:
        return min(max(0, (-255/view_distance)*(self.z-camera[2]) + 255), 255)

    def project(self,
                camera: List[float]) -> Tuple[float, float]:
        # ORTHOGONAL PROJECTION
        # coordinates = (self.x - camera[0],
        #                self.y - camera[1])

        coordinates = (((self.x-camera[0]) * FOV) // (self.z-camera[2]),
                       ((self.y-camera[1]) * FOV) // (self.z-camera[2]))

        # coordinates = (((self.x - camera[0]) * ((self.z - camera[2])/self.z)) + camera[0],
        #                ((self.y - camera[1]) * ((self.z - camera[2])/self.z)) + camera[1])

        return cartesian_to_pygame(*coordinates)

    def render(self,
               camera: List[float]) -> None:
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

@dataclass
class L(object):
    vertex_1: V
    vertex_2: V

    def render(self,
               camera: List[float]) -> None:
        pygame.draw.line(screen, (255, 255, 255),
                         self.vertex_1.project(camera),
                         self.vertex_2.project(camera))

@dataclass
class Model(object):
    vertices: List[V]
    lines: List[L] | None

    def render(self,
               camera: List[float]) -> None:
        if self.lines:
            for line in self.lines:
                line.render(camera)

        for vertex in sorted(self.vertices, key=lambda v: v.brightness(camera)):
            vertex.render(camera)

    def transform(self, f: Callable[[V], V]):
        self.vertices = list(map(f, self.vertices))
        if self.lines:
            transformed_lines = []
            for line in self.lines:
                transformed_lines.append(L(f(line.vertex_1), f(line.vertex_2)))
            self.lines = transformed_lines

@dataclass
class Scene(object):
    models: List[Model]

    def render(self,
               camera: List[int]) -> None:
        lines = reduce(lambda l1, l2: l1 + l2, map(lambda m: m.lines, self.models))
        if lines:
            for line in lines:
                line.render(camera)
        vertices = reduce(lambda v1, v2: v1 + v2, map(lambda m: m.vertices, self.models))
        for vertex in sorted(vertices, key=lambda v: v.brightness(camera)):
            vertex.render(camera)

def parse_obj_model(path: str) -> Model:
    with open(path, 'r') as object:
        data = object.read()
        # print(data.split('\n'))
        vertices = []
        lines = []
        for line in data.split('\n'):
            if len(line) == 0:
                continue
            elif line[0:2] == 'v ':
                params = line.split(' ')
                # print(params)
                vertices.append(V(float(params[1]), float(params[2]), float(params[3])))
            elif line[0:2] == 'f ':
                params = line.split(' ')
                normalized = []
                for p in params[1:]:
                    normalized.append(int(p.split('/')[0]))
                faces = []
                for i in range(1, len(normalized)+1):
                    try:
                        faces.append([vertices[normalized[0]-1],
                                      vertices[normalized[i]-1],
                                      vertices[normalized[i+1]-1]])
                    except IndexError:
                        break
                # print(faces, line, normalized)
                for face in faces:
                    lines.append(L(face[0], face[1]))
                    lines.append(L(face[1], face[2]))
                    lines.append(L(face[2], face[0]))
        return Model(vertices, lines)

model = parse_obj_model('model.obj')
scene = Scene([model])

speed = .05
theta = .015

running = True
clock = pygame.time.Clock()
time = 0
freq = 4000

while running:
    delta = clock.tick(30)
    time += delta
    screen.fill((0, 0, 0))
    screen.blit(orthogonal_text, orthogonal_text_rect)
    screen.blit(solovertices_text, solovertices_text_rect)

    scene.render(camera)

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

    scene.models[0].transform(lambda vertex: V(
            vertex.z*sin(theta) + vertex.x*cos(theta),
            vertex.y,
            vertex.z*cos(theta) - vertex.x*sin(theta)
        ))
    camera[2] = 40*abs(sin(time/4000)) -50
