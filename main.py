import pygame
from _thread import start_new_thread

def average(list):
    return [sum(list[:3])/len(list[:3])]*3

def convert(cimage):
    global image
    for x in range(cimage.get_width()):
        for y in range(cimage.get_height()):
            image.set_at((x, y), average(cimage.get_at((x, y))))


def main():
    global image
    image = pygame.image.load("bild.jpg")

    screen = pygame.display.set_mode((image.get_width(), image.get_height()))

    ongoing = True
    while ongoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start_new_thread(convert, (image, ))
        screen.blit(image, (0, 0))
        pygame.display.flip()

    pygame.quit()



if __name__ == '__main__':
    main()
