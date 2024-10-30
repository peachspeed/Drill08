from pico2d import *

# 상태 정의
class Idle:
    def enter(boy):
        boy.dir = 0
        boy.scale = 1.0  # 크기를 원래대로 돌립니다.

    def do(boy):
        pass

class Run:
    def enter(boy):
        boy.scale = 1.0  # Run 상태에서도 크기를 원래대로 유지합니다.

    def do(boy):
        boy.x += boy.dir * 5

class AutoRun:
    def enter(boy):
        boy.dir = 1
        boy.start_time = get_time()

    def do(boy):
        boy.x += boy.dir * 7

        # 캐릭터가 자동으로 점점 커집니다.
        if boy.scale < 2.5:  # 최대 크기를 제한합니다.
            boy.scale += 0.01

        # 화면의 끝에 도달하면 방향 전환
        if boy.x > 800 or boy.x < 0:
            boy.dir *= -1

        # 5초가 지나면 Idle 상태로 돌아갑니다.
        if get_time() - boy.start_time > 5.0:
            boy.change_state(Idle)

# 캐릭터 클래스 정의
class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.state = Idle  # 초기 상태는 Idle
        self.state.enter(self)
        self.dir = 0  # 방향 초기화
        self.scale = 1.0  # 크기 초기화

    def change_state(self, state):
        self.state = state
        self.state.enter(self)

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.state.do(self)

    def draw(self):
        # 캐릭터를 크기에 맞게 그립니다.
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y, 100 * self.scale, 100 * self.scale)

# Grass 클래스 정의
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

# 메인 루프
open_canvas()

grass = Grass()
boy = Boy()
running = True

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                boy.dir = 1
                boy.change_state(Run)
            elif event.key == SDLK_LEFT:
                boy.dir = -1
                boy.change_state(Run)
            elif event.key == SDLK_a:
                boy.change_state(AutoRun)
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT):
                boy.change_state(Idle)

while running:
    handle_events()
    boy.update()
    clear_canvas()
    grass.draw()  # Grass를 먼저 그려줍니다.
    boy.draw()    # 그 위에 Boy를 그립니다.
    update_canvas()
    delay(0.01)

close_canvas()
