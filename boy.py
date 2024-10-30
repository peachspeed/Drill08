from pico2d import *
from state_machine import StateMachine

IDLE_TIME = 5.0  # 자동 무적 런이 5초 이상 지속되면 Idle로 전환

class Idle:
    def enter(boy, event):
        boy.dir = 0
        boy.speed = 100
        boy.scale = 1.0

    def exit(boy, event):
        pass

    def do(boy):
        pass

    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)

class Run:
    def enter(boy, event):
        boy.speed = 200

    def exit(boy, event):
        pass

    def do(boy):
        boy.x += boy.dir * boy.speed * 0.01

    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, 100 if boy.dir == 1 else 0, 100, 100, boy.x, boy.y)

class AutoRun:
    def enter(boy, event):
        boy.dir = 1
        boy.speed = 300
        boy.scale = 1.5
        boy.start_time = get_time()

    def exit(boy, event):
        boy.speed = 100
        boy.scale = 1.0

    def do(boy):
        boy.x += boy.dir * boy.speed * 0.01

        if boy.x < 0 or boy.x > 800:
            boy.dir *= -1

        if get_time() - boy.start_time > IDLE_TIME:
            boy.state_machine.change_state(Idle)

    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, boy.y, 100 * boy.scale, 100 * boy.scale)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

        # 상태 전환 설정
        self.state_machine.set_transitions({
            Idle: {'space_down': AutoRun, 'right_down': Run, 'left_down': Run},
            Run: {'right_up': Idle, 'left_up': Idle},
            AutoRun: {'right_down': Run, 'left_down': Run},
        })

    def update(self):
        self.state_machine.update()
        self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        self.state_machine.handle_event(event)

    def draw(self):
        self.state_machine.draw()

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)
