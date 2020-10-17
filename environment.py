import pygame as pg
import pymunk.pygame_util
import random
import drower
from pymunk import Vec2d

pymunk.pygame_util.positive_y_is_up = False
pg.font.init()
font = pg.font.Font(None, 100)


RES = WIDTH, HEIGHT = 800, 800
FPS = 60
_FPS = 1 / FPS

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 1500
blood_v = 0
bit_rate = 60

collision_types = {
    "blood_cells": 1,
    "cleaner": 2
}

drower.collision_types = collision_types
drower.space = space
drower.draw_heart()
blood_v = 0


def get_bit_rate(t):
    return 1 / (sum(t) / len(t))


def generate_input():
    r = random.randint(55, 95)
    return [1 / r for i in range(1, r + 1)]


class Kostyl():
    def __init__(self):
        s1 = pymunk.Segment(space.static_body, (186, 547), (277, 652), 0.3)
        s2 = pymunk.Segment(space.static_body, (277, 652), (372, 710), 0.3)
        s3 = pymunk.Segment(space.static_body, (372, 710), (458, 740), 0.3)
        s3 = pymunk.Segment(space.static_body, (458, 740), (532, 746), 0.3)
        s4 = pymunk.Segment(space.static_body, (532, 746), (594, 685), 0.3)
        s5 = pymunk.Segment(space.static_body, (594, 685), (629, 576), 0.3)
        s6 = pymunk.Segment(space.static_body, (629, 576), (648, 518), 0.3)
        s7 = pymunk.Segment(space.static_body, (648, 518), (650, 368), 0.3)
        self.all_shapes = [s1, s2, s3, s4, s5, s6, s7]
        for i in range(len(self.all_shapes)):
            self.all_shapes[i].collision_type = collision_types["cleaner"]
            self.all_shapes[i].color = pg.color.THECOLORS["black"]
    
    def on(self):
        space.add(*self.all_shapes)
    
    def off(self):
        space.remove(*self.all_shapes)
kostyl = Kostyl()


class Blood_cell():
    
    def __init__(self, pos, impulse, color, moment=6.2, mass=0.5, radius=8):
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.body.apply_impulse_at_local_point(Vec2d(impulse))
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.color = pg.color.THECOLORS[color]
        self.shape.collision_type = collision_types["blood_cells"]
        self.shape.elasticity = 0
        
    def spawn(self):
        space.add(self.body, self.shape)
        
    def destroy(self):
        space.remove(self.shape)


def spawn_blood_cell(pos, impulse, color):
    global blood_v
    for _ in range(2):
        new_cell = Blood_cell(pos, impulse, color)
        new_cell.spawn()
        blood_v += 1


def remove_blood_cell(arbiter, space, data):
    global blood_v
    cell_shape = arbiter.shapes[0] 
    space.remove(cell_shape, cell_shape.body)
    blood_v -= 1
    return True
    
    
class Muscle():
    def __init__(self, from_, to_, vel):
        self.vel = vel
        self.from_ = from_
        self.to_ = to_
        
    def draw(self):
        self.body = pymunk.Body(500, pymunk.inf, pymunk.Body.KINEMATIC)
        self.body.position = ((self.from_[0] + self.from_[1]) / 350, (self.to_[0] + self.to_[1]) / 350)
        
        self.shape = pymunk.Segment(self.body, self.from_, self.to_, 4)
        self.shape.color = pg.color.THECOLORS["brown"]
        self.shape.elasticity = 0.8
        space.add(self.body, self.shape)
        self.is_use = False
        
    def up(self):
        self.body.velocity = (-self.vel[0], -self.vel[1])
        
    def down(self):
        self.body.velocity = self.vel
        
    def not_active(self):
        self.body.velocity = (0, 0)


class Border():
    def __init__(self, from_, to_):
        self.segment_shape = pymunk.Segment(space.static_body, from_, to_, 3)
        self.segment_shape.color = pg.color.THECOLORS["darkslategray"]
        
    def spawn(self):
        space.add(self.segment_shape)
        
    def destroy(self):
        space.remove(self.segment_shape)
            


class Heart():
    def __init__(self, borders, muscles, kostyls):
        self.kostyls = kostyls
        self.borders = borders
        self.muscles = muscles
        self.t = 0
        self.is_use = False

        self.timing = generate_input()
        self.timer = 0
    
    def use(self):
        self.timing.append(self.timer)
        self.timing = self.timing[1:]
        self.timer = 0
        self.is_use = True
        try:
            for border in self.borders:
                border.spawn()
        except:
            pass
    
    def update(self):
        if self.is_use:
            if self.t > 20:
                for border in self.borders:
                    border.destroy()
                self.t = 0
                self.is_use = False
                self.kostyls.off()
            elif self.t <= 20 and self.is_use:
                if self.t == 1:
                    self.kostyls.on()
                if self.t <= 10:
                    for muscle in muscles:
                        muscle.up()
                else:
                    for muscle in muscles:
                        muscle.down()
                self.t += 1
        else:
            for muscle in muscles:
                muscle.not_active()

        self.timer += _FPS


h = space.add_collision_handler(
    collision_types["blood_cells"], 
    collision_types["cleaner"])
h.begin = remove_blood_cell
    
bord1 = Border((650, 330), (518, 352))
bord2 = Border((297, 379), (186, 488))
borders = [bord1, bord2]

m1 = Muscle((178, 549), (272, 651), (-700, 800))
m2 = Muscle((272, 651), (391, 722), (0, 1100))
m3 = Muscle((391, 722), (462, 750), (0, 1200))
m4 = Muscle((462, 750), (546, 755), (0, 1200))
m5 = Muscle((543, 750), (519, 726), (0, 1200))
m6 = Muscle((519, 726), (475, 644), (0, 1200))
m7 = Muscle((475, 644), (431, 524), (0, 1200))
m8 = Muscle((431, 524), (412, 406), (0, 1200))
m9 = Muscle((546, 755), (609, 684), (0, 1200))
m10 = Muscle((609, 684), (638, 576), (700, 800))
m11 = Muscle((638, 576), (659, 527), (700, 800))
m12 = Muscle((657, 516), (661, 381), (500, 100))
muscles = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]

cleaner1 = drower.create_cleaner((303, 376), (413, 382))
cleaner2 = drower.create_cleaner((514, 354), (421, 404))



heart = Heart(borders, muscles, kostyl)
frames_timer = 0


def reset():
    global blood_v, frames_timer, heart
    
    space.remove(space.shapes)
    drower.draw_heart()
    for m in muscles:
        m.draw()
    heart = Heart(borders, muscles, kostyl)
    cleaner1 = drower.create_cleaner((303, 376), (413, 382))
    cleaner2 = drower.create_cleaner((514, 354), (421, 404))

    blood_v = 0


def step(action):
    global blood_v, bit_rate
    
    spawn_blood_cell((215, 271), (0, 0), "blue")
    spawn_blood_cell((582, 187), (0, 0), "red")
    if action == 1 and not heart.is_use:
        heart.use()
    heart.update()

    bit_rate = get_bit_rate(heart.timing)
    print(heart.timing)
    print(bit_rate)
    if (blood_v < 950) and (55 < bit_rate < 140):
        done = False
    else:
        done = True
    space.step(_FPS)
    clock.tick(FPS)
    
    return [bit_rate, blood_v], done, heart.is_use


def render():
    surface.fill(pg.Color("black"))
    text = font.render(str(int(bit_rate)), 5, (255, 180, 180))
    surface.blit(text, (650, 710))
    space.debug_draw(draw_options)
    pg.display.flip()