import sys
from typing import List, Optional

import pygame
import pygame as pg

import src.consts
from src.modules.banners.upheaval_font import UpheavalFont
from src.utils.funcs import load_image, select_from_db

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, img: pg.Surface, x: int, y: int, rx: int, ry: int, *group: pygame.sprite.Group):
        super().__init__(*group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (rx, ry))

    def update(self, y):
        self.rect.y = y


def terminate():
    pygame.quit()
    sys.exit()


def streak(lst):
    if not lst:
        return 0
    a = lst[-1]
    st = ""
    for i in range(1, len(lst) + 1):
        if lst[-i] == a:
            st += lst[-i]
        else:
            break
    if "l" in st:
        return f"-{len(st)}"
    return f"{len(st)}"


class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fon = pygame.transform.scale(load_image("images/menu/fon.png"), (WIDTH, HEIGHT))

        self.head_sprites = pygame.sprite.Group()
        self.anim_sprites1 = pygame.sprite.Group()
        self.anim_sprites2 = pygame.sprite.Group()

        # Параметры анимации
        self.dx = 90  # горизонтальное смещение
        self.vy = 0.5  # скорость изменения dx
        self.i = 0.0  # счетчик для переключения анимации
        self.di = 0.25  # инкремент для i
        self.current_anim_group = self.anim_sprites1  # текущая группа для отрисовки

        self._init_sprites()

    def _init_sprites(self):
        """Инициализация всех спрайтов меню"""

        MenuSprite(
            load_image("images/menu/head.png", -1),
            100, 100, 1100, 200,
            self.head_sprites,
        )
        MenuSprite(
            load_image("images/menu/isaac1.png", -1),
            365, 300, 500, 500,
            self.anim_sprites1,
        )
        MenuSprite(
            load_image("images/menu/isaac2.png", -1),
            365, 300, 500, 500,
            self.anim_sprites2,
        )

    def _handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key != pygame.K_ESCAPE:
                    from src.modules.main_menu.character_selection import CharacterSelectionMenu
                    return CharacterSelectionMenu(self.screen).run()
                else:
                    terminate()
        return None

    def _update_animation_state(self):
        """Обновление состояния анимации"""
        self.dx += self.vy
        if self.dx >= 120:
            self.vy = -0.5
        elif self.dx <= 90:
            self.vy = 0.5

        self.i += self.di
        if self.i >= 6:
            self.i = 0

        if 0 <= self.i < 2 or 4 <= self.i < 6:
            self.current_anim_group = self.anim_sprites1
        else:
            self.current_anim_group = self.anim_sprites2

    def _draw(self):
        """Отрисовка всех элементов"""
        self.screen.blit(self.fon, (0, 0))

        self.head_sprites.draw(self.screen)
        self.head_sprites.update(self.dx)
        self.current_anim_group.draw(self.screen)

    def run(self):
        """Основной цикл стартового экрана"""
        while True:
            result = self._handle_events()
            if result is not None:
                if isinstance(result, type):
                    new_screen_instance = result(self.screen)
                    if hasattr(new_screen_instance, 'run'):
                        selection_result = new_screen_instance.run()
                        if selection_result == "BACK_TO_MAIN":
                            continue
                        else:
                            return selection_result
                elif result == "BACK_TO_MAIN":
                    continue
                elif result in ["isaac", "cain", "lost"]:
                    return result

            self._update_animation_state()

            self._draw()

            pygame.display.flip()
            self.clock.tick(40)
