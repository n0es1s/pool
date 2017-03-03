import pygame
import math

class Canvas:
    def __init__(self, vertical_size, horizontal_size, background_color, *args, **kwargs):
        self.surface = pygame.display.set_mode((vertical_size, horizontal_size), *args, **kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

        self.background = pygame.Surface(self.surface.get_size())
        self.background = self.background.convert()
        self.background.fill(background_color)

        self.surface.blit(self.background, (0, 0))


    def draw_main_menu(self,table_color):
        text_color = (255, 255, 255)
        text_selected_color = (0, 0, 255)
        font_name = pygame.font.get_default_font()
        title_font = pygame.font.Font(font_name, 40)
        options_font = pygame.font.Font(font_name, 20)

        title_text = "Pool"
        menu_buttons = ["Play Pool", "Fully random", "Exit"]
        # generating options buttons
        buttons = [
            # text when mouse is outside the button range
            [options_font.render(label, False, text_color),
             # text when mouse is inside the button range
             options_font.render(label, False, text_selected_color)]
            for label in menu_buttons]
        # calculating button sizes
        button_size = [options_font.size(label) for label in menu_buttons]

        # generating the title
        title = [title_font.render(title_text, False, text_color),
                 title_font.render(title_text, False, text_color)]
        buttons.insert(0, title)
        button_size.insert(0, title_font.size(title_text))

        screen_mid = self.size_x / 2
        margin = 20
        spacing = 10

        screen_y = (self.size_y - margin * 2) / (len(buttons))

        # generating text coordinates
        text_starting_place = [(screen_mid - (button_size[num][0] / 2),
                                num * screen_y + (button_size[num][1] / 2)) for num in range(len(buttons))]
        text_ending_place = [(text_starting_place[num][0] + button_size[num][0],
                              text_starting_place[num][1] + button_size[num][1]) for num in range(len(buttons))]

        # writing text and drawing a rectangle around it
        for num in range(len(buttons)):
            self.surface.blit(buttons[num][0], text_starting_place[num])
            # no rectangle on the title
            if num > 0:
                pygame.draw.rect(self.surface, text_color,
                                 (text_starting_place[num][0] - spacing, text_starting_place[num][1] - spacing,
                                  button_size[num][0] + spacing * 2, button_size[num][1] + spacing * 2), 1)

        return text_starting_place, text_ending_place, spacing, buttons
