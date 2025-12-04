import random
import sys

import pygame
import pygame as pg

import src.consts
from src.modules.banners.shop_font import ShopFont
from src.modules.main_menu.start_screen import MenuSprite
from src.utils.funcs import add_db, load_image

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


def terminate():
    pygame.quit()
    sys.exit()


def save_score(score):
    add_db("l", score)


def save_and_exit(score):
    save_score(score)
    terminate()


def end_screen(screen, hero, score):
    end_list = pygame.sprite.Group()
    # Магические константы
    DEATH_LIST_POS = (320, 100, 660, 760)
    HERO_NAME_POS = (780, 223, 150, 70)
    RANDOM_IMAGE_POS = (670, 400, 150, 90)
    BANNER_POS = (430, 610)

    MenuSprite(
        load_image("images/menu/death_list.png", -1),
        *DEATH_LIST_POS,
        end_list,
    )
    MenuSprite(
        load_image(f"images/menu/{hero}_name.png", -1),
        *HERO_NAME_POS,
        name := pygame.sprite.Group(),
    )
    MenuSprite(
        load_image(f"images/menu/deth/image_part_00{random.randint(1, 9)}.png", -1),
        *RANDOM_IMAGE_POS,
        name,
    )
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(200)
    font = ShopFont(is_black=True)
    banner = font.write_text(f"{abs(score)}")
    screen.blit(surf, (0, 0))
    end_list.draw(screen)
    name.draw(screen)
    screen.blit(banner, BANNER_POS)
    pygame.display.flip()
    # дублирование кода
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                save_and_exit(score)
                return

            if event.type == pygame.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_SPACE, pg.K_RETURN):
                    if event.key == pg.K_ESCAPE:
                        save_and_exit(score)
                    else:
                        save_score(score)
                        return True
