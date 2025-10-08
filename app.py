import pygame
pygame.init #Run pygame


screen_width, screen_height = 640, 480
display_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Code-Slayer-v0.1")

#Create player
char = pygame.image.load('Images/character.png')


Running = True #Running the game
while Running: #Looping the game
    #       
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            Running = False
    
    display_screen.fill("salmon")
    display_screen.blit(char, (100,150))
    pygame.display.update()

pygame.quit()