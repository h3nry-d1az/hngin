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

camera = [0, 0.25, -2]
scale = 100
separation = 200

pygame.init()
pygame.display.set_caption('sequence 6')

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

    def __add__(self, other):
        assert isinstance(other, V)
        return V(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        assert isinstance(other, V)
        return V(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return V(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return V(self.x / other, self.y / other, self.z / other)

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __matmul__(self, other):
        assert isinstance(other, V)
        return self.x*other.x + self.y*other.y + self.z*other.z

@dataclass
class F(object):
    vertex_1: V
    vertex_2: V
    vertex_3: V
    color: Tuple[int, int, int]

    def render(
        self,
        camera: List[float],
        light: V
    ) -> None:
        v1 = self.vertex_1.project(camera)
        v2 = self.vertex_2.project(camera)
        v3 = self.vertex_3.project(camera)
        brightness = -(light @ N)
        final_color = max(self.color[0]*brightness, 0),\
                      max(self.color[1]*brightness, 0),\
                      max(self.color[2]*brightness, 0)
        pygame.draw.polygon(screen, final_color, (
            v1, v2, v3
        ))
        pygame.draw.polygon(screen, (255, 255, 255), (
            v1, v2, v3
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
        light: V,
        no_dots: bool = False,
    ) -> None:
        if self.faces:
            for face in sorted(self.faces, key=lambda f: f.center.brightness(camera)):
                face.render(camera, light)

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

face_vertex_1 = V(0.125, 0.15, -1)
face_vertex_2 = V(0.625, 0, -0.5)
face_vertex_3 = V(0.3, 0.35, -1.25)

A = face_vertex_2 - face_vertex_1
B = face_vertex_3 - face_vertex_1

N = V(
    A.y * B.z - A.z * B.y,
    A.z * B.x - A.x * B.z,
    A.x * B.y - A.y * B.x
)
N = N / (2*abs(N)) # the 2 is just there for the sake of a better representation
print(N)

light_beam_start = V(0, 0, 0)
light_beam_end = V(0, 0, 0)

model = Model(
    [face_vertex_1, face_vertex_2, face_vertex_3], 
    [F(face_vertex_1, face_vertex_2, face_vertex_3, (
        randrange(256),
        randrange(256),
        randrange(256)
    ))],
)
# size = 50
# model.transform(lambda v: V(size*v.x, size*v.y, size*v.z))
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

    light_beam_end = V(cos(time/1000)/2, sin(time/1000)/2, 0)

    scene.models[0].render(camera, light_beam_end*2, no_dots=True)
    pygame.draw.line(screen, (255, 255, 255),
        model.faces[0].center.project(camera),
        (model.faces[0].center + N).project(camera),
    width=5)

    start = light_beam_start.project(camera)
    start = start[0] - 300, start[1] - 200

    end = light_beam_end.project(camera)
    end = end[0] - 300, end[1] - 200

    pygame.draw.line(screen, (255, 255, 255), start, end, width=5)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # scene.models[0].transform(lambda vertex: V(
    #         vertex.z*sin(theta) + vertex.x*cos(theta),
    #         vertex.y,
    #         vertex.z*cos(theta) - vertex.x*sin(theta)
    #     ))