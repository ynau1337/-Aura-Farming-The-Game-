import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.assets_dir = os.path.join("assets", "player")
        self.rest_dir = os.path.join(self.assets_dir, "rest animation")
        self.run_dir = os.path.join(self.assets_dir, "run animation")
        
        self.load_animations()
        
        self.image = self.rest_frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.x = float(x)
        self.y = float(y)
        self.speed = 4.0
        
        self.is_moving = False
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 120
        self._last_moving_state = False
    
    def load_animations(self):
        sprite_size = (96, 96)
        
        rest_filenames = [
#            "assets/player/rest animation/player_rest01.png",
            "player_rest01.png",
            "player_rest02.png",
            "player_rest03.png",
            "player_rest04.png",
        ]
        self.rest_frames = []
        for name in rest_filenames:
            path = os.path.join(self.rest_dir, name)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, sprite_size)
                self.rest_frames.append(img)
            except (pygame.error, FileNotFoundError):
                surf = pygame.Surface(sprite_size)
                surf.fill((0, 255, 100))
                self.rest_frames.append(surf)
        
        run_filenames = [
            "player_run01.png",
            "player_run02.png",
            "player_run03.png",
            "player_run04.png",
            "player_run05.png",
            "player_run06.png",
            "player_run07.png",
        ]
        self.run_frames = []
        for name in run_filenames:
            path = os.path.join(self.run_dir, name)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, sprite_size)
                self.run_frames.append(img)
            except (pygame.error, FileNotFoundError):
                surf = pygame.Surface(sprite_size)
                surf.fill((0, 255, 100))
                self.run_frames.append(surf)       
            
    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
            
        if dx != 0 or dy != 0:
            self.is_moving = True
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071
        else:
            self.is_moving = False
            
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.center = (round(self.x), round(self.y))
            
        self.animate()
            
    def animate(self):
        now = pygame.time.get_ticks()
        current_frames = self.run_frames if self.is_moving else self.rest_frames
        
        if self._last_moving_state != self.is_moving:
            self.anim_index = 0
            self._last_moving_state = self.is_moving
            
        if now - self.anim_timer > self.anim_speed:
            self.anim_timer = now
            self.anim_index = (self.anim_index + 1) % len(current_frames)
            self.image = current_frames[self.anim_index]