import pygame, sys
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

class Cita:
        scena = 0
        limite_scenas = 3
        
        font = pygame.font.Font(None,50)

        def __init__(self, window_size, waifu):  # construye un nuevo objeto con nuevas variables.
                self.window_size = window_size
                self.resultado = []
                self.boton = pygame.transform.scale(pygame.image.load('imagenes/boton.jpg'), (window_size[0]-200, 40))
                self.texto = pygame.transform.scale(pygame.image.load('imagenes/texto.jpg'), (window_size[0]-200, 40))

                self.waifu = waifu['personaje']

                self.dialogo = waifu['dialogo']
                self.opciones = waifu['opciones']

                self.respuestas = waifu['respuestas']
                
                self.colliders = [
                                pygame.Rect(100,450,window_size[0] - 200,40),
                                pygame.Rect(100,500,window_size[0] - 200,40),
                                pygame.Rect(100,550,window_size[0] - 200,40),
                                 ]

                self.imagenes = []
                for img in waifu['imagenes']:
                        self.imagenes.append(pygame.transform.scale(pygame.image.load(img), window_size))

                self.update()

        def select_option(self, event, click):
                if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(len(self.colliders)):
                                if event.button == 1 and self.colliders[i].collidepoint(event.pos):
                                        self.resultado.append(self.respuestas[self.scena][i])
                                        self.scena += 1
                                        click.play()
                                        if self.scena < self.limite_scenas:
                                                self.update()
                
        def update_scenas(self, screen):
                if self.scena < self.limite_scenas:
                        self.mostrar_scenas(screen)
                        return False
                else:
                        return True
                                
        def mostrar_scenas(self, screen):
                screen.blit(self.imagenes[self.scena], (0,0))
                
                screen.blit(self.texto, (100,400))
                screen.blit(self.message, (110, 405))
                
                screen.blit(self.boton, (100,450))
                screen.blit(self.botones[0], (110, 455))
                
                screen.blit(self.boton, (100,500))
                screen.blit(self.botones[1], (110, 505))
                
                screen.blit(self.boton, (100,550))
                screen.blit(self.botones[2], (110,555))

        def update(self):
                self.message = self.font.render(self.dialogo[self.scena],1,(0,0,0))
                self.botones = []
                for i in range(3):
                        self.botones.append(self.font.render(self.opciones[self.scena][i],1,(0,0,0)))
                        
        def __str__(self):
                return str(int((sum(self.resultado)/len(self.resultado))*100)) + "%"

