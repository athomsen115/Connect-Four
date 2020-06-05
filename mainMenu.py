import pygame
import connect4
from AI_Connect4 import *


pygame.init()
pygame.font.init()
WIDTH = 700
HEIGHT = 700
RADIUS = 100
win = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    run = True
    click = False
    while run:
        win.fill(BLACK)
        title = pygame.image.load("title.png")
        win.blit(title, (0,0))
        
        buttonFont = pygame.font.SysFont('comicsans', 30)
        posx, posy = pygame.mouse.get_pos()
        
        button1 = pygame.draw.circle(win, YELLOW, (200, 500), RADIUS)
        twoPlayer = buttonFont.render("Two-Player", 1, RED)
        win.blit(twoPlayer, (200 - twoPlayer.get_width()/2, 500 - twoPlayer.get_height()/2))
        button2 = pygame.draw.circle(win, RED, (500, 500), RADIUS)
        AIGame = buttonFont.render("Against an AI", 1, YELLOW)
        win.blit(AIGame, (500 - AIGame.get_width()/2, 500 - AIGame.get_height()/2))
        pygame.display.update()
        
        if button1.collidepoint(posx, posy):
            if click:
                win.fill(BLACK)
                connect4.main()
                click = False
        if button2.collidepoint(posx, posy):
            if click:
                AIMainMenu()
                click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update
                
                
main()