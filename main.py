import pygame, sys
import random

pygame.init()
pygame.mixer.init()

class Click:
        def __init__(self, sound = "musica/click.mp3"):
                self.click = pygame.mixer.Sound(sound)
        def play_sound(self, sonido):
                sound = pygame.mixer.Sound(sonido)
                sound.play()

class Cita(Click):
        def __init__(self, window_size, waifu):  # construye un nuevo objeto con nuevas variables.
                super().__init__()
                self.scena = 0
                self.limite_scenas = 5
                
                self.font = pygame.font.Font(None,50)
        
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

        def select_option(self, event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(len(self.colliders)):
                                if event.button == 1 and self.colliders[i].collidepoint(event.pos):
                                        self.resultado.append(self.respuestas[self.scena][i])
                                        self.scena += 1
                                        self.click.play()
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

class Game(Click):
        def __init__(self, data):
                super().__init__()
                self.clock = pygame.time.Clock()
                self.WINDOW_SIZE = (1200,600)
                self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
                self.data = data

                self.fondo = pygame.transform.scale(pygame.image.load('imagenes/fondo.jpg'), self.WINDOW_SIZE)

                pygame.mixer.music.load('musica/fondo.mp3')
                pygame.mixer.music.play(loops=-1)

        def run_game(self):
                waifu_1, waifu_2 = self.selecionar_waifus()
                        
                cita_1 = Cita(self.WINDOW_SIZE, waifu_1)
                cita_2 = Cita(self.WINDOW_SIZE, waifu_2)
                self.citas = [cita_1, cita_2]

                actual = 0
                while True:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        self.exit_game()
                                self.citas[actual].select_option(event)


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
                sound_acepta = "musica/acepta.mp3"
                
                rechaza = pygame.transform.scale(pygame.image.load('imagenes/rechazo.png'), (80,50))
                sound_rechazo = "musica/rechazo.mp3"

                opcion = None

                while True:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
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
                                                        self.play_sound(sound_acepta)
                                                        opcion = acepta
                                                else:
                                                        opcion = rechaza
                                                        self.play_sound(sound_rechazo)
                                        if event.button == 1 and right_collider.collidepoint(event.pos) and right_on != True and left_on != True:
                                                right_on = True
                                                if random.choice(self.citas[1].resultado):
                                                        opcion = acepta
                                                        self.play_sound(sound_acepta)
                                                else:
                                                        opcion = rechaza
                                                        self.play_sound(sound_rechazo)
                                        
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

        def selecionar_waifus(self):  # recursividad
                waifu_1, waifu_2 = random.choices(self.data, k=2)
                if id(waifu_1) != id(waifu_2):
                        return waifu_1, waifu_2
                else:
                     return self.selecionar_waifus()
                        
        def exit_game(self):
                pygame.quit()
                sys.exit()

        def set_waifus(self, data):
                self.data = data

a = {
        'dialogo':[' Que hace un extraño aqui? !!! ...',
                   ' no eres un acosador verdad? !!! ...',
                   ' mejor llamare a la policia ...',
                   ' a...aaa!!!, que quieres decir?!',
                   ' hubieras empezado con eso ...'],
        'opciones':[['tú que haces aqui!','...','yo soy tu padre!'],
                    ['solo si tú lo quisieras', 'solo fue una vez!', 'y si lo fuera, qué harias?'],
                    ['por ser demasido guapo?', 'no tengo niños en el sotano!!!', 'y diles que anguien trata de robarme el corazon'],
                    ['que soy traficador de organos', 'que fui tallado por los dioses', 'quiero salir contigo!'],
                    ['me perdi en tu hermosura', 'queria ver como te ponias', 'queria invitarte un cevichito']],
        'respuestas':[[True, False, False],
                      [False,  False, True],
                      [False, False, True],
                      [False,  False, True],
                      [False, False, True]],
        'imagenes':['imagenes/itsuki_1.jpg',
                    'imagenes/itsuki_2.jpg',
                    'imagenes/itsuki_3.jpg',
                    'imagenes/itsuki_4.jpg',
                    'imagenes/itsuki_5.jpg'],
        'personaje':'imagenes/itsuki.jpg'
        }

b = {"dialogo":["¡Hola!",
                "¿Enserio crees eso?",
                "Gracias, sabes me gusta hacer deporte",
                "Genial, me gustaria hacerlo juntos algunas vez",
                "¡Maravilloso!, eres muy interesante y te pareces mucho a mi"],
        "opciones":[["¿Hola como estas?","Te ves muy linda hoy","Te queda bien ese moño"],
                    ["No, era broma","Si, combina con tu forma de vestir","Si jaja"],
                    ["A mi no, son muy agotadores","A mi tambien, en especial el futbol","Prefiero ver peliculas"],
                    ["igualmente, lo esperare con ansias","No creo que tenga tiempo","La verdad no tengo interes en eso"],
                    ["Igualmente, siento que nos llevaremos bien","No lo creo pero gracias por eso, supongo","No vemos hasta la proxima"]],
        "respuestas":[[False,False,True],
                      [False,True,False],
                      [False,True,False],
                      [True,False,False],
                      [True,False,False]],
        "imagenes":["imagenes/yotsuba_5.jpg",
                    "imagenes/yotsuba_2.jpg",
                    "imagenes/yotsuba_1.jpg",
                    "imagenes/yotsuba_4.jpg",
                    "imagenes/yotsuba_3.jpg"], 
        "personaje":"imagenes/yotsuba_ultima.jpg"
        }

c = {
        'dialogo':[' Ohayoo conero-kun',
                   ' ¿Listo para el trabajo de hoy?',
                   ' ¿Te molesta algo conero-kun?',
                   ' ¿Harás todo lo que te pida verdad?',
                   ' Muy bien denji'],
        'opciones':[['Hi?','...','Hola...'],
                    ['Si, siempre listo', 'Tendré que ir de nuevo con Power', 'Aki siempre anda molesto'],
                    ['No, todo bien', 'Esto es muy difícil', 'Trabajar con esos pendejos es un martirio'],
                    ['Siempre', 'woaff', 'Como sea'],
                    ['…', '…Gracias', 'adios makima']],
        'respuestas':[[False, True, False],
                      [True,  False, False],
                      [True, False, False],
                      [False,  True, False],
                      [False, False, True]],
        'imagenes':['imagenes/Makima1.png',
                    'imagenes/Makima2.jpg',
                    'imagenes/Makima3.png',
                    'imagenes/Makima4.png',
                    'imagenes/Makima5.png'],
        'personaje':'imagenes/Makima.png'
        }

d = {
        'dialogo':["Quien eres?",
                   "Es la primera vez que te veo",
                   "Solo te ponia a prueba",
                   "Bueno, entonces crees que podriamos salir?",
                   "Tengo cosas que hacer, luego seguimos hablando"],
        'opciones':[["Tu admirador Nº1", "Era tu amigo", "Ni yo me acuerdo"],
                    ["Tambien es mi primera vez", "Oh ya veo", "Que bueno"],
                    ["Jaja que graciosa", "Mmm bueno","Te pasas ah"],
                    ["Esta bien", "Bueno, nos vemos", "Todavia no te vayas, por favor"],
                    ["Yo creo que sí", "Claro, tu solo dime cuando", "No estoy seguro, talvez"]],
        'respuestas':[[True,False,False],
                      [False,True,False],
                      [True,False,False],
                      [False,True,False],
                      [False,True,False]],
        'imagenes':['imagenes/mai_1.png',
                    'imagenes/mai_2.png',
                    'imagenes/mai_3.png',
                    'imagenes/mai_4.png',
                    'imagenes/mai_5.png'],
        'personaje':'imagenes/mai.png'
        }

data = [a, b, c, d]


if __name__ == '__main__':
        game = Game(data)
        game.run_game()
