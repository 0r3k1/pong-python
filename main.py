#!user/bin/env python
# -*- coding: utf-8 -*-

import pygame, clases
from clases import alto, ancho, paleta, blanco, negro

def main():
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 120)

    quit = False
    puntos = [0, 0]
    centrox = ancho/2

    pelota = clases.pelota((ancho/2), (alto/2))
    player = clases.player(10, (alto/2))
    pc = clases.pc(ancho-25, (alto/2))


    while not quit:
        pj = font.render("{0}".format(puntos[0]), 1, paleta[blanco])
        pp = font.render("{0}".format(puntos[1]), 1, paleta[blanco])

        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit = True
            player.handle(event)

        pelota.punto(pelota.handle(), puntos)
        pc.handle(pelota)

        pelota.colicion(player)
        pelota.colicion(pc)
        player.colicion(pelota)

        player.limites()
        pc.limites()

        pelota.mueve()
        player.mueve()
        pc.mueve()

        ventana.fill(paleta[negro])
        pygame.draw.line(ventana, paleta[blanco], (centrox+3, 0), (centrox+3, alto), 6)
        ventana.blit(pj, (centrox-80, 15))
        ventana.blit(pp, (centrox+30, 10))
        pelota.pinta(ventana)
        player.pinta(ventana)
        pc.pinta(ventana)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

main()
