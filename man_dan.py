import pygame
import time
import random

pygame.init()

crash_sound =pygame.mixer.Sound('Windshield_Hit_With_Bar.mp3')
pygame.mixer.music.load("8_Bit_March.mp3")

pause = True
dodged = 0
crashed = True


display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
blue = (0,0,150)



gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Man Dan')
clock = pygame.time.Clock()


manImg = pygame.image.load('man.png')
manLogo = pygame.image.load('man_icon.png')
pygame.display.set_icon(manLogo)

def unpause():
	global pause
	pause = False
	pygame.mixer.music.unpause()


def quit_game():
	pygame.quit()
	quit()

def man(x,y):
	gameDisplay.blit(manImg,(x,y))



def things(thingx,thingy,thingw,thingh, color):			#--maybe replace things with pretty cats?
	pygame.draw.rect(gameDisplay, color,[thingx,thingy,thingw,thingh])

def things_dodged(count):
	font = pygame.font.SysFont("comicsansms", 25)
	text = font.render('Dodged: ' + str(count), True, black)
	gameDisplay.blit(text,(0,0))


def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.SysFont('comicsansms',115)
	TextSurf, TextRect = text_objects(text,largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	pygame.display.update()

def crash():

	pygame.mixer.music.stop()
	time.sleep(0.5)
	pygame.mixer.Sound.play(crash_sound)
	global crashed
	while crashed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		largeText = pygame.font.SysFont('comicsansms',115)
		textSurf, textRect = text_objects("Game Over",largeText)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurf, textRect)

		button("Play Again",150,450,100,50,green,bright_green,game_loop)
		button("Quit",550,450,100,50,red,bright_red,quit_game)


		pygame.display.update()



def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	#print click 

	if x + w > mouse[0] > x and y + h > mouse[1] >y:
		pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
#--outdated 			if action == "play":
#--outdated 				game_loop()
#--outdated 			elif action == "quit":
#--outdated 				pygame.quit()
#--outdated 				quit()

	else:
		pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

	smallText = pygame.font.SysFont('comicsansms',20)
	textSurf, textRect = text_objects(msg,smallText)
	textRect.center = ((x+(w/2)),(y+(h/2)))
	gameDisplay.blit(textSurf,textRect)

def paused():

	pygame.mixer.music.pause()
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		largeText = pygame.font.SysFont('comicsansms',115)
		textSurf, textRect = text_objects("Paused",largeText)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurf, textRect)

		button("Continue",150,450,100,50,green,bright_green,unpause)
		button("Quit",550,450,100,50,red,bright_red,quit_game)


		pygame.display.update()
		clock.tick(15)


def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		largeText = pygame.font.SysFont('comicsansms',115)
		textSurf, textRect = text_objects("Man Dan",largeText)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurf, textRect)

		button("GO!",150,450,100,50,green,bright_green,game_loop)
		button("Quit",550,450,100,50,red,bright_red,quit_game)


		pygame.display.update()
		clock.tick(15)





def game_loop():
	pygame.mixer.music.play(-1)	
	global pause
	global dodged
	global crashed

	crashed = False
	dodged = 0
	x = (display_width * 0.45)
	y = (display_height * 0.8)

	change_x = 0
	change_y = 0
	man_width = 53

	thing_startx = random.randrange(0,display_width)
	thing_starty = -600
	thing_speed = 3
	thing_width = 100
	thing_height = 100


	gameExit = False


	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					change_x = -5
				if event.key == pygame.K_RIGHT:
					change_x = 5
				if event.key == pygame.K_p:
					pause = True
					paused()


			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					change_x = 0


		x += change_x


		gameDisplay.fill(white)

		
		things(thing_startx,thing_starty,thing_width,thing_height,blue)
		
		thing_starty += thing_speed
		man(x,y)
		
		things_dodged(dodged)

		if x > display_width-man_width or x < 0:
			crash()
		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(0,display_width)
			dodged += 1
			thing_speed += 1


		if y < thing_starty + thing_height:
			print'y crossover'

			if x > thing_startx and x < thing_startx + thing_width or x + man_width > thing_startx and x + man_width < thing_startx + thing_width:
				crashed = True
				crash_sound.play()
				crash()
					

		pygame.display.update()

		clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()