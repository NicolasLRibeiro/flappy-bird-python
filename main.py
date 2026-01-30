# Jogo desenvolvido por: Nicolas Lourenço
# Projeto faculdade em Python utilizando Pygame
# Jogo inspirado no Flappy Bird

import pygame
import sys
import random

# Inicialização
pygame.init()

# Tela
LARGURA = 400
ALTURA = 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird - Nicolas Lourenço")
clock = pygame.time.Clock()

# Cores
FUNDO_NOITE = (10, 10, 30)
AMARELO = (255, 220, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
LARANJA = (255, 140, 0)
VERMELHO = (200, 0, 0)

# Fonte
fonte = pygame.font.SysFont("Arial", 28)
fonte_grande = pygame.font.SysFont("Arial", 36)

# Sons
som_pulo = pygame.mixer.Sound("assets/som_pulo.wav")
som_batida = pygame.mixer.Sound("assets/som_batida.wav")

# Configurações do pássaro
bird_x = 100
bird_raio = 15
pulo = -10
velocidade_cano = 4
intervalo = 1500

def resetar_jogo():
    return {
        "bird_y": 300,
        "gravidade": 0,
        "obstaculos": [],
        "ultimo_obstaculo": pygame.time.get_ticks(),
        "pontos": 0,
        "game_over": False
    }

estado = resetar_jogo()

def criar_obstaculo():
    altura = random.randint(150, 400)
    gap = 150
    topo = pygame.Rect(LARGURA, 0, 50, altura)
    base = pygame.Rect(LARGURA, altura + gap, 50, ALTURA)
    return topo, base

def desenhar_passaro(x, y):
    # Corpo
    pygame.draw.circle(screen, AMARELO, (x, y), bird_raio)

    # Olho
    pygame.draw.circle(screen, BRANCO, (x + 6, y - 4), 4)
    pygame.draw.circle(screen, PRETO, (x + 7, y - 4), 2)

    # Bico (lado correto)
    pygame.draw.polygon(
        screen,
        LARANJA,
        [(x + 22, y), (x + 14, y - 5), (x + 14, y + 5)]
    )

    # Asa
    pygame.draw.ellipse(
        screen,
        (230, 200, 0),
        (x - 10, y, 14, 8)
    )

# Loop principal
rodando = True
while rodando:
    clock.tick(60)
    screen.fill(FUNDO_NOITE)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if not estado["game_over"] and evento.key == pygame.K_SPACE:
                estado["gravidade"] = pulo
                som_pulo.play()

            if estado["game_over"]:
                if evento.key == pygame.K_s:
                    estado = resetar_jogo()
                if evento.key == pygame.K_n:
                    rodando = False

    if not estado["game_over"]:
        # Física do pássaro
        estado["gravidade"] += 0.5
        estado["bird_y"] += int(estado["gravidade"])

        # Criar obstáculos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - estado["ultimo_obstaculo"] > intervalo:
            estado["obstaculos"].extend(criar_obstaculo())
            estado["ultimo_obstaculo"] = tempo_atual

        # Movimento dos canos
        for obstaculo in list(estado["obstaculos"]):
            obstaculo.x -= velocidade_cano

            if obstaculo.x + obstaculo.width < 0:
                estado["obstaculos"].remove(obstaculo)
                estado["pontos"] += 0.5

        # Colisão
        bird_rect = pygame.Rect(
            bird_x - bird_raio,
            estado["bird_y"] - bird_raio,
            bird_raio * 2,
            bird_raio * 2
        )

        for obstaculo in estado["obstaculos"]:
            if bird_rect.colliderect(obstaculo):
                som_batida.play()
                estado["game_over"] = True

        if estado["bird_y"] > ALTURA or estado["bird_y"] < 0:
            som_batida.play()
            estado["game_over"] = True

    # Desenhos
    desenhar_passaro(bird_x, estado["bird_y"])

    for obstaculo in estado["obstaculos"]:
        pygame.draw.rect(screen, VERMELHO, obstaculo)

    texto = fonte.render(f"Pontos: {int(estado['pontos'])}", True, BRANCO)
    screen.blit(texto, (10, 10))

    if estado["game_over"]:
        msg = fonte_grande.render("Jogar novamente?", True, BRANCO)
        opcao = fonte.render("S = Sim   N = Não", True, BRANCO)
        screen.blit(msg, (80, 260))
        screen.blit(opcao, (110, 310))

    pygame.display.flip()

pygame.quit()
sys.exit()
