import random, pygame, time, sys
from tkinter import W

pygame.init()
resolution = (500,500)
screen = pygame.display.set_mode(resolution)
game_over = pygame.font.SysFont("Verdana", 60).render("Game Over", True, (255, 0, 0)) #TEXT Charecteristic

def create_rect(width, height, border, color, border_color):
    surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (border, border, width, height), 0)
    for i in range(1, border):
        pygame.draw.rect(surf, border_color, (border-i, border-i, width+5, height+5), 1)
    return surf

def game_end():
    screen.blit(game_over, (75, 190))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()
class Snake:
    def __init__(self, x, y):
        self.score = 0
        self.is_alive = True
        self.level = 1
        self.size = 1
        self.elements = [[x, y]]  # [[x0, y0], [x1, y1], [x2, y2] ...] (i) -> (i - 1)
        self.radius = 10
        self.dx = 0  # Right/Left
        self.dy = 0  # Up/Down
        self.is_add = False
        self.speed = 30

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (255, 255, 255), element, self.radius)
                                        #color SNAKE
    def add_to_snake(self,food_size=3):
        self.size += food_size
        for element in range(food_size):
            self.elements.append([0, 0])
        self.is_add = False
        if self.size % 5 == 0:
            self.speed += 10
    def walls(self):
        if self.level>1:
            return True

    def move(self):
        if self.is_add:
            self.add_to_snake()

        for i in range(self.size - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]

        #to avoid to going out for infinity
        
        if self.level>1:
            if self.elements[0][0] >= 120 and self.elements[0][0] <= 190 and self.elements[0][1] >= 120 and self.elements[0][1] <= 220:
                self.is_alive = False
                game_end()
            elif self.elements[0][0] >= 270 and self.elements[0][0] <= 420 and self.elements[0][1] >= 150 and self.elements[0][1] <= 300:
                self.is_alive=False  #area of DEAD ZONE
                game_end()
        if (self.elements[0][0] == 20):
            game_end()            
        if (self.elements[0][0] == resolution[0]-20):
            game_end()
        if (self.elements[0][1] == 20):
            game_end()
        if(self.elements[0][1] == resolution[1]-20):
            game_end()
        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy
        

    def eat(self, foodx, foody):
        x = self.elements[0][0]
        y = self.elements[0][1]
        if foodx <= x <= foodx + 10 and foody <= y <= foody + 10:
            return True
        return False
    

border_res = (30,470)
class Food:
    def __init__(self,food_size,is_exist=True):
        self.is_exist = is_exist
        self.food_size = food_size
        self.x = random.randint(border_res[0],border_res[1])
        self.y = random.randint(border_res[0],border_res[1])

    def gen(self):
        self.x = random.randint(border_res[0],border_res[1])
        self.y = random.randint(border_res[0],border_res[1])

    def draw(self):
        pygame.draw.rect(screen, (60, 60, 148), (self.x, self.y, 10+self.food_size, 10 + self.food_size))
                                 #color food

border = create_rect(485, 485, 10, (0, 0, 0),(255,0, 0))
Snake = Snake(250, 250)
food = Food(1)
bonus = Food(5,False)

running = True

#Good flow
snake_frame_speed = 5
frame_counter = 0
FPS = 120

d = 5

clock = pygame.time.Clock()

spawn_status = True

spawn_bonus = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_bonus, 4000)
spawn_pause = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_pause, 5000)

start_pos = 250
snake = [(start_pos,start_pos)]
spawn_status = False

while running:
    frame_counter+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_bonus:
            bonus.gen()
            if bonus.is_exist:
                bonus.is_exist = False
            elif bonus.is_exist == False:
                bonus.is_exist=True
            spawn_status = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            #CONTROLLER
            if event.key == pygame.K_RIGHT and Snake.dx != -d:
                Snake.dx = d
                Snake.dy = 0
            if event.key == pygame.K_LEFT and Snake.dx != d:
                Snake.dx = -d
                Snake.dy = 0
            if event.key == pygame.K_UP and Snake.dy != d:
                Snake.dx = 0
                Snake.dy = -d
            if event.key == pygame.K_DOWN and Snake.dy != -d:
                Snake.dx = 0
                Snake.dy = d

    if Snake.eat(food.x, food.y):
        Snake.is_add = True
        Snake.score+=3
        food.gen()
    if Snake.eat(bonus.x, bonus.y):
        Snake.is_add = True
        bonus.is_exist = False
        Snake.score+=1
    
    
    if frame_counter%snake_frame_speed==0:
        if Snake.score>70:
            Snake.level +=1 #Criteries of next level
        print(Snake.size)
        screen.fill((0, 0, 0))
        screen.blit(border,(0,0))
        if (Snake.walls()):
            pygame.draw.rect(screen, (255,0,255), pygame.Rect(120, 120, 70, 100)) # 100 - 200
            pygame.draw.rect(screen, (255,0,255), pygame.Rect(270, 150, 150, 150)) #270 - 350
        Snake.move()    
        Snake.draw()
        food.draw()
        scores = pygame.font.SysFont("Verdana", 10).render(str(Snake.score), True, (255, 255, 255))
        screen.blit(scores,(15,15))
        if bonus.is_exist:
            bonus.draw()
        
    

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()