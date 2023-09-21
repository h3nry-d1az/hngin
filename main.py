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

@dataclass
class Camera(object):
    x: float
    y: float
    z: float
    theta_x: float = 0
    theta_y: float = 0

FOV = 1000

screen_size = (1280, 720)
view_distance = 640*8
vertex_size = 2

camera = Camera(0, 10, -35)
scale = 100
separation = 200


pygame.init()
pygame.display.set_caption('obj')

# CMUSerif = pygame.font.Font("cmunbx.ttf", 32)
CMUSerif = pygame.font.Font("cmunbx.ttf", 64)

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
                   camera: Camera) -> float:
        return min(max(0, (-255/view_distance)*(self.z-camera.z) + 255), 255)

    def project(self,
                camera: Camera) -> Tuple[float, float]:
        x = (self.x - camera.x)
        y = (self.y - camera.y)
        z = (self.z - camera.z)
        tx = camera.theta_y
        ty = camera.theta_x
        rotated = V(
            z*sin(ty)*cos(tx) + y*sin(tx)*sin(ty) + x*cos(ty),
            y*cos(tx) - z*sin(tx),
            -x*sin(ty) + y*sin(tx)*cos(ty) + z*cos(tx)*cos(ty)
        )
        return cartesian_to_pygame((rotated.x * FOV) // rotated.z,
                                   (rotated.y * FOV) // rotated.z)

    def render(self,
               camera: Camera) -> None:
        # if self.z <= camera.z:
        #     return (0, 0)
        
        size = min(max(0, (-vertex_size/view_distance)*(self.z-camera.z) + vertex_size), vertex_size)

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
               camera: Camera) -> None:
        pygame.draw.line(screen, (255, 255, 255),
                         self.vertex_1.project(camera),
                         self.vertex_2.project(camera))

@dataclass
class Model(object):
    vertices: List[V]
    lines: List[L] | None

    def render(self,
               camera: Camera) -> None:
        if self.lines:
            for line in self.lines:
                line.render(camera)

        for vertex in sorted(self.vertices, key=lambda v: v.brightness(camera)):
            vertex.render(camera)

    def transform(self, f: Callable[[V], V]):
        self.vertices = list(map(f, self.vertices))
        if self.lines:
            self.lines = list(map(lambda l: L(f(l.vertex_1), f(l.vertex_2)), self.lines))

@dataclass
class Scene(object):
    models: List[Model]

    def render(self,
               camera: Camera) -> None:
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
theta = .015*2

running = True
clock = pygame.time.Clock()
time = 0
freq = 4000

while running:
    delta = clock.tick(30)
    time += delta
    screen.fill((0, 0, 0))

    scene.render(camera)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera.x -= cos(camera.theta_x)*speed*delta
        camera.z -= sin(camera.theta_x)*speed*delta
    if keys[pygame.K_RIGHT]:
        camera.x += cos(camera.theta_x)*speed*delta
        camera.z += sin(camera.theta_x)*speed*delta
    if keys[pygame.K_UP]:
        camera.x -= sin(camera.theta_x)*speed*delta
        camera.y += sin(camera.theta_y)*speed*delta
        camera.z += cos(camera.theta_x)*speed*delta
    if keys[pygame.K_DOWN]:
        camera.x += sin(camera.theta_x)*speed*delta
        camera.y -= sin(camera.theta_y)*speed*delta
        camera.z -= cos(camera.theta_x)*speed*delta
    # if keys[pygame.K_w]:
    #     FOV += speed*delta
    # if keys[pygame.K_s]:
    #     FOV -= speed*delta
    if keys[pygame.K_a]:
        camera.theta_x += theta
    if keys[pygame.K_d]:
        camera.theta_x -= theta
    if keys[pygame.K_w]:
        camera.theta_y += theta
    if keys[pygame.K_s]:
        camera.theta_y -= theta
    if keys[pygame.K_SPACE]:
        camera.y += speed*delta
    if (keys[pygame.K_LSHIFT]) or \
       (keys[pygame.K_RSHIFT]):
        camera.y -= speed*delta

    scene.models[0].transform(lambda vertex: V(
            vertex.z*sin(theta) + vertex.x*cos(theta),
            vertex.y,
            vertex.z*cos(theta) - vertex.x*sin(theta)
        ))
    # camera.z = 40*abs(sin(time/4000)) -50
