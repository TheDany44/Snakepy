#importar pygame
import pygame
import random
from pygame.display import update
import sys

#inicializar pygame
pygame.init()

#importar variáveis de cor
White = (255,255,255)
Black = (0,0,0)
Green = (0,192,0)
LightGreen = (96,255,128)
Blue = (0,32,255)
Red = (255,0,0)

#Global Variaveis
xRect = 10
yRect = 10
clock = 0
velocity = 10


#atributos da area de jogo e screen
def window(x_screen_change,y_screen_change):
    global x_border, y_screen,x_screen,y_border,thickness,screen
    
    x_border = x_screen = x_screen_change
    y_screen = y_screen_change
    y_border = y_screen - 30
    thickness = 20

    #inicializar a janela
    screen = pygame.display.set_mode((x_screen,y_screen))
    pygame.display.set_caption("Snake")

#inicializar funcao que escreve texto
def text(words, center, size,  color):
    """
    Parameters:
    words : string
    center : tuple (coords) or align
    size : integer
    color : name of color (from var "COLORS")
    """
    font = pygame.font.SysFont(None, size)
    text = font.render(words, True, color, None)
    textRect = text.get_rect()
    if center == "topleft":
        textRect.topleft = (10,10)
    elif center == "bottomleft":
        textRect.bottomleft = (10,y_screen-10)
    elif center == "bottomright":
        textRect.bottomright = (x_screen-10,y_screen-10)
    elif center == "midbottom":
        textRect.midbottom = (x_screen/2,y_screen)
    else:
        textRect.center = center
    screen.blit(text, textRect)
    return textRect

#função menu final
def end(points):
    screen.fill(Black)
    text(f"Defeat! Score={points}",(x_screen/2,y_screen/2 - 15),70,White)
    playagainRect = text("Play Again",(x_screen/2,y_screen/2 + 35),40,LightGreen)
    pygame.display.update()
    click = False
    while True:
        #get mouse pos
        mx,my = pygame.mouse.get_pos()

        #check buttons
        if click:
            if playagainRect.collidepoint((mx,my)):
                main_menu()
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


#função do jogo principal


def game():
    global start_move

    #verificar perda
    
    def check_defeat(snake,borders,points):
        rectsanteriores = snake.copy()
        del rectsanteriores[-1]
        if pygame.Rect.collidelistall(snake[-1],rectsanteriores) != [] or pygame.Rect.collidelistall(snake[-1],borders) != []:
            end(points)

    #definir score

    def score(previous,atual,points):
        if previous != atual:
            points += 10
        text(f"Score: {points}","midbottom",40,White)
        return points

    #definir onde comeca a snake
    x = random.randint(thickness/10,(x_border-thickness-xRect)/10)*10 #(20-970)
    y = random.randint(thickness/10,(y_border-thickness-yRect)/10)*10 #(20-720)

    
    #desenha a food

    def food(x_y):
        x = random.randint(thickness/10,(x_border-thickness-xRect)/10)*10 #(20-970)
        y = random.randint(thickness/10,(y_border-thickness-yRect)/10)*10 #(20-720)
        for i in range(len(x_y)):
            xx,yy = x_y[i]
            if x == xx and y == yy:
                return food(x_y)
        return x,y

            
    #Função que desenha a snake
    def draw_snake(x,y,x_food,y_food,foodRect,snake,x_y):
        global start_move
        x_y.append((x,y))
        snake.append(pygame.Rect(x,y,xRect,yRect))
        if start_move:
            x_food,y_food = food(x_y)
            start_move = False
        else:
            if pygame.Rect.colliderect(foodRect,snake[-1]):
                x_food,y_food = food(x_y)
            else:
                del snake[0]

        foodRect = pygame.Rect(x_food,y_food,xRect,yRect)
        pygame.draw.rect(screen,Blue,foodRect)
        for a in range(len(snake)):
            pygame.draw.rect(screen,Green,snake[a])
        return x_food, y_food, foodRect, snake, x_y

    #funcão que carrega os atributos
    def loadscreen():
        #desenhar area de jogo
        pygame.draw.rect(screen,Red,[0,0,x_border,y_border])
        pygame.draw.rect(screen,Black,[thickness,thickness,x_border-thickness*2,y_border-thickness*2])

    #reseta o screen e variaveis
    screen.fill(Black)

    x_change = 0
    y_change = 0
    start_move = True
    x_food = 0
    y_food = 0
    foodRect = 0
    snake = []
    prevlen = 1
    borders = [pygame.Rect(0,0,thickness,y_border),pygame.Rect(x_border-thickness,0,thickness,y_border),pygame.Rect(0,0,x_border,thickness),pygame.Rect(0,y_border-thickness,x_border,thickness)]
    points = 0
    x_y = []
    xandy2 = []
    

    #definir o clock do jogo
    clock = pygame.time.Clock()
    #update ao estado inicial do jogo
    pygame.display.update()
    #ciclo do jogo
    run = True
    while run:
        screen.fill(Black)
        loadscreen()      
        if x_change == 0 and y_change == 0:
            vertical = True
            horizontal = True
        elif x_change == 0:
            vertical = False
            horizontal = True
        elif y_change == 0:
            vertical = True
            horizontal = False

        x += x_change
        y += y_change
        
        clock.tick(velocity)
        if not start_move:
            prevlen = len(snake)
        
        
        x_food, y_food, foodRect, snake, x_y = draw_snake(x,y,x_food,y_food,foodRect,snake,x_y)
        
        check_defeat(snake,borders,points)
        
        points = score(prevlen,len(snake),points)
        

        pygame.display.update()
        #eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and vertical:
                    x_change = 0
                    y_change = -10
                if event.key == pygame.K_DOWN and vertical:
                    x_change = 0
                    y_change = 10
                elif event.key == pygame.K_LEFT and horizontal:
                    x_change = -10
                    y_change = 0
                elif event.key == pygame.K_RIGHT and horizontal:
                    x_change = 10
                    y_change = 0         

#funçao do menu principal
def main_menu():
    window(1000,780)
    #Pintar janela
    screen.fill(Black)

    #Escrever jogo título
    text("Classic Snake Game",(x_screen/2,y_screen/2 - 15),70,White)

    #button play
    playRect = text("Play",(x_screen/2,y_screen/2 +35),40,LightGreen)

    #update do screen do main menu
    pygame.display.update()

    #ciclo do main menu
    click = False
    while True:

        #Get mouse pos
        mx,my = pygame.mouse.get_pos()

        #deteta carregamento do butão play
        if click:
            if playRect.collidepoint((mx,my)): 
                game()
                
        click = False

        #Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


#identificar função principal
if __name__ == "__main__":
    main_menu()
