import pygame

ancho = 640
alto = 480

paleta = [(255, 255, 255), (0, 0, 0)]
blanco = 0
negro = 1

def sonido(nombre):
    return  pygame.mixer.Sound(nombre)

class pixel(object):
	def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
		self.r = pygame.Rect(x, y, w, h)
		self.color = c
		self.movx = 0
		self.movy = 0
		self.speed = 3

	def pinta(self, ventana):
		pygame.draw.rect(ventana, self.color, self.r)

	def mueve(self):
		self.r.move_ip(self.movx, self.movy)

	def dentro(self, rect):
		return self.r.colliderect(rect)

class pelota(pixel):
    def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
        pixel.__init__(self, x, y, w, h, c)
        self.speed = 2.5
        self.movx = self.speed
        self.movy = self.speed
        self.color = paleta[blanco]
        self.beep = [sonido("sound/Beep1.wav"), sonido("sound/Beep2.wav"), sonido("sound/Beep8.wav"), sonido("sound/Beep13.wav")]

    def handle(self):
        if self.r.left < 0:
            self.beep[2].play()
            self.movx = self.speed
            return 1
        elif self.r.right > ancho:
            self.beep[2].play()
            self.movx = -self.speed
            return 2
        if self.r.top < 0:
            self.beep[3].play()
            self.movy = self.speed
        elif self.r.bottom > alto:
            self.beep[3].play()
            self.movy = -self.speed

        return None

    def colicion(self, rect):
        m = self.speed
        if self.r.right > rect.r.left and self.r.left < rect.r.right-m and self.r.bottom > rect.r.top+m and self.r.top < rect.r.bottom-m:
            self.beep[0].play()
            self.movx = -self.speed
            self.speed += .3
        if self.r.left < rect.r.right and self.r.right > rect.r.left+m and self.r.bottom > rect.r.top+m and self.r.top < rect.r.bottom-m:
            self.beep[1].play()
            self.movx = self.speed
            self.speed += .3
        if self.r.bottom > rect.r.top and self.r.top < rect.r.bottom-m and self.r.right > rect.r.left+m and self.r.left < rect.r.right-m:
            self.movy = -self.speed
        if self.r.top < rect.r.bottom and self.r.bottom > rect.r.top+m and self.r.right > rect.r.left+m and self.r.left < rect.r.right-m:
            self.movy = self.speed

    def reinicio(self):
        self.r.x = (ancho/2)
        self.r.y = (alto/2)
        self.speed = 2.5
        self.movx = self.speed
        self.movy = self.speed
        pygame.time.delay(500)


    def punto(self, num, puntos):
        if num != None:
            if num == 1:
                puntos[1] += 1
            elif num == 2:
                puntos[0] += 1
            self.reinicio()

class pala(pixel):
    def __init__(self, x=0, y=0, w=15, h=50, c=(255, 255, 255)):
        pixel.__init__(self, x, y, w, h, c)
        self.color = paleta[blanco]
        self.speed = 3.5

    def colicion(self, rect):
        m = self.speed
        if self.r.bottom > rect.r.top and self.r.top < rect.r.bottom-m and self.r.right > rect.r.left+m and self.r.left < rect.r.right-m:
            self.movy = 0
        if self.r.top < rect.r.bottom and self.r.bottom > rect.r.top+m and self.r.right > rect.r.left+m and self.r.left < rect.r.right-m:
            self.movy = 0

    def limites(self):
        if self.r.top < 0:
            self.r.top = 0
            self.movy = 0
        if self.r.bottom > alto:
            self.r.bottom = alto
            self.movy = 0

class player(pala):
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: self.movy = self.speed
            if event.key == pygame.K_UP: self.movy = -self.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                self.movy = 0

class pc(pala):
    def handle(self, pelota):
        half = pelota.r.x > (ancho/2)
        if pelota.movx > 0 and half:
            pos = pelota.r.y - (self.r.width/2) - (pelota.r.w/2)
            if self.r.y < pos:
                self.r.y += self.speed+1
            if self.r.y > pos:
                self.r.y -= self.speed+1
