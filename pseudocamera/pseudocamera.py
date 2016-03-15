import pygame
from pygame.locals import *
from networktables import NetworkTable

pygame.init()

w = 640
h = 480

screen = pygame.display.set_mode((w,h))

NetworkTable.setIPAddress("roborio-4761-frc.local")
NetworkTable.setClientMode()
NetworkTable.initialize()

table = NetworkTable.getTable("vision")

# clock object that will be used to make the animation
# have the same speed on all machines regardless
# of the actual machine speed.
clock = pygame.time.Clock()

while True:
	clock.tick(50);
	try:
		topleft_x = table.getNumber("topleft_x")
		topleft_y = table.getNumber("topleft_y")
		width = table.getNumber("width")
		height = table.getNumber("height")
		
		if table.getNumber("can_see_target") == 1:
			color = (0,255,0)
		else:
			color = (255,0,0)
		screen.fill((0,0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.draw.rect(screen, color, (topleft_x, topleft_y, width, height))
		pygame.draw.line(screen, (255,255,255), (w / 2, 0), (w / 2, h))
		pygame.draw.line(screen, (255,255,255), (0, h / 2), (w, h / 2))
		pygame.display.update()
		print "Updated!"
	except KeyError:
		print "Something went wrong with NetworkTables!"
