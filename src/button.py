import pygame, setting
from constant import *


class Button:
    def __init__(
        self,
        image,
        hovering_image,
        pos,
        text_input,
        font,
        base_color,
        hovering_color,
        scale=(1.0, 1.0),
    ):
        self.base_image = image
        self.base_size = self.base_image.get_size()  # 원래 이미지의 크기
        self.image = self.base_image
        self.hovering_image = hovering_image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.scale = scale  # 추가 조정을 위한 실수 배율
        if self.image is None:
            self.image = self.text
        if self.hovering_image is None:
            self.hovering_image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.resize(setting.get_screen_size())

    def resize(self, size):
        self.base_image = pygame.transform.scale(
            self.base_image,
            (
                size[0] * self.base_size[0] * self.scale[0] / 1920,
                size[1] * self.base_size[1] * self.scale[1] / 1080,
            ),
        )
        self.hovering_image = pygame.transform.scale(
            self.hovering_image,
            (
                size[0] * self.base_size[0] * self.scale[0] / 1920,
                size[1] * self.base_size[1] * self.scale[1] / 1080,
            ),
        )

        self.font = setting.get_font(50 * self.scale[0])
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, state, screen):
        if state:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def changeHighlight(self, state, screen):
        if state:
            self.image = self.hovering_image
            self.changeColor(state, screen)
        else:
            self.image = self.base_image
            self.changeColor(state, screen)

    def changeHighlight1(self, state, screen):
        if state:
            screen.blit(self.image, self.rect)
            screen.blit(self.hovering_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def ChangeImage(self, change_image):
        self.image = change_image
        self.hovering_image = change_image

    def ChangeText(
        self, change_text, change_base_color=None, change_hovering_color=None
    ):
        self.text_input = change_text
        if change_hovering_color is not None:
            self.base_color, self.hovering_color = (
                change_base_color,
                change_hovering_color,
            )
        self.text = self.font.render(self.text_input, True, self.base_color)
