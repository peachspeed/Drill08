# state_machine.py

class StateMachine:
    def __init__(self, character):
        self.character = character
        self.state = None
        self.transitions = {}

    def start(self, initial_state):
        self.state = initial_state
        self.state.enter(self.character, None)

    def draw(self):
        if self.state and hasattr(self.state, 'draw'):
            self.state.draw(self.character)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def change_state(self, new_state):
        if self.state:
            self.state.exit(self.character, None)
        self.state = new_state
        self.state.enter(self.character, None)

    def update(self):
        if self.state:
            self.state.do(self.character)

    def handle_event(self, event):
        event_type = event.type
        key = event.key if hasattr(event, 'key') else None

        new_state = None

        if self.state in self.transitions:
            if event_type == SDL_KEYDOWN:
                if key == SDLK_RIGHT:
                    new_state = self.transitions[self.state].get('right_down')
                elif key == SDLK_LEFT:
                    new_state = self.transitions[self.state].get('left_down')
                elif key == SDLK_a:
                    new_state = self.transitions[self.state].get('space_down')
            elif event_type == SDL_KEYUP:
                if key == SDLK_RIGHT:
                    new_state = self.transitions[self.state].get('right_up')
                elif key == SDLK_LEFT:
                    new_state = self.transitions[self.state].get('left_up')

        if new_state is not None:
            self.change_state(new_state)
