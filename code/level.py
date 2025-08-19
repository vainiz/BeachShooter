#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame

from code.entity import Entity
from code.entityFactory import EntityFactory


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            for ent in self.entity_list:
                ent.move()
            self.window.fill((0, 0, 0))
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)


            pygame.display.flip()

            # Limita o jogo a 60 frames por segundo
            clock.tick(60)
