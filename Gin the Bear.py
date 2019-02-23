#!/usr/bin/env python
import os,random,pygame
from pygame import*
def fps():time.Clock().tick(60)
def load_image(file):return image.load(os.path.join('data',file)).convert_alpha()
def sound(file):
	class Nosound:
		def play(self):pass
	if not pygame.mixer:return Nosound()
	return mixer.Sound(os.path.join('data',file)).play()
class Bear(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self,self.sprite)
		self.image=self.images[0]
		self.rect=self.image.get_rect(midbottom=[w/2,h])
		self.reload=0
		self.origtop=self.rect.top-30
		self.facing=-1
	def move(self,going):
		if going:self.facing=going
		self.rect.move_ip(going*7,0)
		self.rect=self.rect.clamp(0,0,w,h)
		if going<0:self.image=self.images[0]
		elif going>0:self.image=self.images[1]
		self.rect.top=self.origtop-(self.rect.left//24%2)
	def gun(self):return self.rect.centerx,self.rect.top
class Penguin(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self,self.sprite)
		self.image=self.images[0]
		self.rect=self.image.get_rect()
		self.facing=random.choice((-1,1))*4
		self.frame=0
		if self.facing<0:self.rect.right=w
	def update(self):
		self.rect.move_ip(self.facing,0)
		if not Rect(0,0,w,h).contains(self.rect):
			self.facing=-self.facing
			self.rect.top=self.rect.bottom+1
			self.rect=self.rect.clamp(0,0,w,h)
		self.frame+=1
		self.image=self.images[self.frame//13%2]
class Boom(sprite.Sprite):
	def __init__(self,actor):
		sprite.Sprite.__init__(self,self.sprite)
		self.image=self.images[0]
		self.rect=self.image.get_rect(center=actor.rect.center)
		self.life=26
		sound('boom.ogg')
	def update(self):
		self.life-=1
		self.image=self.images[self.life//6%2]
		if self.life<=0:self.kill()
class Shot(sprite.Sprite):
	def __init__(self,pos):
		sprite.Sprite.__init__(self,self.sprite)
		self.rect=self.image.get_rect(midbottom=pos)
		sound('shot.ogg')
	def update(self):
		self.rect.move_ip(0,-7)
		if self.rect.top<=0:self.kill()
class Bomb(sprite.Sprite):
	def __init__(self,penguin):
		sprite.Sprite.__init__(self,self.sprite)
		self.rect=self.image.get_rect(midbottom=penguin.rect.move(0,5).midbottom)
	def update(self):
		self.rect.move_ip(0,7)
		if self.rect.bottom>=h-32:
			Boom(self)
			self.kill()
class Score(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.font=font.Font(os.path.join('data','Jellee-Roman.otf'),22,bold=1)
		self.lastscore=-1
		self.update()
		self.rect=self.image.get_rect().move(10,5)
	def update(self):
		if SCORE!=self.lastscore:
			self.lastscore=SCORE
			self.image=self.font.render("Penguins: %d"%SCORE,1,color)
class Menu():
	def __init__(self,screen):
		fontfile=os.path.join('data','GoodDog.otf')
		fontfile2=os.path.join('data','Jellee-Roman.otf')
		self.font=font.Font(fontfile,70,bold=1)
		self.font2=font.Font(fontfile2,20,bold=1)
		self.font3=font.Font(fontfile2,10,bold=0)
		self.font4=font.Font(fontfile2,7,bold=0)
		self.background=load_image('bg.png')
	def intro(self):
		while True:
			fps()
			key=pygame.key.get_pressed()
			if event.peek(QUIT) or key[K_ESCAPE]:break
			if key[K_SPACE]:
				main()
				break
			screen.blit(self.background,(0,0))
			label=self.font.render("Gin the Bear",1,(197,120,38))
			lw=label.get_rect().width
			lh=label.get_rect().height
			label2=self.font2.render("press space to shoot",1,color)
			lw2=label2.get_rect().width
			lh2=label2.get_rect().height
			label3=self.font3.render("Made by Yojka (C) 2017. Powered by Pygame, beer and muffins. Approved by Gin the Cat. Pre-alpha (Build 18).",1,color)
			lw3=label3.get_rect().width
			lh3=label3.get_rect().height
			logo=load_image('mouse.png')
			lw4=logo.get_rect().width
			lh4=logo.get_rect().height
			screen.blit(label,(w/2-lw/2,h/2-lh4/2-lh-50))
			screen.blit(label2,(w/2-lw2/2,h/2-lh2+120))
			screen.blit(label3,(w/2-lw3/2,h-lh3/2-16))
			screen.blit(logo,(w/2-lw4/2,h/2-lh4/2))
			display.flip()
	def gameover(self):
		global SCORE
		if pygame.mixer:pygame.mixer.music.fadeout(1000)
		pygame.time.wait(1000)
		while True:
			fps()
			key=pygame.key.get_pressed()
			if event.peek(QUIT) or key[K_ESCAPE]:break
			if key[K_SPACE]:
				SCORE=0
				main()
				break
			screen.fill((0,0,0))
			label=self.font.render("Gin is DEAD",1,color)
			lw=label.get_rect().width
			lh=label.get_rect().height
			screen.blit(label,(w/2-lw/2,h/2-lh/2-10))
			cl=h/2-lh/2-35
			label2=self.font2.render("press space to restart",1,color)
			screen.blit(label2,(w/2-label2.get_rect().width/2,h/2-lh+100))
			label3=self.font2.render("Buy me game! - Gin.",1,color)
			if SCORE==5:screen.blit(label3,(w/2-label4.get_rect().width/2,cl))
			label4=self.font2.render("Greenlight is dead too",1,color)
			if SCORE==10:screen.blit(label4,(w/2-label4.get_rect().width/2,cl))
			label666=self.font2.render("Hellygin",1,color)
			if SCORE==666:screen.blit(label666,(w/2-label666.get_rect().width/2,cl))
			label1337=self.font2.render("1337 Hackz00r",1,color)
			if SCORE==1337:screen.blit(label1337,(w/2-label1337.get_rect().width/2,cl))
			label9000=self.font2.render("Over 9000!!!",1,color)
			if SCORE>9000:screen.blit(label9000,(w/2-label9000.get_rect().width/2,cl))
			display.flip()
	def pause(self):
		label=self.font.render("PAUSE",1,color)
		lw=label.get_rect().width
		lh=label.get_rect().height
		screen.blit(label,(w/2-lw/2,h/2-lh))
		if pygame.mixer:pygame.mixer.music.pause()
		while True:
			fps()
			pygame.display.update()
			key=pygame.key.get_pressed()
			if event.peek(QUIT) or key[K_SPACE]:
				screen.blit(self.background,(0,0))
				display.flip()
				if pygame.mixer:pygame.mixer.music.unpause()
				break
def main():
	if not mixer.get_init():pygame.mixer=0
	if pygame.mixer:
		music=os.path.join('data','music.ogg')
		pygame.mixer.music.load(music)
		pygame.mixer.music.play(-1)
	Bear.images=[transform.scale(load_image('mouse.png'),(32,32)),transform.scale(transform.flip(load_image('mouse.png'),1,0),(32,32))]
	Boom.images=[load_image('boom.png'),transform.flip(load_image('boom.png'),1,1)]
	Penguin.images=[load_image('penguin1.png'),load_image('penguin2.png')]
	Bomb.image=load_image('beer.png')
	Shot.image=load_image('muffin.png')
	background=load_image('bg.png')
	screen.blit(background,(0,0))
	display.flip()
	penguins=sprite.Group()
	shots=sprite.Group()
	bombs=sprite.Group()
	oldpenguin=sprite.GroupSingle()
	all=sprite.RenderUpdates()
	Bear.sprite=Boom.sprite=Score.sprite=all
	Penguin.sprite=all,penguins,oldpenguin
	Shot.sprite=all,shots
	Bomb.sprite=all,bombs
	global SCORE
	all.add(Score())
	newpenguin=12
	bear=Bear()
	while bear.alive():
		fps()
		key=pygame.key.get_pressed()
		if event.peek(QUIT) or key[K_ESCAPE]or key[K_PAUSE]:Menu(screen).pause()
		bear.move(key[K_RIGHT]-key[K_LEFT])
		if not bear.reload and key[K_SPACE] and len(shots)<3:Shot(bear.gun())
		bear.reload=key[K_SPACE]
		if newpenguin:newpenguin-=1
		elif not int(random.random()*22):
			Penguin()
			newpenguin=12
		if oldpenguin and not int(random.random()*60):Bomb(oldpenguin.sprite)
		for penguin in sprite.groupcollide(shots,penguins,1,1):
			Boom(penguin)
			SCORE+=1
		for bomb in sprite.spritecollide(bear,bombs,1):
			Boom(bear)
			Boom(bomb)
			bear.kill()
		for penguin in sprite.spritecollide(bear,penguins,1):
			Boom(penguin)
			Boom(bear)
			bear.kill()
		all.clear(screen,background)
		all.update()
		display.update(all.draw(screen))
	Menu(screen).gameover()
init()
w=640
h=480
SCORE=0
color=(255,0,0)
mouse.set_visible(0)
screen=display.set_mode([w,h])
display.set_icon(load_image('mouse.png'))
display.set_caption('Gin the Bear')
Menu(screen).intro()