# https://math.stackexchange.com/questions/2305792/3d-projection-on-a-2d-plane-weak-maths-ressources
# https://en.wikipedia.org/wiki/Projection_(linear_algebra)
# https://en.wikipedia.org/wiki/3D_projection
# https://en.wikipedia.org/wiki/Painter%27s_algorithm
# http://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm
# https://cs418.cs.illinois.edu/website/text/obj.html
# https://free3d.com/3d-model/low-poly-male-26691.html
from dataclasses import dataclass
from typing import Tuple, List, Callable
from copy import deepcopy
from math import sin, cos
import pygame
import tkinter as tk

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

FOV_label = tk.Label(text='FOV (field of view)')
FOV_label.pack()
FOV_slider = tk.Scale(from_=0, to=2000, orient=tk.HORIZONTAL)
FOV_slider.set(1000)
FOV_slider.pack()

# screen_size = (1280, 720)
screen_size = (640, 480)

vertex_size_label = tk.Label(text='Vertex size')
vertex_size_label.pack()
vertex_size_slider = tk.Scale(from_=0, to=10, orient=tk.HORIZONTAL)
vertex_size_slider.set(1)
vertex_size_slider.pack()

camera = Camera(0, 8, -50)

pygame.init()
pygame.display.set_caption('hngin -- v0.0.1')

font = pygame.font.SysFont(None, 38)

screen = pygame.display.set_mode(screen_size)
interface = tk.Tk()
interface.withdraw()

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
        return cartesian_to_pygame((rotated.x * FOV_slider.get()) // rotated.z,
                                   (rotated.y * FOV_slider.get()) // rotated.z)

    def render(self,
               camera: Camera) -> None:
        # if self.z <= camera.z:
        #     return (0, 0)

        pygame.draw.circle(screen,
                           (255, 255, 255),
                           self.project(camera),
                           vertex_size_slider.get())

@dataclass
class L(object):
    vertex_1: V
    vertex_2: V

    def render(self,
               camera: Camera,
               color: Tuple[int, int, int]) -> None:
        pygame.draw.line(screen, color,
                         self.vertex_1.project(camera),
                         self.vertex_2.project(camera))

@dataclass
class Model(object):
    vertices: List[V]
    lines: List[L] | None
    color: Tuple[int, int, int]

    def render(self,
               camera: Camera) -> None:
        if self.lines:
            for line in self.lines:
                line.render(camera, self.color)

        for vertex in self.vertices:
            vertex.render(camera)

    def transform(self, f: Callable[[V], V]) -> None:
        self.vertices = list(map(f, self.vertices))
        if self.lines:
            self.lines = list(map(lambda l: L(f(l.vertex_1), f(l.vertex_2)), self.lines))

@dataclass
class Scene(object):
    models: List[Model]

    def render(self,
               camera: Camera) -> None:
        for model in self.models:
            model.render(camera)

def parse_obj_model(path: str,
                    color: Tuple[int, int, int]) -> Model:
    with open(path, 'r') as object:
        data = object.read()
        vertices = []
        lines = []
        for line in data.split('\n'):
            if len(line) == 0:
                continue
            elif line[0:2] == 'v ':
                params = line.split(' ')
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
        return Model(vertices, lines, color)

model = parse_obj_model('models/human.obj', (0, 255, 0))
model.transform(lambda v: V(
    v.x*.75,
    v.y*.75,
    v.z*.75,
))
cube = parse_obj_model('models/cube.obj', (0, 0, 255))
cube.transform(lambda v: V(
    v.x + 9,
    v.y + 8,
    v.z + 6
))
pyramid = parse_obj_model('models/pyramid.obj', (255, 255, 0))
pyramid.transform(lambda v: V(
    v.x*6 - 10,
    v.y*6 + 8,
    v.z*6 + 6
))
base_icosahedron = parse_obj_model('models/icosahedron.obj', (255, 0, 0))
base_icosahedron.transform(
    lambda v: V(
        v.x*3 - 13,
        v.y*3 + 5,
        v.z*3 + 8
    )
)
render_icosahedron = deepcopy(base_icosahedron)
scene = Scene([cube, pyramid, render_icosahedron, model])

speed_label = tk.Label(text='Camera speed')
speed_label.pack()
speed_slider = tk.Scale(from_=0, to=.5*100, orient=tk.HORIZONTAL)
speed_slider.set(.05*100)
speed_slider.pack()

theta_label = tk.Label(text='Rotation speed')
theta_label.pack()
theta_slider = tk.Scale(from_=0, to=.5*100, orient=tk.HORIZONTAL)
theta_slider.set(.015*2*100)
theta_slider.pack()

running = True
clock = pygame.time.Clock()
time = 0

freq_label = tk.Label(text='Icosahedron frequency')
freq_label.pack()
freq_slider = tk.Scale(from_=1, to=10_000, orient=tk.HORIZONTAL)
freq_slider.set(4000)
freq_slider.pack()

while running:
    delta = clock.tick(0)
    time += delta

    speed = speed_slider.get() / 100
    theta = theta_slider.get() / 100
    freq = freq_slider.get()

    screen.fill((0, 0, 0))

    scene.render(camera)

    screen.blit(font.render(f'FPS: {round(clock.get_fps())}', True, (255, 255, 255)), (10, 10))

    position = font.render(f'({round(camera.x)}, {round(camera.y)}, {round(camera.z)})', True, (255, 255, 255))
    screen.blit(position, (screen_size[0] - position.get_width() - 10, 10))

    angle = font.render(f'θx={round(camera.theta_x, 2)}; θy={round(camera.theta_y, 2)}', True, (255, 255, 255))
    screen.blit(angle, (screen_size[0] - angle.get_width() - 10, 40))

    pygame.display.flip()
    interface.update()

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

    scene.models[-1].transform(lambda vertex: V(
            vertex.z*sin(theta) + vertex.x*cos(theta),
            vertex.y,
            vertex.z*cos(theta) - vertex.x*sin(theta)
        ))
    new_icosahedron = deepcopy(base_icosahedron)
    new_icosahedron.transform(lambda v: V(
        ((v.x + 13)/3 * abs(cos(2*time/freq)))*3 - 13,
        ((v.y - 5)/3 * abs(cos(2*time/freq)))*3 + 5,
        ((v.z - 8)/3 * abs(cos(2*time/freq)))*3 + 8
    ))
    scene.models[2] = new_icosahedron
