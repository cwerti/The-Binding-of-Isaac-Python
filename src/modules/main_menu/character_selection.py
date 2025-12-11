import pygame
from typing import List, Tuple, Optional

from src.modules.banners.upheaval_font import UpheavalFont
from src.utils.funcs import load_image, select_from_db


# Магические константы вынесены в понятные переменные (исправлено: Магические константы)
CHARACTER_MENU_CONSTANTS = {
    'BACKGROUND_PATH': 'images/menu/choise_fon.png',
    'HERO_SPRITE_PATHS': [
        "images/menu/isaac.png",
        "images/menu/cain.png",
        "images/menu/lost.png",
    ],
    'HERO_NAME_PATHS': [
        "images/menu/isaac_name.png",
        "images/menu/cain_name.png", 
        "images/menu/lost_name.png",
    ],
    'HERO_INFO_PATHS': [
        "images/menu/isaac_info.png",
        "images/menu/cain_info.png",
        "images/menu/lost_info.png",
    ],
    'HERO_POSITIONS': [(610, 450), (510, 360), (710, 360)],
    'HERO_SIZE': (80, 90),
    'HERO_NAMES': ["isaac", "cain", "lost"],
    'MENU_ITEM_NAMES': ["new", "continue", "options"],
    'WHOAM_PATH': 'images/menu/whoam.png',
    'LEFT_ARROW_PATH': 'images/menu/left.png',
    'RIGHT_ARROW_PATH': 'images/menu/right.png',
    'SHEET_PATH': 'images/menu/sheet.png',
    'BUTTON_PATHS': [
        'images/menu/new_run.png',
        'images/menu/continue_true.png',
        'images/menu/options.png'
    ],
    'BUTTON_POSITIONS': [(945, 300), (950, 370), (955, 435)],
    'ARROW_BUTTON_POSITIONS': [(905, 335), (910, 405), (910, 475)],
    'NAME_POSITION': (570, 550),
    'INFO_POSITION': (480, 630),
    'TEXT_SCORE_POS': (60, 245),
    'TEXT_WIN_RATE_POS': (150, 290),
    'TEXT_STREAK_POS': (200, 680),
}


