import pygame

BUTTON_A = 0
BUTTON_B = 1
BUTTON_C = 2


class Input:
    def __init__(self):
        self.current_button = None

    def get_inputs(self, event):
        # Make sure focus is on the Display window NOT the console!!
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("You pressed the A button")
                self.current_button = BUTTON_A
            if event.key == pygame.K_b:
                print("You pressed the B button")
                self.current_button = BUTTON_B
            if event.key == pygame.K_c:
                print("You pressed the C button")
                self.current_button = BUTTON_C
        else:
            self.current_button = None

        return self.current_button