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

def end2(points,points2):
    screen.fill(Black)
    if points == points2:
        play1color = White
        play2color = White
    elif points > points2:
        play1color = Blue
        play2color = White
    else:
        play1color = White
        play2color = Blue
    text(f"Defeat! Total Score: {points + points2}",(x_screen/2,y_screen/2-15),70,White)
    text(f"Score Player1: {points}",(x_screen/2,y_screen/2+35),60,play1color)
    text(f"Score Player2: {points2}",(x_screen/2,y_screen/2+85),60,play2color)
    playagainRect = text("Play Again",(x_screen/2,y_screen/2 + 135),40,LightGreen)
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


def game(multi):
    global start_move

    #verificar perda
    if multi:
        def check_defeat2(snake,snake2,borders,points,points2):
            rectsanteriores = snake.copy()
            rectsanteriores2 = snake2.copy()
            del rectsanteriores[-1]
            del rectsanteriores2[-1]
            if pygame.Rect.collidelistall(snake[-1],rectsanteriores) != [] or pygame.Rect.collidelistall(snake[-1],borders) != [] or pygame.Rect.collidelistall(snake2[-1],rectsanteriores2) or pygame.Rect.collidelistall(snake2[-1],borders) or pygame.Rect.collidelistall(snake[-1],snake2) or pygame.Rect.collidelistall(snake2[-1],snake):
                end2(points,points2)
    else:
        def check_defeat(snake,borders,points):
            rectsanteriores = snake.copy()
            if pygame.Rect.collidelistall(snake[-1],rectsanteriores) != [] or pygame.Rect.collidelistall(snake[-1],borders) != []:
                end(points)

    #definir score
    if multi:
        def score2(previous,previous2,atual,atual2,points,points2):
            if previous != atual:
                points += 10
            if previous2 != atual2:
                points2 += 10
            text(f"Score Player1: {points}",(x_screen/3,y_screen-14),40,Green)
            text(f"Score Player2: {points2}",(x_screen/3*2,y_screen-14),40,White)
            return points, points2
    else:
        def score(previous,atual,points):
            if previous != atual:
                points += 10
            text(f"Score: {points}","midbottom",40,White)
            return points

    #definir onde comeca a snake
    x = random.randint(thickness/10,(x_border-thickness-xRect)/10)*10 #(20-970)
    y = random.randint(thickness/10,(y_border-thickness-yRect)/10)*10 #(20-720)

    if multi:
        def x_y2(x,y):
            x2 = random.randint(thickness/10,(x_border-thickness-xRect)/10)*10 #(20-970)
            y2 = random.randint(thickness/10,(y_border-thickness-yRect)/10)*10 #(20-720)
            if x == x2 or y == y2:
                x_y2(x,y)
            else:
                return x2,y2
        
        x2,y2 = x_y2(x,y)
    
    #desenha a food
    if multi:
        def food2(x_y,xandy2):
            x = random.randint(thickness/10,(x_border-thickness-xRect)/10)*10 #(20-970)
            y = random.randint(thickness/10,(y_border-thickness-yRect)/10)*10 #(20-720)
            for i in range(len(x_y)):
                xx,yy = x_y[i]
                if x == xx and y == yy:
                    return food2(x_y,xandy2)
            for i in range(len(xandy2)):
                xx,yy = xandy2[i]
                if x == xx and y == yy:
                    return food2(x_y,xandy2)
            return x,y
    else:
        def food(x_y):
            x = random.randint(thickness/10,(x_border-thickness-xRect)/10)*10 #(20-970)
            y = random.randint(thickness/10,(y_border-thickness-yRect)/10)*10 #(20-720)
            for i in range(len(x_y)):
                xx,yy = x_y[i]
                if x == xx and y == yy:
                    return food(x_y)
            return x,y

    def snakestart(snake,x_y):
        xx, yy = x_y[-1]

        def starting(xx,yy):
            value = random.randint(0,3)
            x_start_change = 0
            y_start_change = 0
            if value // 2 == 0:
                x_start_change = 10
                if value % 2 == 0:
                    x_start_change *= -1
            else:
                y_start_change = 10
                if value % 2 == 0:
                    y_start_change *= -1
            for i in range(4):
                if borders[i].collidepoint(xx+x_start_change,yy+y_start_change):
                    return starting(xx,yy)
            return x_start_change, y_start_change
        
        x_start_change, y_start_change = starting(xx,yy)
        for i in range(2):
            xx += x_start_change
            yy += y_start_change
            snake.append(pygame.Rect(xx,yy,xRect,yRect))
            x_y.append((xx,yy))
        return snake, x_y
        

            

    if multi:
        #desenha as snakes 
        def draw_snake2(x,y,x2,y2,x_food,y_food,x_food2,y_food2,foodRect,foodRect2,snake,snake2,x_y,xandy2):
            global start_move

            snake.append(pygame.Rect(x,y,xRect,yRect))
            snake2.append(pygame.Rect(x2,y2,xRect,yRect))

            if start_move:
                x_food,y_food = food2(x_y,xandy2)
                x_food2,y_food2 = food2(x_y,xandy2)
                start_move = False
            else:
                if pygame.Rect.colliderect(foodRect,snake[-1]):
                    x_food,y_food = food2(x_y,xandy2)
                elif pygame.Rect.colliderect(foodRect2,snake[-1]):
                    x_food2, y_food2 = food2(x_y,xandy2)
                else:
                    del snake[0]
                    
                if pygame.Rect.colliderect(foodRect,snake2[-1]):
                    x_food,y_food = food2(x_y,xandy2)
                elif pygame.Rect.colliderect(foodRect2,snake2[-1]):
                    x_food2, y_food2 = food2(x_y,xandy2)
                else:
                    del snake2[0]
                    
            foodRect2 = pygame.Rect(x_food2,y_food2,xRect,yRect)
            foodRect = pygame.Rect(x_food,y_food,xRect,yRect)

            pygame.draw.rect(screen,Blue,foodRect)
            pygame.draw.rect(screen,Blue,foodRect2)
            for a in range(len(snake)):
                pygame.draw.rect(screen,Green,snake[a])
            for b in range(len(snake2)):
                pygame.draw.rect(screen,White,snake2[b])
            return x_food, y_food, x_food2, y_food2, foodRect, foodRect2, snake, snake2,x_y,xandy2
    
    else:
        #Função que desenha a snake
        def draw_snake(x,y,x_food,y_food,foodRect,snake,x_y):
            global start_move
            x_y.append((x,y))
            if start_move:
                x_food,y_food = food(x_y)
                snake, x_y = snakestart(snake,x_y)
                snake.append(pygame.Rect(x,y,xRect,yRect))
                start_move = False
            else:
                snake.append(pygame.Rect(x,y,xRect,yRect))
                if pygame.Rect.colliderect(foodRect,snake[-1]):
                    x_food,y_food = food(x_y)
                elif len(snake) > 3:
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

    if multi:
        x_change2 = 0
        y_change2 = 0
        x_food2 = 0
        y_food2 = 0
        foodRect2 = 0
        snake2 = []
        prevlen2 = 1
        points2 = 0
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

        if multi:
            if x_change2 == 0 and y_change2 == 0:
                vertical2 = True
                horizontal2 = True
            elif x_change2 == 0:
                vertical2 = False
                horizontal2 = True
            elif y_change2 == 0:
                vertical2 = True
                horizontal2 = False

        x += x_change
        y += y_change
        if multi:
            x2 += x_change2
            y2 += y_change2
        clock.tick(velocity)
        if not start_move:
            prevlen = len(snake)
        if multi:
            if not start_move:
                prevlen2 = len(snake2)
        if not multi:
            x_food, y_food, foodRect, snake, x_y = draw_snake(x,y,x_food,y_food,foodRect,snake,x_y)
        else:
            x_food,y_food,x_food2,y_food2,foodRect,foodRect2,snake,snake2, x_y, xandy2 = draw_snake2(x,y,x2,y2,x_food,y_food,x_food2,y_food2,foodRect,foodRect2,snake,snake2, x_y, xandy2)
        if not multi:
            check_defeat(snake,borders,points)
        else:
            check_defeat2(snake,snake2,borders,points,points2)
        if not multi:
            points = score(prevlen,len(snake),points)
        else:
            points, points2 = score2(prevlen,prevlen2,len(snake),len(snake2),points,points2)

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
                if multi:
                    if event.key == pygame.K_w and vertical2:
                        x_change2 = 0
                        y_change2 = -10
                    elif event.key == pygame.K_s and vertical2:
                        x_change2 = 0
                        y_change2 = 10
                    elif event.key == pygame.K_a and horizontal2:
                        x_change2 = -10
                        y_change2 = 0
                    elif event.key == pygame.K_d and horizontal2:
                        x_change2 = 10
                        y_change2 = 0

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
    multi = False
    click = False
    while True:

        #Get mouse pos
        mx,my = pygame.mouse.get_pos()

        #deteta carregamento do butão play
        if click:
            if playRect.collidepoint((mx,my)) and not multi: 
                multi = True
                screen.fill(Black)
                singleplayerRect = text("1 Player",(x_screen/2,y_screen/3),60,White)
                multiplayerRect = text("2 Players",(x_screen/2,y_screen/3 *2),60,White)
                pygame.display.update()
            if multi:
                if singleplayerRect.collidepoint((mx,my)):
                    game(False)
                if multiplayerRect.collidepoint((mx,my)):
                    game(True)
                
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
