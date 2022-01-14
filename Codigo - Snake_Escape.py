# Jogo 1º Semestre - Snake Escape - Grupo 7
#
#           Alan Marques da Silva
#          Guilherme Rocha Pedrina
#       Josué Eduardo Menezes Junior
#--------------------------------------------


import pygame, sys
from random import randint
from pygame.locals import *
 
pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()

#Cores
branco = (255,255,255)
vermelho = (255,0,0)
amarelo = (255,255,0)

#Outras variáveis
larguraTela = 1000
alturaTela = 700
vel = 25
delayJogo = 100
pausado = False
tut = True           
espera1 = True
espera2 = True
delayFrutaDourada = randint(20,40)*1000
removeFrutaDourada = None
delayFrutaNegra = randint(20,30)*1000
removeFrutaNegra = None
delayRato = randint(10,15)*1000
removeRato = None
cima = (0,-vel)
baixo = (0,vel)
esquerda = (-vel,0)
direita = (vel,0)
soundOn = True
efeitoSonOn = True
vel_anima = 0.5
animaFV = animaFD = animaFP = animaRato = 0
corcobra = 1
x = randint(0,500)
y = randint(0,500)


#Lê o arquivo com os melhores placares
arq = open("dadosCobra.txt", "r")
aux = arq.readline().strip()
hiScores = aux.split('|')
for x in range(len(hiScores)):
    hiScores[x] = int(hiScores[x])
arq.close()

# Carrega os spirtes da cobra com a cor escolhida pelo jogador
def CorCobra():
    cobraint = []
    if corcobra == 1:
        CobraInteira = pygame.image.load("Imagens\CobraInteira.png")
    elif corcobra == 2:
        CobraInteira = pygame.image.load("Imagens\CobraInteiraAma.png")
    elif corcobra == 3:
        CobraInteira = pygame.image.load("Imagens\CobraInteiraAzul.png")
    elif corcobra == 4:
        CobraInteira = pygame.image.load("Imagens\CobraInteiraLar.png")
    else:
        CobraInteira = pygame.image.load("Imagens\CobraInteiraRoxa.png")
    i = Xcabeça = Xcorpo = Xcauda = 0
    while i < 14:
        if i < 4:
            cabeça = CobraInteira.subsurface([Xcabeça*25,0,25,25])
            cobraint.append(cabeça)
            Xcabeça += 1
        elif i < 10:
            corpo = CobraInteira.subsurface([Xcorpo*25,25,25,25])
            cobraint.append(corpo)
            Xcorpo += 1
        else:
            linha = 50
            cauda = CobraInteira.subsurface([Xcauda*25,50,25,25])
            cobraint.append(cauda)
            Xcauda += 1
        i += 1
    cobraint = tuple(cobraint)
    return cobraint
# Índice Cobra:
# Direções Cabeça: 0 = Cima, 1 = baixo, 2 = Esquerda, 3 = Direita
# Direções Corpo: 4 = Vertical, 5 = Horizontal, 6 = Curva Cima+esquerda, 7 = Curva Baixo+Direita, 8 = Cima+Direita, 9 = Baixo+Esquerda
# Direções Cauda: 10 = Cima, 11 = Baixo, 12 = Direita, 13 = Esquerda

# Carregando sprites das frutas
todasfrutas = []
TodasFrutas = pygame.image.load("imagens\Frutas.png")
i = i2 = i3 = 0
while i < 10:
    if i < 2:
        fruta_ver = TodasFrutas.subsurface([i*25,0,25,25])
        todasfrutas.append(fruta_ver)
    elif i < 6:
        fruta_dou = TodasFrutas.subsurface([i2*25,25,25,25])
        todasfrutas.append(fruta_dou)
        i2 += 1
    else:
        fruta_pod = TodasFrutas.subsurface([i3*25,50,25,25])
        todasfrutas.append(fruta_pod)
        i3 += 1
    i += 1

