#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.entity import Entity


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, ):
        self.rect.x -= 1

        image_width = self.rect.width

        if self.rect.right <= 0:
            self.rect.x += image_width * 2