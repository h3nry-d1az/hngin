# https://math.stackexchange.com/questions/2305792/3d-projection-on-a-2d-plane-weak-maths-ressources
# https://en.wikipedia.org/wiki/Projection_(linear_algebra)
# https://en.wikipedia.org/wiki/3D_projection
# https://en.wikipedia.org/wiki/Painter%27s_algorithm
# http://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm
# https://cs418.cs.illinois.edu/website/text/obj.html
# https://free3d.com/3d-model/low-poly-male-26691.html
# https://free3d.com/3d-model/low_poly_tree-816203.html
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Callable
from copy import deepcopy
from math import sin, cos, pi
import pygame
import tkinter as tk
from tkinter import ttk

def cartesian_to_pygame(
    x: float,
    y: float
) -> Tuple[float, float]:
    return (x + screen_size[0]//2,
            screen_size[1]//2 - y)

def hex_to_rgb(hex_value: str) -> Tuple[int, int, int]:
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex_value[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)


"""Tkinter interface for scene model settings
"""
models_interface = tk.Tk()
models_interface.title('model settings')
models_interface.iconphoto(False, tk.PhotoImage(file='assets/hngin-favicon.png'))
models_interface.geometry('124x256+154+175')
models_interface.resizable(False, False)

models_title_label = tk.Label(models_interface, text='ʜɴɢɪɴ Model Settings', font=('Times New Roman', 10, 'bold'))
models_title_label.pack()

ttk.Separator(models_interface, orient='horizontal').pack(fill='x')

vertex_size_label = tk.Label(models_interface, text='Vertex size')
vertex_size_label.pack()
vertex_size_slider = tk.Scale(models_interface, from_=0, to=10, orient=tk.HORIZONTAL)
vertex_size_slider.set(0)
vertex_size_slider.pack()

ttk.Separator(models_interface, orient='horizontal').pack(fill='x')

model_label = tk.Label(models_interface, text='Rotating model')
model_label.pack()
model_entry = tk.Entry(models_interface)
model_entry.insert(0, 'models/tree.obj')
model_entry.pack()

model_scale_label = tk.Label(models_interface, text='Rotating model scale')
model_scale_label.pack()
model_scale_slider = tk.Scale(models_interface, from_=0, to=200, orient=tk.HORIZONTAL)
model_scale_slider.set(75)
model_scale_slider.pack()

ttk.Separator(models_interface, orient='horizontal').pack(fill='x')

model_speed_label = tk.Label(models_interface, text='Model rotation speed')
model_speed_label.pack()
model_speed_slider = tk.Scale(models_interface, from_=0, to=.001*10000, orient=tk.HORIZONTAL)
model_speed_slider.set(.0003*10000)
model_speed_slider.pack()


"""Tkinter interface for engine settings
"""
engine_interface = tk.Toplevel(models_interface)
engine_interface.title('engine settings')
engine_interface.iconphoto(False, tk.PhotoImage(file='assets/hngin-favicon.png'))
engine_interface.geometry('142x350+1050+175')
engine_interface.resizable(False, False)

engine_title_label = tk.Label(engine_interface, text='ʜɴɢɪɴ Engine Settings', font=('Times New Roman', 10, 'bold'))
engine_title_label.pack()

ttk.Separator(engine_interface, orient='horizontal').pack(fill='x')

FPS_label = tk.Label(engine_interface, text='Maximum FPS')
FPS_label.pack()
FPS_slider = tk.Scale(engine_interface, from_=0, to=60, orient=tk.HORIZONTAL)
FPS_slider.set(30)
FPS_slider.pack()

ttk.Separator(engine_interface, orient='horizontal').pack(fill='x')

focal_length_label = tk.Label(engine_interface, text='Focal length')
focal_length_label.pack()
focal_length_slider = tk.Scale(engine_interface, from_=0, to=2000, orient=tk.HORIZONTAL)
focal_length_slider.set(1000)
focal_length_slider.pack()

ttk.Separator(engine_interface, orient='horizontal').pack(fill='x')

def toggle_face_properties():
    if not hollow_faces.get():
        vertex_size_slider.set(0)
    else:
        vertex_size_slider.set(1)

hollow_faces = tk.BooleanVar()
hollow_checkbox = tk.Checkbutton(
    engine_interface,
    text='Hollow faces',
    variable=hollow_faces,
    onvalue=True,
    offvalue=False,
    command=toggle_face_properties,
)
hollow_checkbox.pack()

ttk.Separator(engine_interface, orient='horizontal').pack(fill='x')

background_color_label = tk.Label(engine_interface, text='Background color')
background_color_label.pack()
background_color_entry = tk.Entry(engine_interface)
background_color_entry.insert(0, '0A0A0A')
background_color_entry.pack()

ttk.Separator(engine_interface, orient='horizontal').pack(fill='x')

speed_label = tk.Label(engine_interface, text='Camera movement speed')
speed_label.pack()
speed_slider = tk.Scale(engine_interface, from_=0, to=.5*100, orient=tk.HORIZONTAL)
speed_slider.set(.05*100)
speed_slider.pack()

ttk.Separator(engine_interface, orient='horizontal').pack(fill='x')

theta_label = tk.Label(engine_interface, text='Camera rotation speed')
theta_label.pack()
theta_slider = tk.Scale(engine_interface, from_=0, to=.002*10000, orient=tk.HORIZONTAL)
theta_slider.set(.0007*10000)
theta_slider.pack()

@dataclass
class Camera(object):
    x: float
    y: float
    z: float
    theta_x: float = 0.
    theta_y: float = 0.
    theta_z: float = 0.
    vertical_angle: float = 0
    angle_ratios: Dict[str, float] = field(default_factory=dict)

    def compute_angle_ratios(self) -> None:
        self.angle_ratios = {
            "sin_tx": sin(self.theta_y),
            "sin_ty": sin(self.theta_x),
            "sin_tz": sin(self.theta_z),
            "cos_tx": cos(self.theta_y),
            "cos_ty": cos(self.theta_x),
            "cos_tz": cos(self.theta_z)
        }

# screen_size = (1280, 720)
screen_size = (640, 480)
camera = Camera(0, 8, -50)

pygame.init()
pygame.display.set_caption('hngin -- v0.0.1')
pygame.display.set_icon(pygame.image.load('assets/hngin-favicon.png'))

font = pygame.font.SysFont('Helvetica', 28)

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

    def project(self,
                camera: Camera) -> Tuple[float, float] | None:
        x = (self.x - camera.x)
        y = (self.y - camera.y)
        z = (self.z - camera.z)
        stx = camera.angle_ratios["sin_tx"]
        sty = camera.angle_ratios["sin_ty"]
        stz = camera.angle_ratios["sin_tz"]
        ctx = camera.angle_ratios["cos_tx"]
        cty = camera.angle_ratios["cos_ty"]
        ctz = camera.angle_ratios["cos_tz"]

        rotated = V(
            z*sty*ctx + y*(stx*sty*ctz - stz*cty) + x*(stx*sty*stz + cty*ctz),
            -z*stx + x*stz*ctx + y*ctx*ctz,
            x*(stx*stz*cty - sty*ctz) + y*(stx*cty*ctz + sty*stz) + z*ctx*cty
        )
        if rotated.z < 0:
            return None
        return cartesian_to_pygame((rotated.x * focal_length_slider.get()) // rotated.z,
                                   (rotated.y * focal_length_slider.get()) // rotated.z)

    def render(self,
               camera: Camera) -> None:
        if not (projected := self.project(camera)):
            return
        pygame.draw.circle(screen,
                           (255, 255, 255),
                           projected,
                           vertex_size_slider.get())

@dataclass
class F(object):
    vertex_1: V
    vertex_2: V
    vertex_3: V

    def render(
        self,
        camera: Camera,
        color: Tuple[int, int, int]
    ) -> None:
        if not (p1 := self.vertex_1.project(camera))\
        or not (p2 := self.vertex_2.project(camera))\
        or not (p3 := self.vertex_3.project(camera)):
            return
        pygame.draw.polygon(screen, color, [p1, p2, p3],
            1 if hollow_faces.get() else 0)

@dataclass
class Model(object):
    vertices: List[V]
    faces: List[F] | None
    color: Tuple[int, int, int]

    def render(self,
               camera: Camera) -> None:
        if self.faces:
            for face in self.faces:
                face.render(camera, self.color)

        if vertex_size_slider.get() != 0:
            for vertex in self.vertices:
                vertex.render(camera)

    def transform(self, f: Callable[[V], V]) -> None:
        self.vertices = list(map(f, self.vertices))
        if self.faces:
            self.faces = list(map(lambda fc: F(f(fc.vertex_1), f(fc.vertex_2), f(fc.vertex_3)), self.faces))

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
        faces = []
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
                for i in range(1, len(normalized)+1):
                    try:
                        faces.append(F(vertices[normalized[0]-1],
                                       vertices[normalized[i]-1],
                                       vertices[normalized[i+1]-1]))
                    except IndexError:
                        break
        return Model(vertices, faces, color)

model_original = parse_obj_model('models/tree.obj', (0, 255, 0))
model = deepcopy(model_original)
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

running = True
clock = pygame.time.Clock()
time = 0

model_value = 'models/tree.obj'
scale_value = 75.
freq = 4000

last_background_color = (0, 0, 0)

while running:
    delta = clock.tick(FPS_slider.get())
    time += delta

    speed = speed_slider.get() / 100
    theta = theta_slider.get() / 10000
    mtheta = model_speed_slider.get() / 10000

    try:
        entry = background_color_entry.get()
        screen.fill(hex_to_rgb(entry))
        last_background_color = hex_to_rgb(entry)
    except Exception:
        screen.fill(last_background_color)

    camera.compute_angle_ratios()
    scene.render(camera)

    screen.blit(font.render(f'FPS: {round(clock.get_fps())}', True, (255, 255, 255)), (10, 10))

    position = font.render(f'({round(camera.x)}, {round(camera.y)}, {round(camera.z)})', True, (255, 255, 255))
    screen.blit(position, (screen_size[0] - position.get_width() - 10, 10))

    angle_x = font.render(f'θx={round(camera.theta_y, 2)}', True, (255, 255, 255))
    screen.blit(angle_x, (screen_size[0] - angle_x.get_width() - 10, 40))

    angle_y = font.render(f'θy={round(camera.theta_x, 2)}', True, (255, 255, 255))
    screen.blit(angle_y, (screen_size[0] - angle_y.get_width() - 10, 70))

    angle_z = font.render(f'θz={round(camera.theta_z, 2)}', True, (255, 255, 255))
    screen.blit(angle_z, (screen_size[0] - angle_z.get_width() - 10, 100))

    pygame.display.flip()
    models_interface.update()
    engine_interface.update()

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
    if keys[pygame.K_a]:
        camera.theta_x = min(camera.theta_x + theta*delta, pi)
    if keys[pygame.K_d]:
        camera.theta_x = max(camera.theta_x - theta*delta, -pi)
    if keys[pygame.K_w]:
        camera.vertical_angle = min(camera.vertical_angle + theta*delta, pi)
    if keys[pygame.K_s]:
        camera.vertical_angle = max(camera.vertical_angle - theta*delta, -pi)
    if keys[pygame.K_SPACE]:
        camera.y += speed*delta
    if (keys[pygame.K_LSHIFT]) or \
       (keys[pygame.K_RSHIFT]):
        camera.y -= speed*delta

    camera.theta_y = camera.vertical_angle*cos(camera.theta_x)
    camera.theta_z = camera.vertical_angle*sin(camera.theta_x)

    if (ms := model_scale_slider.get()) != scale_value:
        new_model = deepcopy(model_original)
        new_model.transform(lambda v: V(
            v.x*ms/100,
            v.y*ms/100,
            v.z*ms/100
        ))
        scene.models[-1] = new_model
        scale_value = ms

    if (mt := model_entry.get()) != model_value:
        try:
            model_original = parse_obj_model(mt, (0, 255, 0))
            new_model = deepcopy(model_original)
            new_model.transform(lambda v: V(
                v.x*ms/100,
                v.y*ms/100,
                v.z*ms/100
            ))
            scene.models[-1] = new_model
            model_value = mt
        except Exception:
            model_value = mt

    scene.models[-1].transform(lambda vertex: V(
            vertex.z*sin(mtheta*delta) + vertex.x*cos(mtheta*delta),
            vertex.y,
            vertex.z*cos(mtheta*delta) - vertex.x*sin(mtheta*delta)
        ))
    new_icosahedron = deepcopy(base_icosahedron)
    new_icosahedron.transform(lambda v: V(
        ((v.x + 13)/3 * abs(cos(2*time/freq)))*3 - 13,
        ((v.y - 5)/3 * abs(cos(2*time/freq)))*3 + 5,
        ((v.z - 8)/3 * abs(cos(2*time/freq)))*3 + 8
    ))
    scene.models[2] = new_icosahedron