#Carregando sprites do rato
rato1 = []
rato2 = []
RatoSprite = pygame.image.load("Imagens\Rato.png")
i = 0
while i < 8:
    if i <=1:
        aux = RatoSprite.subsurface([i*25,0,25,25])
        rato2.append(aux)
        aux = RatoSprite.subsurface([i*25,25,25,25])
        rato1.append(aux)
    elif i<=3:
        aux = RatoSprite.subsurface([i*25,0,25,25])
        rato1.append(aux)
        aux = RatoSprite.subsurface([i*25,25,25,25])
        rato2.append(aux)
    elif i==4 or i==7:
        aux = RatoSprite.subsurface([i*25,0,25,25])
        rato2.append(aux)
        aux = RatoSprite.subsurface([i*25,25,25,25])
        rato2.append(aux)
    else:
        aux = RatoSprite.subsurface([i*25,0,25,25])
        rato1.append(aux)
        aux = RatoSprite.subsurface([i*25,25,25,25])
        rato1.append(aux)
    i += 1

#Preparando para as Animações
fruta_vermelha = (todasfrutas[0],todasfrutas[1])
fruta_dourada = (todasfrutas[2],todasfrutas[3],todasfrutas[4],todasfrutas[5])
fruta_podre = (todasfrutas[6],todasfrutas[7],todasfrutas[8],todasfrutas[9])

rato_baixo1 = (rato1[0],rato1[1])
rato_baixo2 = (rato2[0],rato2[1])
rato_cima1 = (rato1[2],rato1[3])
rato_cima2 = (rato2[2],rato2[3])
rato_direita1 = (rato1[4],rato1[5])
rato_direita2 = (rato2[4],rato2[5])
rato_esquerda1 = (rato1[6],rato1[7])
rato_esquerda2 = (rato2[6],rato2[7])

#Carregando botões
botoes = []
todosbotoes = pygame.image.load("Menus\Botões.png")
i = i2 = i3 = 0
while i < 8:
    if i < 2:
        tela_ini = todosbotoes.subsurface([i*175,0,175,75])
        botoes.append(tela_ini)
    elif i < 5:
        mus = todosbotoes.subsurface([i2*78,75,78,76])
        botoes.append(mus)
        i2 += 1
    else:
        effects = todosbotoes.subsurface([i3*78,151,78,74])
        botoes.append(effects)
        i3 += 1
    i += 1
botoes = tuple(botoes)
# Índice Botões:
# 0 = Começar, 1 = Sair
# 2 = Pausa - Musica ligada,  3 = Música desligada,
# 5 = Pausa - Efeitos ligados, 6 = Efeitos desligados,
# 4 = Menu - Musica desligada, 7 = Efeitos desligados

# Cabeça da cobra na tela de tutorial
cores = []
CabCores = pygame.image.load("Menus\IndicaCores.png")
i = 0
while i < 5:
    tal_cor = CabCores.subsurface([i*100,0,100,70])
    cores.append(tal_cor)
    i += 1
cores = tuple(cores)


#Carregando os menus
menu = pygame.image.load("Menus\Menu.png")
telaPlacar = pygame.image.load("Menus\Placar.png")
tutorial = pygame.image.load("Menus\Tutorial.png")
fdj1 = pygame.image.load("Menus\FDJCorpo.png")
fdj2 = pygame.image.load("Menus\FDJPodre.png")
pausa = pygame.image.load("Menus\Pausa.png")

#Carregando o cenário
cen1 = pygame.image.load("Imagens\Mapa.png")
semvida = pygame.image.load("Imagens\SemVida.png")

#Sons
mordida = pygame.mixer.Sound("Sons\SomMordida.trimmer")
comer = pygame.mixer.Sound("Sons\SomMordidaDourada.mp3")
comerpodre = pygame.mixer.Sound("Sons\SomMordidaPodre.mp3")
macaDourada = pygame.mixer.Sound("Sons\SomMaça2Surge.mp3")
macaPodre = pygame.mixer.Sound("Sons\SomMaça3Surge.mp3")
Srato = pygame.mixer.Sound("Sons\Rato.trimmer")
GameOver = pygame.mixer.Sound("Sons\FimJG.trimmer")
ClickB = pygame.mixer.Sound("Sons\ClickB.trimmer")

#Fontes
pygame.font.init()
fonte = pygame.font.SysFont("Verdana", 35)
fontePequena = pygame.font.SysFont("Verdana", 20)
 
#Criando a tela 
tela = pygame.display.set_mode((larguraTela,alturaTela))
pygame.display.set_caption("Snake Escape")
logo = pygame.image.load("Imagens\Icone.png")
pygame.display.set_icon(logo)

class Fruta(pygame.sprite.Sprite):
      def __init__(self, imagem):
        super().__init__() 
        self.image = imagem
        self.rect = self.image.get_rect()
        
