import sys
import pygame

def main():
    # Инициализация Pygame.
    pygame.init()
    
    # Настройки окна.
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Auro Farming: The Game")
    
    # Настройка часов для контроля FPS
    clock = pygame.time.Clock()
    FPS = 60
    
    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill((30, 30, 30))
        pygame.display.flip()
        clock.tick(FPS)
        
    # Корректный выход из программы
    pygame.quit()
    sys.exit()
    
    
if __name__ == "__main__":
    main()