class CharacterSelectionMenu:
    """
    Класс для меню выбора персонажа, выделенный из длинной функции choise_menu
    Это улучшает читаемость и поддерживаемость кода. (исправлено: Длинный метод)
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.fon = pygame.transform.scale(
            load_image(CHARACTER_MENU_CONSTANTS['BACKGROUND_PATH']),
            (pygame.display.Info().current_w, pygame.display.Info().current_h),
        )
        
        # Инициализация спрайтов
        self.whoam_sprites = pygame.sprite.Group()
        self.hero_choise_sprites = pygame.sprite.Group()
        self.name_groups = [pygame.sprite.Group() for _ in CHARACTER_MENU_CONSTANTS['HERO_NAMES']]
        self.menu_groups = [pygame.sprite.Group() for _ in CHARACTER_MENU_CONSTANTS['MENU_ITEM_NAMES']]
        
        self._setup_sprites()
        
        # Состояния меню
        self.hero_index = 0
        self.menu_index = 0 
        
        # Тексты статистики
        self.score_text = self._create_score_text()
        self.win_rate_text = self._create_win_rate_text()
        self.streak_text = self._create_streak_text()
        
    def _setup_sprites(self):
        """Настройка всех спрайтов для меню выбора персонажа"""
        # Фоновые элементы
        self._setup_background_elements()
        # Создание персонажей
        self._setup_character_sprites()
        # Создание кнопок меню
        self._setup_menu_buttons()
        # Создание имен и информации о персонажах
        self._setup_character_names_and_info()
    
    def _setup_background_elements(self):
        """Настройка фоновых элементов меню"""
        # WHO AM I рамка
        MenuSprite(
            load_image(CHARACTER_MENU_CONSTANTS['WHOAM_PATH'], -1),
            350, 100, 600, 740,
            self.whoam_sprites
        )
        # Стрелки навигации
        MenuSprite(
            load_image(CHARACTER_MENU_CONSTANTS['LEFT_ARROW_PATH'], -1),
            510, 560, 50, 50,
            self.whoam_sprites
        )
        MenuSprite(
            load_image(CHARACTER_MENU_CONSTANTS['RIGHT_ARROW_PATH'], -1),
            710, 560, 50, 50,
            self.whoam_sprites
        )
        # Таблица характеристик
        MenuSprite(
            load_image(CHARACTER_MENU_CONSTANTS['SHEET_PATH'], -1),
            880, 200, 700, 600,
            self.whoam_sprites
        )
    
    def _setup_character_sprites(self):
        """Настройка спрайтов персонажей"""
        for img_path, (pos_x, pos_y) in zip(
            CHARACTER_MENU_CONSTANTS['HERO_SPRITE_PATHS'],
            CHARACTER_MENU_CONSTANTS['HERO_POSITIONS']
        ):
            MenuSprite(
                load_image(img_path, -1),
                pos_x, pos_y,
                CHARACTER_MENU_CONSTANTS['HERO_SIZE'][0],
                CHARACTER_MENU_CONSTANTS['HERO_SIZE'][1],
                self.hero_choise_sprites
            )
    
    def _setup_menu_buttons(self):
        """Настройка кнопок меню"""
        for i, (btn_path, btn_pos) in enumerate(zip(
            CHARACTER_MENU_CONSTANTS['BUTTON_PATHS'],
            CHARACTER_MENU_CONSTANTS['BUTTON_POSITIONS']
        )):
            # Кнопка меню
            MenuSprite(
                load_image(btn_path, -1),
                btn_pos[0], btn_pos[1],
                280, 90,
                self.whoam_sprites
            )
            
            # Стрелка рядом с кнопкой меню
            MenuSprite(
                load_image(CHARACTER_MENU_CONSTANTS['RIGHT_ARROW_PATH'], -1),
                CHARACTER_MENU_CONSTANTS['ARROW_BUTTON_POSITIONS'][i][0],
                CHARACTER_MENU_CONSTANTS['ARROW_BUTTON_POSITIONS'][i][1],
                50, 50,
                self.menu_groups[i]
            )
    
    def _setup_character_names_and_info(self):
        """Настройка спрайтов имен и информации о персонажах"""
        for i, (name_path, info_path) in enumerate(zip(
            CHARACTER_MENU_CONSTANTS['HERO_NAME_PATHS'],
            CHARACTER_MENU_CONSTANTS['HERO_INFO_PATHS']
        )):
            # Имя персонажа
            name_pos = CHARACTER_MENU_CONSTANTS['NAME_POSITION']
            # Смещение для lost из-за другого размера
            offset_x = -10 if i == 2 else 0
            offset_y = -10 if i == 2 else 0
            
            MenuSprite(
                load_image(name_path, -1),
                name_pos[0] + offset_x,
                name_pos[1] + offset_y,
                150 if i != 2 else 160,  # Ширина различается для 'lost'
                70 if i != 2 else 90,    # Высота различается для 'lost'
                self.name_groups[i]
            )
            
            # Информация о персонаже
            MenuSprite(
                load_image(info_path, -1),
                CHARACTER_MENU_CONSTANTS['INFO_POSITION'][0],
                CHARACTER_MENU_CONSTANTS['INFO_POSITION'][1],
                350, 70,
                self.name_groups[i]
            )
    
    def _create_score_text(self):
        """Создание текста для максимального счета"""
        scores = [int(row[2]) for row in select_from_db()]
        max_score = max(scores, default=0)
        score_font = UpheavalFont(is_black=True)
        return score_font.write_text(str(max_score))
    
    def _create_win_rate_text(self):
        """Создание текста для процента побед"""
        outcomes = [row[1] for row in select_from_db()]
        win_rate = self._calculate_win_rate(outcomes)
        rate_font = UpheavalFont(is_black=True)
        return rate_font.write_text(f"{win_rate}%")
    
    def _create_streak_text(self):
        """Создание текста для серии побед/поражений"""
        outcomes = [row[1] for row in select_from_db()]
        streak_result = self._calculate_streak(outcomes)
        streak_font = UpheavalFont(is_black=True)
        return streak_font.write_text(str(streak_result))
    
    def _calculate_win_rate(self, outcomes: List[str]) -> int:
        """Вычисление процента побед"""
        if not outcomes:
            return 0
        wins = outcomes.count("w")
        return int(wins / len(outcomes) * 100)
    
    def _calculate_streak(self, outcomes: List[str]) -> str:
        """Вычисление текущей серии (побед/поражений)"""
        if not outcomes:
            return "0"
        last_outcome = outcomes[-1]
        streak_str = ""
        
        for outcome in reversed(outcomes):
            if outcome == last_outcome:
                streak_str += outcome
            else:
                break
        
        if "l" in streak_str:
            return f"-{len(streak_str)}"
        return f"{len(streak_str)}"
    
    def handle_event(self, event) -> Optional[str]:
        """Обработка событий клавиатуры"""
        if event.type == pygame.QUIT:
            from src.modules.main_menu.start_screen import terminate
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._change_character(-1)
            elif event.key == pygame.K_RIGHT:
                self._change_character(1)
            elif event.key == pygame.K_RETURN:
                # Возвращаем имя выбранного персонажа
                return CHARACTER_MENU_CONSTANTS['HERO_NAMES'][self.hero_index]
            elif event.key == pygame.K_ESCAPE:
                # Возвращаем специальное значение для возврата к главному меню
                return "BACK_TO_MAIN"
        return None
    
    def _change_character(self, direction: int):
        """Изменение выбранного персонажа"""
        self.hero_index = (self.hero_index + direction) % len(CHARACTER_MENU_CONSTANTS['HERO_NAMES'])
        self._update_character_sprites()
    
    def _update_character_sprites(self):
        """Обновление спрайтов персонажей в соответствии с текущим выбором"""
        # Обновляем порядок изображений в зависимости от индекса
        hero_paths = CHARACTER_MENU_CONSTANTS['HERO_SPRITE_PATHS']
        rotated_paths = hero_paths[self.hero_index:] + hero_paths[:self.hero_index]
        
        # Пересоздаем спрайты с новым порядком
        self.hero_choise_sprites.empty()
        for img_path, (pos_x, pos_y) in zip(rotated_paths, CHARACTER_MENU_CONSTANTS['HERO_POSITIONS']):
            MenuSprite(
                load_image(img_path, -1),
                pos_x, pos_y,
                CHARACTER_MENU_CONSTANTS['HERO_SIZE'][0],
                CHARACTER_MENU_CONSTANTS['HERO_SIZE'][1],
                self.hero_choise_sprites
            )
    
    def draw(self):
        """Отрисовка всех элементов меню выбора персонажа"""
        # Отрисовка фона
        self.screen.blit(self.fon, (0, 0))
        
        # Отрисовка фоновых элементов
        self.whoam_sprites.draw(self.screen)
        
        # Отрисовка спрайтов персонажей
        self.hero_choise_sprites.draw(self.screen)
        
        # Отрисовка активного имени и информации о персонаже
        active_name_group = self.name_groups[self.hero_index % len(self.name_groups)]
        active_name_group.draw(self.screen)
        
        # Отрисовка активной кнопки меню (временно всегда первая)
        # NOTE: Обработка меню временно отключена, как в оригинальном коде
        if self.menu_groups:
            self.menu_groups[0].draw(self.screen)
        
        # Отрисовка текстов статистики
        self.screen.blit(self.score_text, CHARACTER_MENU_CONSTANTS['TEXT_SCORE_POS'])
        self.screen.blit(self.win_rate_text, CHARACTER_MENU_CONSTANTS['TEXT_WIN_RATE_POS'])
        self.screen.blit(self.streak_text, CHARACTER_MENU_CONSTANTS['TEXT_STREAK_POS'])


    def run(self):
        """Основной цикл работы меню выбора персонажа"""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result is not None:
                    if result == "BACK_TO_MAIN":
                        # Возвращаемся в главное меню
                        from src.modules.main_menu.start_screen import StartScreen
                        return StartScreen
                    else:
                        # Возвращаем имя выбранного персонажа
                        return result

            self.draw()
            pygame.display.flip()
            clock.tick(60)  # 60 FPS


# Класс MenuSprite, скопированный из оригинального файла для обеспечения работоспособности
class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, x: int, y: int, rx: int, ry: int, *group: pygame.sprite.Group):
        super().__init__(*group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (rx, ry))

    def update(self, y):
        self.rect.y = y