class Cabeca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = cobraint[3]
        self.rect = self.image.get_rect()
        self.rect.topleft = (larguraTela/2, alturaTela/2)
        self.posicaoAnt = 0
        self.direcao = (vel,0)
        self.direcaoAnt = self.direcao
        
    def move(self):
        cima = (0,-vel)
        baixo = (0,vel)
        esquerda = (-vel,0)
        direita = (vel,0)
        self.direcaoAnt = self.direcao
        teclaPrecionada = pygame.key.get_pressed()
        if (teclaPrecionada[K_UP] or teclaPrecionada[K_w]) and self.direcao != baixo:
            self.direcao = cima
            self.image = cobraint[0]
        elif (teclaPrecionada[K_DOWN] or teclaPrecionada[K_s]) and self.direcao != cima:
            self.direcao = baixo
            self.image = cobraint[1]
        elif (teclaPrecionada[K_LEFT] or teclaPrecionada[K_a]) and self.direcao != direita:
            self.direcao = esquerda
            self.image = cobraint[2]
        elif (teclaPrecionada[K_RIGHT] or teclaPrecionada[K_d]) and self.direcao != esquerda:
            self.direcao = direita
            self.image = cobraint[3]
        self.posicaoAnt = self.rect.center
        self.rect.move_ip(self.direcao)
        if self.rect.left < 0:
            self.rect.right = larguraTela
        if self.rect.right > larguraTela:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = alturaTela
        if self.rect.bottom > alturaTela:
            self.rect.top = 0
        
class Corpo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = cobraint[5]
        self.rect = self.image.get_rect()
        self.posAnt = 0
        self.direcaoC = direita
        self.direcaoAntC = None

class Rato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = rato1[0]
        self.rect = self.image.get_rect()
        self.vel = 25
        self.direcaoR = 0 #0 = baixo; 2 = cima; 4 = direita; 6 = esquerda
        self.tempo = 0
        
    def ratoMove1(self, animaRato):
        if self.tempo == 0:
            sorteio = randint(1,4)
            if sorteio == 1:
                self.direcaoR = 0
                self.image = rato_baixo1[int(animaRato)]
            elif sorteio == 2:
                self.direcaoR = 2 
                self.image = rato_cima1[int(animaRato)]
            elif sorteio == 3:
                self.direcaoR = 4 
                self.image = rato_direita1[int(animaRato)]
            elif sorteio == 4:
                self.direcaoR = 6 
                self.image = rato_esquerda1[int(animaRato)]
            self.tempo = randint(3,10)
        else:
            self.tempo -= 1
        if self.direcaoR == 0:
            self.rect.move_ip(0,self.vel)
        elif self.direcaoR == 2:
            self.rect.move_ip(0,-self.vel)
        elif self.direcaoR == 4:
            self.rect.move_ip(self.vel,0)
        else:
            self.rect.move_ip(-self.vel,0)
        if self.rect.left < 0:
            self.rect.right = larguraTela
        if self.rect.right > larguraTela:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = alturaTela
        if self.rect.bottom > alturaTela:
            self.rect.top = 0

    def ratoMove2(self, R1, animaRato):
        if R1.direcaoR == 2:
            self.rect.top = R1.rect.bottom
            self.rect.left = R1.rect.left
            self.image = rato_cima2[int(animaRato)]
        elif R1.direcaoR == 0: 
            self.rect.bottom = R1.rect.top
            self.rect.left = R1.rect.left
            self.image = rato_baixo2[int(animaRato)]
        elif R1.direcaoR == 6: 
            self.rect.bottom = R1.rect.bottom
            self.rect.left = R1.rect.right
            self.image = rato_esquerda2[int(animaRato)]
        elif R1.direcaoR == 4:
            self.rect.top = R1.rect.top
            self.rect.right = R1.rect.left
            self.image = rato_direita1[int(animaRato)]

