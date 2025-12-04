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
                    return "choice_menu"
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
            if result == "choice_menu":
                return choise_menu(self.screen)

            self._update_animation_state()

            self._draw()

            pygame.display.flip()
            self.clock.tick(40)


# Магические константы
HERO_POSITIONS = [
    (610, 450),
    (510, 360),
    (710, 360),
]
HERO_SIZE = (80, 90)

HERO_NAMES = ["isaac", "cain", "lost"]
MENU_ITEM_NAMES = ["new", "continue", "options"]


def create_hero_sprites(image_paths: List[str], group: pygame.sprite.Group) -> None:
    if len(image_paths) != len(HERO_POSITIONS):
        raise ValueError(f"Ожидается {len(HERO_POSITIONS)} изображений, получено {len(image_paths)}")

    for img_path, (x, y) in zip(image_paths, HERO_POSITIONS):
        MenuSprite(
            load_image(img_path, -1),
            x, y,
            HERO_SIZE[0], HERO_SIZE[1],
            group
        )


def draw_name(i: int):
    if i % 3 == 0:
        return "isaac.draw(screen)"
    if i % 3 == 1:
        return "cain.draw(screen)"
    if i % 3 == 2:
        return "lost.draw(screen)"


def draw_menu(i: int):
    if i % 3 == 0:
        return "new.draw(screen)"
    if i % 3 == 1:
        return "con.draw(screen)"
    if i % 3 == 2:
        return "opt.draw(screen)"


def get_hero_name(hero_index: int) -> str:
    """Возвращает имя героя по индексу."""
    return HERO_NAMES[hero_index % len(HERO_NAMES)]


# Условная сложность
def check_selection(menu_index: int, hero_index: int) -> Optional[str]:
    if menu_index % len(MENU_ITEM_NAMES) == 0:
        return get_hero_name(hero_index)

    return None


def wr(lst):
    if not lst:
        return 0
    win = lst.count("w")
    return int(win / len(lst) * 100)


# Возвращает имя персонажа (допилить возврат управления)
def choise_menu(screen):
    start_screen = StartScreen(screen)
    fon = pygame.transform.scale(
        load_image("images/menu/choise_fon.png"),
        (WIDTH, HEIGHT),
    )
    whoam = pygame.sprite.Group()
    list_hero = [
        "images/menu/isaac.png",
        "images/menu/cain.png",
        "images/menu/lost.png",
    ]
    MenuSprite(load_image("images/menu/whoam.png", -1), 350, 100, 600, 740, whoam)
    MenuSprite(load_image("images/menu/left.png", -1), 510, 560, 50, 50, whoam)
    MenuSprite(load_image("images/menu/right.png", -1), 710, 560, 50, 50, whoam)
    MenuSprite(load_image("images/menu/sheet.png", -1), 880, 200, 700, 600, whoam)

    MenuSprite(load_image("images/menu/new_run.png", -1), 945, 300, 280, 90, whoam)
    MenuSprite(
        load_image("images/menu/continue_true.png", -1),
        950,
        370,
        280,
        90,
        whoam,
    )
    MenuSprite(load_image("images/menu/options.png", -1), 955, 435, 280, 90, whoam)

    MenuSprite(
        load_image("images/menu/right.png", -1),
        905,
        335,
        50,
        50,
        new := pygame.sprite.Group(),
    )
    MenuSprite(
        load_image("images/menu/right.png", -1),
        910,
        405,
        50,
        50,
        con := pygame.sprite.Group(),
    )
    MenuSprite(
        load_image("images/menu/right.png", -1),
        910,
        475,
        50,
        50,
        opt := pygame.sprite.Group(),
    )

    MenuSprite(
        load_image("images/menu/isaac_name.png", -1),
        570,
        550,
        150,
        70,
        isaac := pygame.sprite.Group(),
    )
    MenuSprite(
        load_image("images/menu/cain_name.png", -1),
        570,
        550,
        150,
        70,
        cain := pygame.sprite.Group(),
    )
    MenuSprite(
        load_image("images/menu/lost_name.png", -1),
        560,
        540,
        160,
        90,
        lost := pygame.sprite.Group(),
    )
    MenuSprite(load_image("images/menu/isaac_info.png", -1), 480, 630, 350, 70, isaac)
    MenuSprite(load_image("images/menu/lost_info.png", -1), 480, 630, 350, 70, lost)
    MenuSprite(load_image("images/menu/cain_info.png", -1), 480, 630, 350, 70, cain)

    screen.blit(fon, (0, 0))
    hero_choise_sprites = pygame.sprite.Group()
    MenuSprite(load_image(list_hero[0], -1), 610, 450, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(list_hero[1], -1), 510, 360, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(list_hero[2], -1), 710, 360, 80, 90, hero_choise_sprites)

    font = streak([i[1] for i in select_from_db()])
    streak_text = UpheavalFont(is_black=True)
    font = streak_text.write_text(f"{font}")

    score_max = max(list(map(int, [i[2] for i in select_from_db()])), default=0)
    score_text = UpheavalFont(is_black=True)
    score_max = score_text.write_text(f"{score_max}")

    win_rate = wr([i[1] for i in select_from_db()])
    wr_text = UpheavalFont(is_black=True)
    win_rate = wr_text.write_text(f"{win_rate}%")

    i, j = 0, 0
    f = "isaac.draw(screen)"
    f1 = "new.draw(screen)"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    i += 1
                    hero_choise_sprites = pygame.sprite.Group()
                    whoam.draw(screen)
                    f = draw_name(i)
                    list_hero = list_hero[1:] + list_hero[:1]
                    create_hero_sprites(list_hero, hero_choise_sprites)
                    hero_choise_sprites.draw(screen)

                elif event.key == pygame.K_RIGHT:
                    i -= 1
                    hero_choise_sprites = pygame.sprite.Group()
                    whoam.draw(screen)
                    f = draw_name(i)
                    list_hero = list_hero[-1:] + list_hero[:-1]
                    create_hero_sprites(list_hero, hero_choise_sprites)
                    hero_choise_sprites.draw(screen)

                # elif event.key == pygame.K_DOWN:
                #     j += 1
                #     f1 = draw_menu(j)
                #
                # elif event.key == pygame.K_UP:
                #     j -= 1
                #     f1 = draw_menu(j)

                elif event.key == pygame.K_RETURN:
                    if check_selection(j, i) is not None:
                        return check_selection(j, i)
                    return 0
                elif event.key == pygame.K_ESCAPE:
                    return start_screen.run()

            whoam.draw(screen)
            hero_choise_sprites.draw(screen)
            eval(f)
            eval(f1)
            screen.blit(score_max, (60, 245))

            screen.blit(win_rate, (150, 290))

            screen.blit(font, (200, 680))
            pygame.display.flip()
