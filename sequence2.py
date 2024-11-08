from dataclasses import dataclass
from typing import Tuple, List, Callable
from functools import reduce
from math import sin, cos, sqrt
from random import randrange
import pygame

def cartesian_to_pygame(
    x: int,
    y: int
) -> Tuple[int, int]:
    return (x + screen_size[0]//2,
            screen_size[1]//2 - y)

def pygame_to_cartesian(
    x: int,
    y: int
) -> Tuple[int, int]:
    return (x - screen_size[0]//2,
            screen_size[1]//2 - y)

FOV = 1000

screen_size = (1280, 720)
view_distance = 640*8
vertex_size = 2

camera = [10, 11, -35]
scale = 100
separation = 200

pygame.init()
pygame.display.set_caption('sequence 2')

screen = pygame.display.set_mode(screen_size)

sequence = 0

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

    def project(
        self,
        camera: List[float]
    ) -> Tuple[float, float]:

        coordinates = (((self.x-camera[0]) * FOV) // (self.z-camera[2]),
                       ((self.y-camera[1]) * FOV) // (self.z-camera[2]))

        return cartesian_to_pygame(*coordinates)

    def render(self,
               camera: List[float]) -> None:
        if self.z <= camera[2]:
            return (0, 0)
        
        size = min(max(0, (-vertex_size/view_distance)*(self.z-camera[2]) + vertex_size), vertex_size)

        pygame.draw.circle(
            screen,
            (
                self.brightness(camera),
                self.brightness(camera), 
                self.brightness(camera)
            ),
            self.project(camera),
            size
        )

@dataclass
class F(object):
    vertex_1: V
    vertex_2: V
    vertex_3: V
    color: Tuple[int, int, int]

    def render(
        self,
        camera: List[float],
    ) -> None:
        pygame.draw.polygon(screen, (255, 255, 255), (
            self.vertex_1.project(camera),
            self.vertex_2.project(camera),
            self.vertex_3.project(camera)
        ), width=1)

    @property
    def center(self) -> V:
        xs = [self.vertex_1.x, self.vertex_2.x, self.vertex_3.x]
        ys = [self.vertex_1.y, self.vertex_2.y, self.vertex_3.y]
        zs = [self.vertex_1.z, self.vertex_2.z, self.vertex_3.z]

        return V(
            (max(xs) + min(xs)) / 2,
            (max(ys) + min(ys)) / 2,
            (max(zs) + min(zs)) / 2,
        )

    def project(self, camera):
        return F(
            V(*pygame_to_cartesian(*self.vertex_1.project(camera)), 0),
            V(*pygame_to_cartesian(*self.vertex_2.project(camera)), 0),
            V(*pygame_to_cartesian(*self.vertex_3.project(camera)), 0),
            self.color
        )

@dataclass
class Model(object):
    vertices: List[V]
    faces: List[F] | None

    def render(
        self,
        camera: List[float],
        no_dots: bool = False,
    ) -> None:
        if self.faces:
            for face in sorted(self.faces, key=lambda f: f.center.brightness(camera)):
                face.render(camera)

        if no_dots:
            return

        for vertex in sorted(self.vertices, key=lambda v: v.brightness(camera)):
            vertex.render(camera)

    def transform(self, f: Callable[[V], V]):
        self.vertices = list(map(f, self.vertices))
        if self.faces:
            transformed_faces = []
            for face in self.faces:
                transformed_faces.append(F(f(face.vertex_1), f(face.vertex_2), f(face.vertex_3), face.color))
            self.faces = transformed_faces

    def project(self, camera):
        return Model(
            [V(*pygame_to_cartesian(*vertex.project([0, 11, -35])), 0) for vertex in self.vertices],
            [face.project([0, 11, -35]) for face in self.faces]
        )

@dataclass
class Scene(object):
    models: List[Model]

    def render(self,
               camera: List[int]) -> None:
        faces = reduce(lambda f1, f2: f1 + f2, map(lambda m: m.faces, self.models))
        if faces:
            for face in faces:
                face.render(camera)
        vertices = reduce(lambda v1, v2: v1 + v2, map(lambda m: m.vertices, self.models))
        for vertex in sorted(vertices, key=lambda v: v.brightness(camera)):
            vertex.render(camera)

def parse_obj_model(path: str) -> Model:
    with open(path, 'r') as object:
        data = object.read()
        # print(data.split('\n'))
        vertices = []
        total_faces = []
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
                    try:
                        normalized.append(int(p.split('/')[0]))
                    except ValueError:
                        continue
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
                    total_faces.append(F(face[0], face[1], face[2], (
                        randrange(256),
                        randrange(256),
                        randrange(256)
                    )))
        return Model(vertices, total_faces)

model = parse_obj_model('human.obj')
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

    scene.models[0].render(camera, no_dots=True)

    projected_model = scene.models[0].project(camera)
    projected_model.transform(lambda vertex: V(vertex.x/34 + 35, vertex.y/34 + 10, 80))
    v1 = projected_model.project(camera).vertices[1]
    print(cartesian_to_pygame(v1.x, v1.y))
    projected_model.render(camera, no_dots=True)
    pygame.draw.line(screen, (255, 255, 255), (690, 280), (320 + 690, 280))
    pygame.draw.line(screen, (255, 255, 255), (690, 280), (690, 180 + 280))
    pygame.draw.line(screen, (255, 255, 255), (690, 180 + 280), (320 + 690, 180 + 280))
    pygame.draw.line(screen, (255, 255, 255), (320 + 690, 280), (320 + 690, 180 + 280))

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