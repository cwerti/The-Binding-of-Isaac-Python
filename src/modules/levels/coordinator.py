import pygame as pg
from typing import Dict, List, Callable
from src.modules.characters.main_hero import Player
from src.modules.levels.room import Room
from src.modules.levels.level import Level
from src.modules.menus.stats_line import Stats


class GameCoordinator:
    """
    Координирует действия в игре
    """

    def __init__(self, main_hero: Player, current_level: Level, stats: Stats):
        self.main_hero = main_hero
        self.current_level = current_level
        self.stats = stats
        self.rooms_dict: Dict[tuple[int, int], Room] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}

        self.enemies = []
        self.items = []
        self.doors = []
        self.bosses = []

    def handle_enemy_damage(self, enemy, damage_source, damage_amount):

        if hasattr(enemy, 'hurt'):
            enemy.hurt(damage_amount)

        if hasattr(damage_source, 'is_hero') and damage_source.is_hero:
            self.main_hero.add_score(10)
            self.stats.update_hero_stats()

    def process_item_pickup(self, player, item):
        player.handle_item_pickup(item)

        self.stats.update_hero_stats()

    def update_room_state(self, room: Room):
        room.update_room_state()
        self.stats.update_minimap()

    def handle_level_transition(self, direction):
        self.current_level.move_to_next_room(direction)
        self.main_hero.reset_speed()
        self.stats.update_current_stats(self.main_hero, self.current_level)
        self.current_level.update_main_hero_collide_groups()