class Game:
        clock = pygame.time.Clock()
        WINDOW_SIZE = (1200,600)
        screen = pygame.display.set_mode(WINDOW_SIZE)
        data = []

        fondo = pygame.transform.scale(pygame.image.load('imagenes/fondo.jpg'), WINDOW_SIZE)

        pygame.mixer.music.load('musica/fondo.mp3')
        pygame.mixer.music.play(loops=-1)

        click = pygame.mixer.Sound("musica/click.mp3")

        def run_game(self):
                waifu_1, waifu_2 = random.choices(self.data, k=2)
                while id(waifu_1) == id(waifu_2):
                        waifu_1, waifu_2 = random.choices(self.data, k=2)
                        
                cita_1 = Cita(self.WINDOW_SIZE, waifu_1)
                cita_2 = Cita(self.WINDOW_SIZE, waifu_2)
                self.citas = [cita_1, cita_2]

                actual = 0
                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        self.exit_game()
                                self.citas[actual].select_option(event, self.click)


                        self.screen.fill((0,0,0))

                        if self.citas[actual].update_scenas(self.screen):
                                actual += 1
                                
                        if actual == 2:
                                self.restart_game()
                        
                        pygame.display.update()
                        self.clock.tick(30)
                        
        def restart_game(self, text=' Quieres jugar de nuevo? '):
                if self.push_button(text):
                        self.run_game()
                else:
                        self.exit_game()
                        
        def push_button(self, text):

                font = pygame.font.Font(None,70)
                width = 120
                height = 150

                left = font.render(self.citas[0].__str__(), 1, (0,0,0))
                left_img = pygame.transform.scale(pygame.image.load(self.citas[0].waifu), (width, height))
                left_collider = pygame.Rect(60,400, width, height)
                left_on = False

                right = font.render(self.citas[1].__str__(), 1, (0,0,0))
                right_img = pygame.transform.scale(pygame.image.load(self.citas[1].waifu), (width, height))
                right_collider = pygame.Rect(1020,400, width, height)
                right_on = False

                midle_x, midle_y = self.WINDOW_SIZE[0]//2, self.WINDOW_SIZE[1]//2

                pos_yes = (midle_x-110, midle_y+50)
                yes = pygame.Rect(pos_yes[0], pos_yes[1], 90,50)
                message_yes = font.render('Yes', 1, (0,0,0))

                pos_no = (midle_x+20, midle_y+50)
                no = pygame.Rect(pos_no[0], pos_no[1], 90,50)
                message_no = font.render('No', 1, (0,0,0))
                
                message = font.render(text,1,(0,0,0))
                lenght = message.get_width()
                pos_msg = (midle_x//2,midle_y-40)


                acepta = pygame.transform.scale(pygame.image.load('imagenes/aceptar.png'), (80,50))
                sound_acepta = pygame.mixer.Sound("musica/acepta.mp3")
                
                rechaza = pygame.transform.scale(pygame.image.load('imagenes/rechazo.png'), (80,50))
                sound_rechazo = pygame.mixer.Sound("musica/rechazo.mp3")

                opcion = None

                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        self.exit_game()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1 and yes.collidepoint(event.pos):
                                                self.click.play()
                                                return True
                                        if event.button == 1 and no.collidepoint(event.pos):
                                                self.click.play()
                                                return False
                                        if event.button == 1 and left_collider.collidepoint(event.pos) and right_on != True and left_on != True:
                                                left_on = True
                                                if random.choice(self.citas[0].resultado):
                                                        sound_acepta.play()
                                                        opcion = acepta
                                                else:
                                                        opcion = rechaza
                                                        sound_rechazo.play()
                                        if event.button == 1 and right_collider.collidepoint(event.pos) and right_on != True and left_on != True:
                                                right_on = True
                                                if random.choice(self.citas[1].resultado):
                                                        opcion = acepta
                                                        sound_acepta.play()
                                                else:
                                                        opcion = rechaza
                                                        sound_rechazo.play()
                                        
                        self.screen.blit(self.fondo, (0,0))

                        self.screen.blit(left, (70,550))
                        self.screen.blit(left_img, (60,400))
                        if left_on:
                                self.screen.blit(opcion, (70,340))
                        
                        self.screen.blit(right, (1030,550))
                        self.screen.blit(right_img, (1020,400))
                        if right_on:
                                self.screen.blit(opcion, (1030,340))
                                                
                        pygame.draw.rect(self.screen, (255,100,0), yes)
                        self.screen.blit(message_yes, pos_yes)
                        
                        pygame.draw.rect(self.screen, (255,100,0), no)
                        self.screen.blit(message_no, pos_no)
                        
                        pygame.draw.rect(self.screen, (255,255,255), [pos_msg[0], pos_msg[1],lenght, 60])
                        self.screen.blit(message, pos_msg)
                        
                        pygame.display.update()
                        self.clock.tick(30)
                        
        def exit_game(self):
                pygame.quit()
                sys.exit()

        def set_waifus(self, data):
                self.data = data


a = {
        'dialogo':['hola ?', ' jajaja me gradas', 'casemos'],
        'opciones':[['si eto','safa','ptmr'],
                    ['vete ctmr', 'a noma', 'XD'],
                    ['no!', 'me gustaria tener 17 hijos', 'carajo']],
        'respuestas':[[ False,True, False], [True,  False, False], [False, True, False]],
        'imagenes':['imagenes/w1.png', 'imagenes/w2.png', 'imagenes/w3.png'],
        'personaje':'imagenes/w.png'
        }

b = {
        'dialogo':['yaharoo!', ' entonces estas bien ?', ' mejor llamare a la policia'],
        'opciones':[['yaharooo','oe chivola rctmr','klla kchera'],
                    ['supongo', 'a', 'a mi pichula!'],
                    ['por ser demasido guapo?', 'adios', 'naice']],
        'respuestas':[[ False,False, True], [True,  False, False], [False, True, False]],
        'imagenes':['imagenes/miku_1.png', 'imagenes/miku_2.png', 'imagenes/miku_3.png'],
        'personaje':'imagenes/miku.png'
        }

data = [a, b]


if __name__ == '__main__':
        game = Game()
        game.set_waifus(data)
        game.run_game()
