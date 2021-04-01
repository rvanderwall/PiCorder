import pygame

BUTTON_A = 0
BUTTON_B = 1
BUTTON_C = 2


class Input:
    def __init__(self):
        self.current_button = None

    def get_inputs(self, event):
        keys = []
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("You pressed the A button")
                keys.append(BUTTON_A)
                self.current_button = BUTTON_A
            if event.key == pygame.K_b:
                print("You pressed the B button")
                keys.append(BUTTON_B)
                self.current_button = BUTTON_B
            if event.key == pygame.K_c:
                print("You pressed the C button")
                keys.append(BUTTON_C)
            self.current_button = BUTTON_C
        return keys
