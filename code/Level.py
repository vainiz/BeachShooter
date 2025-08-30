#!/usr/-bin/python
# -*- coding: utf-8 -*-
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_WHITE, WIN_HEIGHT, WIN_WIDTH, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_CYAN, \
    EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player
from code.Enemy import Enemy


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))

        player1 = EntityFactory.get_entity('Player1')
        player1.score = player_score[0]
        self.entity_list.append(player1)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player2 = EntityFactory.get_entity('Player2')
            player2.score = player_score[1]
            self.entity_list.append(player2)

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        self.timeout = TIMEOUT_LEVEL
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    self.entity_list.append(EntityFactory.get_entity('Enemy1'))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout <= 0:
                        return True

            for ent in self.entity_list:
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot:
                        self.entity_list.append(shoot)

            EntityMediator.verify_collision(self.entity_list)
            EntityMediator.verify_health(self.entity_list)

            found_player = any(isinstance(ent, Player) for ent in self.entity_list)
            if not found_player:
                return False

            self.window.fill((0, 0, 0))
            for ent in self.entity_list:
                self.window.blit(ent.surf, ent.rect)

            player1 = next((ent for ent in self.entity_list if ent.name == 'Player1'), None)
            player2 = next((ent for ent in self.entity_list if ent.name == 'Player2'), None)

            if player1:
                player_score[0] = player1.score
                self.level_text(14, f'JOGADOR 1 - VIDA: {player1.health} | PONTOS: {player1.score}', C_GREEN, (10, 25))
            if player2:
                player_score[1] = player2.score
                self.level_text(14, f'JOGADOR 2 - VIDA: {player2.health} | PONTOS: {player2.score}', C_CYAN, (10, 45))

            self.level_text(14, f'TEMPO: {self.timeout / 1000:.0f}', C_WHITE, (WIN_WIDTH / 2 - 40, 5))

            pygame.display.flip()
            clock.tick(60)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)