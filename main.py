# Atualizado por: Leonardo Hilgemberg Lopes.
# Athenasarch

import pygame  # Importando a biblioteca pygame para a criação de jogos
from copy import deepcopy  # Importando a função deepcopy para cópias completas de listas
from random import choice, randrange  # Importando a função choice para escolher elementos aleatórios de uma lista e randrange para números aleatórios

W, H = 10, 16  # Definindo a largura e a altura do campo do jogo em blocos
TILE = 40  # Definindo o tamanho de cada bloco
GAME_RES = W * TILE, H * TILE  # Definindo a resolução do campo do jogo
RES = 750, 800  # Definindo a resolução da janela do jogo
FPS = 60  # Definindo a taxa de quadros por segundo

pygame.init()  # Iniciando o pygame
sc = pygame.display.set_mode(RES)  # Criando a janela do jogo
game_sc = pygame.Surface(GAME_RES)  # Criando a superfície do campo do jogo
clock = pygame.time.Clock()  # Criando um objeto de relógio para controlar a taxa de quadros por segundo

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]  # Criando a grade do campo do jogo

# Definindo as posições iniciais das figuras do Tetris
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)    ],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)  ],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)   ],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)   ],
               [(0, 0), (0, -1), (0, 1), (-1, -1)   ],
               [(0, 0), (0, -1), (0, 1), (1, -1)    ],
               [(0, 0), (0, -1), (0, 1), (-1, 0)    ]]

# Transformando as posições iniciais em objetos retangulares do pygame
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]

# Definindo o retângulo que representa cada bloco da figura
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

# Criando o campo do jogo como uma lista de listas
field = [[0 for i in range(W)] for j in range(H)]

# Definindo variáveis para o controle da velocidade de queda das figuras
anim_count, anim_speed, anim_limit = 0, 60, 2000

# Carregando as imagens de fundo do jogo
bg = pygame.image.load('img/bg.jpg').convert()
game_bg = pygame.image.load('img/bg2.jpg').convert()

# Carregando as fontes do jogo
main_font = pygame.font.Font('font/font.ttf', 50)
font = pygame.font.Font('font/font.ttf', 35)

# Criando os títulos do jogo
title_tetris = main_font.render('TETRIS V2', True, pygame.Color('darkorange'))
title_score = font.render('PONTOS:', True, pygame.Color('green'))
title_record = font.render('MELHOR:', True, pygame.Color('red'))

#constantes das posicoes dos titulos
POS_TITLE_GAME_X = 435
POS_TITLE_GAME_Y = 10

POS_TITLE_SCORE_X = 440 
POS_TITLE_SCORE_Y = 90 
POS_NUMBER_SCORE_X = 630 

POS_TITLE_RECORD_X = 440
POS_TITLE_RECORD_Y = 140 
POS_NUMBER_RECORD_X = 630

# CONSTANTES DE DESENHOS DAS PROXIMAS DIGURAS
SPACING_BETWEEN_BLOCKS = 4
POS_NEXT_FIGURES_X = 380
POS_NEXT_FIGURES_y = 250
QTTY_FIGURES_SHOW = 3

# Definindo uma função para obter uma cor aleatória
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

# Escolhendo a figura inicial e a próxima figura
# figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
# Escolhendo as figuras iniciais e as próximas figuras
figure = deepcopy(choice(figures))
next_figures = [deepcopy(choice(figures)) for _ in range(3)]

# Escolhendo a cor inicial e a próxima cor
# color, next_color = get_color(), get_color()
color = get_color()
next_colors = [get_color() for _ in range(3)]

# Inicializando a pontuação e o número de linhas removidas
score, lines = 0, 0

# Definindo a pontuação recebida por remover linhas
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

# Definindo uma função para verificar se uma figura está dentro dos limites do campo do jogo e não está sobrepondo outras figuras
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

# Definindo uma função para obter o recorde atual do arquivo salvo
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')

# Definindo uma função para salvar o recorde no arquivo
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

# Iniciando o laço principal do jogo
while True:
    # Recuperando o recorde atual
    record = get_record()

    # Inicializando as variáveis de movimento e rotação
    dx, rotate = 0, False

    # Desenhando o fundo do jogo
    sc.fill((0, 0, 0))  # Preencha a superfície com preto (ou qualquer outra cor de fundo)
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))

    # Controlando o atraso para as linhas completas
    for i in range(lines):
        pygame.time.wait(200)

    # Processando os eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Se o evento for sair do jogo, encerre o jogo
            exit()
        if event.type == pygame.KEYDOWN:  # Se o evento for uma tecla sendo pressionada
            if event.key == pygame.K_LEFT:  # Se a tecla for a seta para a esquerda, mova a figura para a esquerda
                dx = -1
            elif event.key == pygame.K_RIGHT:  # Se a tecla for a seta para a direita, mova a figura para a direita
                dx = 1
            elif event.key == pygame.K_DOWN:  # Se a tecla for a seta para baixo, acelere a queda da figura
                anim_limit = 100
            elif event.key == pygame.K_UP:  # Se a tecla for a seta para cima, rotacione a figura
                rotate = True

    # Movendo a figura no eixo x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # Movendo a figura no eixo y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figures.pop(0), next_colors.pop(0)
                next_figures.append(deepcopy(choice(figures)))
                next_colors.append(get_color())
                anim_limit = 2000
                break

    # Rotacionando a figura
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # Verificando as linhas completas
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Computando a pontuação
    score += scores[lines]

    # Desenhando a grade
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Desenhando a figura
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)

    # Desenhando o campo
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)


    # Desenhando as proximas figuras:
    for n in range(QTTY_FIGURES_SHOW):
        for i in range(4):
            if n == 1:
                figure_rect.x = next_figures[n][i].x * TILE + POS_NEXT_FIGURES_X - 10
            elif n == 2:
                figure_rect.x = next_figures[n][i].x * TILE + POS_NEXT_FIGURES_X + 50
            else:
                figure_rect.x = next_figures[n][i].x * TILE + POS_NEXT_FIGURES_X

            figure_rect.y = next_figures[n][i].y * TILE + POS_NEXT_FIGURES_y + (n * TILE * SPACING_BETWEEN_BLOCKS)  # Ajusta a posicao y para cada figura, com um espaçamento de 5 blocos
            pygame.draw.rect(sc, next_colors[n], figure_rect)

    # desenha os titulos e sistemas de pontuacao do jogo
    sc.blit(title_tetris, (POS_TITLE_GAME_X, POS_TITLE_GAME_Y))
    sc.blit(title_score, (POS_TITLE_SCORE_X, POS_TITLE_SCORE_Y))
    sc.blit(font.render(str(score), True, pygame.Color('White')), (POS_NUMBER_SCORE_X, POS_TITLE_SCORE_Y))
    sc.blit(title_record, (POS_TITLE_RECORD_X, POS_TITLE_RECORD_Y))
    sc.blit(font.render(str(score), True, pygame.Color('White')), (POS_NUMBER_RECORD_X, POS_TITLE_RECORD_Y))

    # Game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(FPS)

    pygame.display.flip()  # Atualizando a janela do jogo
    clock.tick(FPS)  # Controlando a taxa de quadros por segundo
    dx, rotate = 0, False  # Redefinindo as variáveis de movimento e rotação

# Esse é um código completo para um jogo Tetris. Se houver partes do código que foram modificadas e você deseja verificá-las, por favor, forneça essas partes específicas para que eu possa ajudar de maneira mais eficaz.
