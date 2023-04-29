import random
import pygame
import math

BLACK = (0, 0, 0)
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Paint')
screen.fill(BLACK)
base = pygame.Surface((800, 600))

draw_on = False

prev_Pos = (0, 0)

colors = {
    'red' : (255, 0, 0),
    'blue' : (0, 0, 255),
    'green' : (0, 255, 0),
    'white' : (255, 255, 255),
    'purple' : (255, 0, 255),
    'brown' : (150, 75, 0),
    'olive' : (128, 128, 0),
    'sky blue' : (0, 255, 255)
}

color = colors['green']
reflect = 'pen'

def Rect_pos(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))



done = False

while not done:
    for current_Pos in pygame.event.get():
        if current_Pos.type == pygame.QUIT:
            done = True
        if current_Pos.type == pygame.KEYDOWN: # for changing pens
            if current_Pos.key == pygame.K_r:
                color = colors['red']
            if current_Pos.key == pygame.K_n:
                color = colors['brown']
            if current_Pos.key == pygame.K_g:
                color = colors['green']
            if current_Pos.key == pygame.K_a:
                color = colors['sky blue']
            if current_Pos.key == pygame.K_w:
                color = colors['white']
            if current_Pos.key == pygame.K_o:
                color = colors['olive']
            if current_Pos.key == pygame.K_u:
                color = colors['purple']
            if current_Pos.key == pygame.K_b:
                color = colors['blue']
            if current_Pos.key == pygame.K_p:
                reflect = 'pen'
            if current_Pos.key == pygame.K_h:
                reflect = 'rhombus'    
            if current_Pos.key == pygame.K_k:
                reflect = 'rectangle'
            if current_Pos.key == pygame.K_s:
                reflect = 'square'    
            if current_Pos.key == pygame.K_e:
                reflect = 'erase'
            if current_Pos.key == pygame.K_t:
                reflect = 'right triangle'
            if current_Pos.key == pygame.K_c:
                reflect = 'circle'
            if current_Pos.key == pygame.K_q:
                reflect = 'equilateral triangle'
        if current_Pos.type == pygame.MOUSEBUTTONDOWN:
            draw_on = True
            prev_Pos = current_Pos.pos
        if current_Pos.type == pygame.MOUSEBUTTONUP:
            draw_on = False
            base.blit(screen, (0, 0))
        if current_Pos.type == pygame.MOUSEMOTION: # functions for figures
            if draw_on == True:
                if reflect == 'circle':
                    screen.blit(base, (0, 0))
                    pygame.draw.circle(screen, color, (prev_Pos[0], prev_Pos[1]), int(math.sqrt((current_Pos.pos[0] - prev_Pos[0]) ** 2 + (current_Pos.pos[1] - prev_Pos[1]) ** 2)))
                if reflect == 'rectangle':
                    screen.blit(base, (0, 0))
                    a = Rect_pos(prev_Pos[0], prev_Pos[1], current_Pos.pos[0], current_Pos.pos[1])
                    pygame.draw.rect(screen, color, pygame.Rect(a))
                if reflect == 'pen':
                    pygame.draw.line(screen, color, [prev_Pos[0], prev_Pos[1]], [current_Pos.pos[0], current_Pos.pos[1]], 5)
                    prev_Pos = current_Pos.pos
                if reflect == 'erase':
                    pygame.draw.circle(screen, BLACK, (current_Pos.pos[0], current_Pos.pos[1]), 9)
                if reflect == 'square':
                    screen.blit(base, (0, 0))
                    a = Rect_pos(prev_Pos[1], prev_Pos[1], current_Pos.pos[1], current_Pos.pos[1])
                    pygame.draw.rect(screen, color, pygame.Rect(a))
                if reflect == 'right triangle':
                    screen.blit(base, (0, 0))
                    pygame.draw.polygon(screen, color, [(prev_Pos[0], prev_Pos[1] + current_Pos.pos[0]), (prev_Pos[0], prev_Pos[1]), (prev_Pos[0] + 2 * current_Pos.pos[0], prev_Pos[1])])
                if reflect == 'equilateral triangle':
                    screen.blit(base, (0, 0))
                    pygame.draw.polygon(screen, color, [(prev_Pos[0] - current_Pos.pos[0], prev_Pos[0] + current_Pos.pos[0]), (prev_Pos[0] + current_Pos.pos[0], prev_Pos[0] + current_Pos.pos[0]), (prev_Pos[0], prev_Pos[0] - current_Pos.pos[0])])
                if reflect == 'rhombus':
                    pos1 = (prev_Pos[0] / 2, prev_Pos[1] / 2 - current_Pos.pos[0] / 2)
                    pos2 = (pos1[0] - current_Pos.pos[1] / 2, pos1[1] + current_Pos.pos[0] / 2)
                    pos3 = (pos1[0], pos1[1] + current_Pos.pos[0])
                    pos4 = (pos2[0] + current_Pos.pos[1], pos2[1])
                    points = [pos1, pos2, pos3, pos4]
                    screen.blit(base, (0, 0))
                    pygame.draw.polygon(screen, color, points)
    pygame.display.flip()
pygame.quit()
