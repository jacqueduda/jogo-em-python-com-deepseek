import pygame
import time
import random

# Inicialização do Pygame
pygame.init()

# Definição de cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# Configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo da Cobrinha')

# Relógio para controlar a velocidade do jogo
relogio = pygame.time.Clock()

# Tamanho do bloco da cobrinha e velocidade
tamanho_bloco = 20
velocidade_cobra = 15

# Fontes para mensagens
fonte_pontuacao = pygame.font.SysFont("comicsansms", 35)
fonte_mensagem = pygame.font.SysFont("bahnschrift", 50)

def mostrar_pontuacao(pontuacao):
    """Mostra a pontuação atual na tela"""
    valor = fonte_pontuacao.render("Pontuação: " + str(pontuacao), True, azul)
    tela.blit(valor, [10, 10])

def desenhar_cobra(tamanho_bloco, lista_cobra):
    """Desenha a cobra na tela"""
    for bloco in lista_cobra:
        pygame.draw.rect(tela, verde, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

def mensagem(msg, cor):
    """Exibe uma mensagem na tela (usada para game over e reinício)"""
    texto = fonte_mensagem.render(msg, True, cor)
    tela.blit(texto, [largura_tela / 6, altura_tela / 3])

def jogo():
    """Função principal que roda o jogo"""
    
    game_over = False
    game_close = False
    
    # Posição inicial da cobra
    x1 = largura_tela / 2
    y1 = altura_tela / 2
    
    # Mudança de posição inicial
    x1_mudanca = 0
    y1_mudanca = 0
    
    # Corpo da cobra (lista de coordenadas)
    lista_cobra = []
    comprimento_cobra = 1
    
    # Posição da comida
    comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / 20.0) * 20.0
    
    while not game_over:
        
        while game_close:
            # Tela de game over
            tela.fill(branco)
            mensagem("Game Over! Pressione Q-Sair ou C-Jogar", vermelho)
            mostrar_pontuacao(comprimento_cobra - 1)
            pygame.display.update()
            
            # Opções para o jogador após game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        jogo()  # Reinicia o jogo
        
        # Controles do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_mudanca == 0:  # Evita movimento inverso
                    x1_mudanca = -tamanho_bloco
                    y1_mudanca = 0
                elif event.key == pygame.K_RIGHT and x1_mudanca == 0:
                    x1_mudanca = tamanho_bloco
                    y1_mudanca = 0
                elif event.key == pygame.K_UP and y1_mudanca == 0:
                    y1_mudanca = -tamanho_bloco
                    x1_mudanca = 0
                elif event.key == pygame.K_DOWN and y1_mudanca == 0:
                    y1_mudanca = tamanho_bloco
                    x1_mudanca = 0
        
        # Verifica se a cobra bateu na parede
        if x1 >= largura_tela or x1 < 0 or y1 >= altura_tela or y1 < 0:
            game_close = True
        
        # Atualiza a posição da cobra
        x1 += x1_mudanca
        y1 += y1_mudanca
        tela.fill(preto)
        
        # Desenha a comida
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        
        # Atualiza o corpo da cobra
        cabeca_cobra = []
        cabeca_cobra.append(x1)
        cabeca_cobra.append(y1)
        lista_cobra.append(cabeca_cobra)
        
        # Mantém o tamanho correto da cobra
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]
        
        # Verifica se a cobra bateu em si mesma
        for bloco in lista_cobra[:-1]:
            if bloco == cabeca_cobra:
                game_close = True
        
        # Desenha a cobra e atualiza a pontuação
        desenhar_cobra(tamanho_bloco, lista_cobra)
        mostrar_pontuacao(comprimento_cobra - 1)
        
        pygame.display.update()
        
        # Verifica se a cobra comeu a comida
        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura_tela - tamanho_bloco) / 20.0) * 20.0
            comida_y = round(random.randrange(0, altura_tela - tamanho_bloco) / 20.0) * 20.0
            comprimento_cobra += 1
        
        # Controla a velocidade do jogo
        relogio.tick(velocidade_cobra)
    
    pygame.quit()
    quit()

# Inicia o jogo
jogo()