#Menu
terminou = False
fim = True
pygame.mixer.music.load("Sons\MenuMusic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
while not terminou:
    if not soundOn:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    tela.blit(menu,(0,0))
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            fim = True
            terminou = True
            pygame.mixer.music.pause()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            #Se o botão sair for pressionado
            if 280 <= mouse[0] <= 455 and  575 <= mouse[1] <= 650:
                fim = True
                terminou = True
                pygame.mixer.music.pause()
                if efeitoSonOn:
                    ClickB.play()
            #Se o botão começar for pressionado    
            elif 543 <= mouse[0] <= 718 and  575 <= mouse[1] <= 650:
                fim = False
                primeiroLoop = True
                if efeitoSonOn:
                    ClickB.play()
            #Se o botão do som for pressionado
            elif 800 <= mouse[0] <= 878 and 600 <= mouse[1] <= 676:
                if soundOn:
                    soundOn = False
                else:
                    soundOn = True
            elif 900 <= mouse[0] <= 978 and 600 <= mouse[1] <= 676:
                if efeitoSonOn:
                    efeitoSonOn = False
                else:
                    efeitoSonOn = True
    if 280 <= mouse[0] <= 455 and  575 <= mouse[1] <= 650: 
        tela.blit(botoes[1], (280,575))          
    elif 543 <= mouse[0] <= 718 and  575 <= mouse[1] <= 650: 
        tela.blit(botoes[0], (543,575))
    if not soundOn:
        tela.blit(botoes[4], (800, 600))
    if not efeitoSonOn:
        tela.blit(botoes[7], (900,600))   
    pygame.display.update()
    
    #Game Loop
    while not fim:        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.pause()
                fim = True
                terminou = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pausado = True
                    tela.blit(pausa, (0,0))
                    pygame.mixer.music.pause()
                    if todos.has(R1):
                        pygame.mixer.Sound.stop(Srato)
                    if delayJogo <=50:
                        delayJogo += 50
                        vel_anima += 0.25
                        if todos.has(R1):
                            R1.vel += 13
            # Controle da velocidade da cobra
                if event.key == K_LSHIFT or event.key == K_SPACE:
                    if delayJogo >= 51:
                        delayJogo -= 50
                        vel_anima -= 0.25
                        if todos.has(R1):
                            R1.vel -= 13
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_SPACE:
                    if delayJogo < 51:
                        delayJogo += 50
                        vel_anima += 0.25
                        if todos.has(R1):
                            R1.vel += 13

        while pausado:
            mouse = pygame.mouse.get_pos() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    fim = True
                    terminou = True
                    pausado = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if soundOn:
                            pygame.mixer.music.unpause()
                        
                        pausado = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 800 <= mouse[0] <= 878 and 600 <= mouse[1] <= 676:
                        if soundOn:
                            soundOn = False
                            pygame.mixer.music.pause() 
                        else:
                            soundOn = True
                    elif 900 <= mouse[0] <= 978 and 600 <= mouse[1] <= 676:
                        if efeitoSonOn:
                            efeitoSonOn = False
                        else:
                            efeitoSonOn = True
            if soundOn:
                tela.blit(botoes[2], (800,600))
            else:
                tela.blit(botoes[3], (800, 600))   
            if efeitoSonOn:
                tela.blit(botoes[5], (900,600))
            else:
                tela.blit(botoes[6], (900,600))
            pygame.display.update()

        if primeiroLoop:
            #Apresenta a tela com o tutorial
            while tut:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        fim = True
                        terminou = True
                        tut = False
                    if event.type == MOUSEBUTTONDOWN:
                        tut = False
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load("Sons\MusicSnakk-.mp3")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.5)
                        if not soundOn:
                            pygame.mixer.music.pause()
                    if event.type == KEYUP:
                        if event.key == K_c:
                            corcobra += 1
                            if corcobra == 6:
                                corcobra = 1
                tela.blit(tutorial, (0,0))
                if corcobra == 1:
                    tela.blit(cores[0],(700, 130))
                if corcobra == 2:
                    tela.blit(cores[1],(700, 130))
                if corcobra == 3:
                    tela.blit(cores[2],(700, 130))
                if corcobra == 4:
                    tela.blit(cores[3],(700, 130))
                if corcobra == 5:
                    tela.blit(cores[4],(700, 130))
                pygame.display.update()
                
            #Definindo as Sprites iniciais
            cobraint = CorCobra()
            C1 = Cabeca()
            F1 = Fruta(fruta_vermelha[0])
            F1.rect.topleft = (randint(2, 37)*25, randint(2, 25)*25)
            F2 = Fruta(fruta_dourada[0])
            CO1 = Corpo()
            CO1.rect.topright = (C1.rect.left, C1.rect.top)
            CO2 = Corpo()
            CO2.rect.topright = (CO1.rect.left, CO1.rect.top)
            R1 = Rato()
            R2 = Rato()
            
            #Criando os grupos de Sprites
            cab = pygame.sprite.GroupSingle()
            cab.add(C1)
            frutas = pygame.sprite.GroupSingle()
            frutas.add(F1)
            fDourada = pygame.sprite.GroupSingle()
            fNegra = pygame.sprite.Group()
            listaFNegra = []
            corpos = pygame.sprite.Group()
            corpos.add(CO1)
            corpos.add(CO2)
            listaCorpos = [CO1, CO2]
            rat = pygame.sprite.Group()
            todos = pygame.sprite.Group()
            todos.add(C1)
            todos.add(F1)
            todos.add(CO1)
            todos.add(CO2)

            #Redefinindo as variáveis do jogo
            tut = True
            pontuacao = 0
            vidas = 3
            delayJogo = 100
            soltaFrutaDourada = pygame.time.get_ticks()
            soltaFrutaNegra = pygame.time.get_ticks()
            soltaRato = pygame.time.get_ticks()
            delayRato = randint(10,15)*1000
            primeiroLoop = False        
        
        # Animações Frutas
        animaFV = animaFV + vel_anima
        if animaFV > 1.999:
            animaFV = 0
        F1.image = fruta_vermelha[int(animaFV)]

        animaFD = animaFD + vel_anima
        if animaFD > 3.999:
            animaFD = 0
        F2.image = fruta_dourada[int(animaFD)]
        
        animaFP = animaFP + vel_anima
        if animaFP > 3.999:
            animaFP = 0
        if len(listaFNegra) != 0:
            for f in listaFNegra: 
                f.image = fruta_podre[int(animaFP)]
        
        #Começa a preparação para soltar a fruta dourada
        if soltaFrutaDourada:
            tempoFrutaDourada = pygame.time.get_ticks() - soltaFrutaDourada
            if tempoFrutaDourada >= delayFrutaDourada:
                flag = True
                while flag:
                    F2.rect.topleft = (randint(2, 37)*25, randint(2, 25)*25)
                    if not (pygame.sprite.spritecollideany(F2,cab) or pygame.sprite.spritecollideany(F2,corpos) or pygame.sprite.spritecollideany(F2,fNegra) or pygame.sprite.spritecollideany(F2,frutas)):
                        flag = False
                fDourada.add(F2)            
                todos.add(F2)
                if efeitoSonOn:
                    macaDourada.play()
                soltaFrutaDourada = None
                tempoFrutaDourada = None
                delayFrutaDourada = randint(20,40)*1000
                removeFrutaDourada = pygame.time.get_ticks()

        #Se a fruta dourada foi gerada
        if removeFrutaDourada:
            tempoRemoveFrutaDourada = pygame.time.get_ticks() - removeFrutaDourada
            # Remove a fruta depois de 5 segs se necessário e zera os contadores
            if tempoRemoveFrutaDourada >= 5000:
                if todos.has(F2):
                    F2.kill()
                    removeFrutaDourada = None
                    tempoRemoveFrutaDourada = None
                    soltaFrutaDourada = pygame.time.get_ticks()
        
        #Começa a preparação para soltar a fruta negra
        if soltaFrutaNegra:
            tempoFrutaNegra = pygame.time.get_ticks() - soltaFrutaNegra
            if tempoFrutaNegra >= delayFrutaNegra:
                for i in range (10):
                    listaFNegra.append(Fruta(fruta_podre[0]))
                    fNegra.add(listaFNegra[-1])            
                    todos.add(listaFNegra[-1])
                    flag = True
                    while flag:
                        listaFNegra[-1].rect.topleft = (randint(2, 37)*25, randint(2, 25)*25)
                        if not (pygame.sprite.spritecollideany(listaFNegra[-1],cab) or pygame.sprite.spritecollideany(listaFNegra[-1],corpos) or pygame.sprite.spritecollideany(listaFNegra[-1],frutas) or pygame.sprite.spritecollideany(listaFNegra[-1],fDourada)):
                            flag = False
                    if efeitoSonOn:
                        macaPodre.play()
                soltaFrutaNegra = None
                tempoFrutaNegra = None
                delayFrutaNegra = randint(5,10)*1000
                removeFrutaNegra = pygame.time.get_ticks()

        #Se a fruta negra foi gerada
        if removeFrutaNegra:
            tempoRemoveFrutaNegra = pygame.time.get_ticks() - removeFrutaNegra
            # Remove a fruta depois de 10 segs se necessário e zera os contadores
            if tempoRemoveFrutaNegra >= 10000:
                while len(listaFNegra) != 0:
                    listaFNegra[-1].kill()
                    listaFNegra.pop()
                removeFrutaNegra = None
                tempoRemoveFrutaNegra = None
                soltaFrutaNegra = pygame.time.get_ticks()
        
        #Começa a preparação para soltar o rato
        if soltaRato:
            tempoRato = pygame.time.get_ticks() - soltaRato
            if tempoRato >= delayRato:
                flag = True
                while flag:
                    R1.rect.topleft = (randint(2, 37)*25, randint(2, 25)*25)
                    if not (pygame.sprite.spritecollideany(R1,cab) or pygame.sprite.spritecollideany(R1,corpos) or pygame.sprite.spritecollideany(R1,fNegra) or pygame.sprite.spritecollideany(R1,frutas) or pygame.sprite.spritecollideany(R1,fDourada)):
                        flag = False
                R2.rect.bottom = R1.rect.top
                R2.rect.left = R1.rect.left
                R2.image = rato2[0]
                rat.add(R1)
                rat.add(R2)            
                todos.add(R1)
                todos.add(R2)
                if delayJogo >= 51:
                    R1.vel = 25
                else:
                    R1.vel = 12
                if efeitoSonOn:
                    macaDourada.play()
                    Srato.play()
                soltaRato = None
                tempoRato = None
                delayRato = randint(30,40)*1000
                removeRato = pygame.time.get_ticks()
        
        #Move somente a cabeça
        C1.move()    
        
        #Se o rato foi gerado
        if removeRato:
            tempoRemoveRato = pygame.time.get_ticks() - removeRato
            R1.ratoMove1(animaRato)
            R2.ratoMove2(R1,animaRato)
            # Remove o rato depois de 10 segs se necessário e zera os contadores
            if tempoRemoveRato >= 10000:
                if todos.has(R1):
                    R1.kill()
                    R2.kill()
                    removeRato = None
                    tempoRemoveRato = None
                    soltaRato = pygame.time.get_ticks()
                    pygame.mixer.Sound.stop(Srato)
            #Se o rato colidir com algo diferente da cabeça
            if pygame.sprite.spritecollideany(R1,corpos) or pygame.sprite.spritecollideany(R1,fNegra) or pygame.sprite.spritecollideany(R1,frutas) or pygame.sprite.spritecollideany(R1,fDourada):
                if R1.direcaoR == 2:   #0 = baixo; 2 = cima; 4 = direita; 6 = esquerda
                    R1.direcaoR = 0
                    R1.image = rato_baixo1[int(animaRato)]
                    R2.rect.bottom = R1.rect.top
                    R2.rect.left = R1.rect.left
                    R2.image = rato_baixo2[int(animaRato)]
                elif R1.direcaoR == 0:
                    R1.direcaoR = 2
                    R1.image = rato_cima1[int(animaRato)]
                    R2.rect.top = R1.rect.bottom
                    R2.rect.left = R1.rect.left
                    R2.image = rato_cima2[int(animaRato)]
                elif R1.direcaoR == 4:
                    R1.direcaoR = 6
                    R1.image = rato_esquerda1[int(animaRato)]
                    R2.rect.left = R1.rect.right
                    R2.rect.top = R1.rect.top
                    R2.image = rato_esquerda2[int(animaRato)]
                elif R1.direcaoR == 6:
                    R1.direcaoR = 4
                    R1.image = rato_direita1[int(animaRato)]
                    R2.rect.right = R1.rect.left
                    R2.rect.top = R1.rect.top
                    R2.image = rato_direita2[int(animaRato)]
                R1.tempo += 3
                R1.ratoMove1(animaRato)
                R1.ratoMove1(animaRato)
                R2.ratoMove2(R1, animaRato)
                R2.ratoMove2(R1, animaRato)
        
        #Animações Rato
        animaRato = animaRato + vel_anima
        if animaRato > 1.999:
            animaRato = 0
        if R1.direcaoR == 0:
            R1.image = rato_baixo1[int(animaRato)]
            R2.image = rato_baixo2[int(animaRato)]           
        elif R1.direcaoR == 2:
            R1.image = rato_cima1[int(animaRato)]
            R2.image = rato_cima2[int(animaRato)]
        elif R1.direcaoR == 4:
            R1.image = rato_direita1[int(animaRato)]
            R2.image = rato_direita2[int(animaRato)]
        else:
            R1.image = rato_esquerda1[int(animaRato)]
            R2.image = rato_esquerda2[int(animaRato)]
        
        #Se a cabeça colidir com a fruta vermelha
        if pygame.sprite.spritecollideany(C1, frutas):
            pontuacao+=10
            delayJogo-=0.1
            if efeitoSonOn:
                mordida.play()
            #impede que uma fruta seja gerada em uma posição indevida
            flag = True
            while flag:
                F1.rect.topleft = (randint(2, 37)*25, randint(2, 25)*25)
                if not (F1.rect.center == C1.posicaoAnt or pygame.sprite.spritecollideany(F1,cab) or pygame.sprite.spritecollideany(F1,corpos) or pygame.sprite.spritecollideany(F1,fNegra) or pygame.sprite.spritecollideany(F1,fDourada)):
                    flag = False
            listaCorpos.append(Corpo())
            listaCorpos[-1].rect.center = listaCorpos[-2].posAnt
            corpos.add(listaCorpos[-1])
            todos.add(listaCorpos[-1])
            
        #Caso a cabeça colida com a fruta Dourada
        if pygame.sprite.spritecollideany(C1, fDourada):
            pontuacao += 50
            delayJogo-=0.5
            if efeitoSonOn:
                comer.play()
            F2.kill()
            removeFrutaDourada = None
            tempoRemoveFrutaDourada = None
            soltaFrutaDourada = pygame.time.get_ticks()
            for i in range (5):
                listaCorpos.append(Corpo())
                listaCorpos[-1].rect.center = (listaCorpos[-2].posAnt)
                listaCorpos[-1].posAnt = listaCorpos[-2].posAnt
                listaCorpos[-1].direcaoC = listaCorpos[-2].direcaoAntC
                listaCorpos[-1].direcaoAntC = listaCorpos[-1].direcaoC
                corpos.add(listaCorpos[-1])
                todos.add(listaCorpos[-1]) 
        
        #Caso a cabeça colida com a fruta Negra
        for n in listaFNegra:
            if  n.rect.center == C1.rect.center:
                vidas-=1
                if efeitoSonOn:
                    if vidas != 0:
                        comerpodre.play()
                    else:
                        mordida.play()
                listaFNegra.remove(n)
                n.kill()
                if pontuacao >= 50:
                    pontuacao -= 50
                    delayJogo+=0.5
                    for i in range (5):
                        corpos.remove(listaCorpos[-1])
                        todos.remove(listaCorpos[-1])
                        listaCorpos.pop()
        
        #Se a cabeça colidir com o rato
        if pygame.sprite.spritecollideany(C1, rat):
            pontuacao += 100
            delayJogo -= 1
            if vidas < 3:
                vidas += 1
            if efeitoSonOn:
                comer.play()
            R1.kill()
            R2.kill()
            removeRato = None
            tempoRemoveRato = None
            soltaRato = pygame.time.get_ticks()
            pygame.mixer.Sound.stop(Srato)
            for i in range (10):
                listaCorpos.append(Corpo())
                listaCorpos[-1].rect.center = (listaCorpos[-2].posAnt)
                listaCorpos[-1].posAnt = listaCorpos[-2].posAnt
                listaCorpos[-1].direcaoC = listaCorpos[-2].direcaoAntC
                listaCorpos[-1].direcaoAntC = listaCorpos[-1].direcaoC
                corpos.add(listaCorpos[-1])
                todos.add(listaCorpos[-1])
        
        #Ajustando o corpo e a cauda
        #Atualiza a direção
        i=0
        for c in corpos:
            c.direcaoAntC = c.direcaoC
            #Se for a primeira parte do corpo
            if i == 0:
                if C1.direcao != C1.direcaoAnt:
                    c.direcaoC = (C1.direcaoAnt, C1.direcao)
                else:
                    c.direcaoC = C1.direcaoAnt
                c.posAnt = c.rect.center
                c.rect.center = C1.posicaoAnt
                
            #As outras partes
            else:
                c.direcaoC = listaCorpos[i-1].direcaoAntC
                c.posAnt = c.rect.center
                c.rect.center = listaCorpos[i-1].posAnt
            
            #Atualiza as imagens com base nas direções
            
            #Se não for a cauda
            if i != len(corpos)-1:
                if c.direcaoC == direita or c.direcaoC == esquerda:
                    c.image = cobraint[5]
                elif c.direcaoC == cima or c.direcaoC == baixo:
                    c.image = cobraint[4]
                elif c.direcaoC == (cima, direita) or c.direcaoC == (esquerda, baixo):
                    c.image = cobraint[7]
                elif c.direcaoC == (cima, esquerda) or c.direcaoC == (direita, baixo):
                    c.image = cobraint[9]
                elif c.direcaoC == (baixo, esquerda) or c.direcaoC == (direita, cima):
                    c.image = cobraint[6]
                else:
                    c.image = cobraint[8]
            #Se for a cauda
            else:
                if c.direcaoC == direita or c.direcaoC == (cima, direita) or c.direcaoC == (baixo, direita):
                    c.image = cobraint[12]
                elif c.direcaoC == esquerda or c.direcaoC == (cima, esquerda) or c.direcaoC == (baixo, esquerda):
                    c.image = cobraint[13]
                elif c.direcaoC == cima or c.direcaoC == (esquerda, cima) or c.direcaoC == (direita, cima):
                    c.image = cobraint[10]
                else:
                    c.image = cobraint[11]
            i+=1

        #Caso a cabeça colida com o corpo ou vidas se esgotem
        if pygame.sprite.spritecollideany(C1, corpos) or vidas == 0:
            if todos.has(R1):
                pygame.mixer.Sound.stop(Srato)
            pontuacaoJogo = pontuacao
            hiScores.append(pontuacao)
            hiScores.sort(reverse=True)
            if efeitoSonOn:
                GameOver.play()
            pygame.mixer.music.unload()
            if not soundOn:
                pygame.mixer.music.pause()
            if len(hiScores) > 10:
                hiScores.pop()
            #Salva os novos placares no arquivo
            arq = open("dadosCobra.txt", "w")
            for i in range (len(hiScores)-1):
                arq.write("{}|".format(hiScores[i]))
            arq.write("{}".format(hiScores[-1]))
            arq.close() 
            #Dsesnhando os corações
            tela.blit(semvida,(75,34))
            tela.blit(semvida,(45,34))
            tela.blit(semvida,(15,34))           
            #Desenha uma imagem diferente dependendo de como o jogo terminou
            if vidas == 0:
                tela.blit(fdj2,(0,0))
            else:
                tela.blit(fdj1, (0,0))
            pygame.display.update()
            for t in todos:
                t.kill() 
            #Espera um clique do mouse para ir para a próxima tela
            while espera1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        fim = True
                        terminou = True
                        espera1 = False
                        espera2 = False
                    if event.type == MOUSEBUTTONDOWN:
                        espera1 = False
            espera1 = True
            #Desenha a tela com os maiores placares
            tela.blit(telaPlacar, (0,0))
            if soundOn:
                pygame.mixer.music.load("Sons\MenuMusic.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
            for i in range (len(hiScores)):
                if hiScores[i] != pontuacaoJogo:
                    aux = fonte.render("{}. {}".format(str(i+1), hiScores[i]), True, amarelo)
                else:
                    aux = fonte.render("{}. {}".format(str(i+1), hiScores[i]), True, vermelho) 
                rectAux = aux.get_rect()
                rectAux.centerx = tela.get_rect().centerx
                rectAux.centery = 152 + 41*i
                tela.blit(aux,rectAux)
            pygame.display.update()
            #Espera o clique do mouse para sair da tela dos placares e reiniciar o jogo
            while espera2:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        fim = True
                        terminou = True
                        espera2 = False
                    if event.type == MOUSEBUTTONDOWN:
                        espera2 = False
            espera2 = True
            fim = True
            
        #Desenho da tela
        if not fim:
            tela.blit(cen1, (0,0))
            if vidas <= 2:
                tela.blit(semvida,(75,34))
            if vidas <= 1:
                tela.blit(semvida,(45,34))
            placar = fontePequena.render(str(pontuacao), True, amarelo)
            tela.blit(placar, (15,8))
            for t in todos:
                tela.blit(t.image, t.rect)
            pygame.display.update()        
        FramePerSec.tick(FPS)
        pygame.time.delay(int(delayJogo))
pygame.display.quit()
print("Fim do programa")
sys.exit()


