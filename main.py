import pygame

print("Setup Started")
pygame.init()
window = pygame.display.set_mode(size=(600, 480))
print("Setup Ended")

print("Setup Loop")

while True:
    # Check for all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #Close Window
            quit() #end pygame
