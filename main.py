import sys
import pygame

from player import Player

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
    
    all_sprites = pygame.sprite.Group()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(player)
    
    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        all_sprites.update()
                
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
        
    # Корректный выход из программы
    pygame.quit()
    sys.exit()
    
    
if __name__ == "__main__":
    main()