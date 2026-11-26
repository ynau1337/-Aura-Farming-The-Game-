import pygame
import os
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        sprite_size = (16, 8)
        self.image = None
        
        sprites_dir = os.path.join("assets", "sprites")
        if os.path.exists(sprites_dir):
            for fname in os.listdir(sprites_dir):
                if "AK 47_Bullet" in fname.lower() and fname.lower().endswith(".png"):
                    try:
                        img = pygame.image.load(
                            os.path.join(sprites_dir, fname)
                        ).convert_alpha()
                        self.image = pygame.transform.scale(img, sprite_size)
                        break
                    except pygame.error:
                        pass
                    
        if self.image is None:
            self.image = pygame.Surface(sprite_size, pygame.SRCALPHA)
            self.image.fill((255, 215, 0))
        
        angle_deg = -math.degrees(angle)
        self.image = pygame.transform.rotate(self.image, angle_deg)
        self.rect = self.image.get_rect(center=(x, y))
        
        self.x = float(x)
        self.y = float(y)
        self.speed = 12.0
        
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (round(self.x), round(self.y))
        
        if (
            self.rect.x < -100
            or self.rect.x > 1000
            or self.rect.y < -100
            or self.rect.y > 800
        ):
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.assets_dir = os.path.join("assets", "player")
        self.rest_dir = os.path.join(self.assets_dir, "rest animation")
        self.run_dir = os.path.join(self.assets_dir, "run animation")
        self.sprites_dir = os.path.join("assets", "sprites")
        
        self.load_animations()
        self.load_weapon_sprites()
        
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
        
        self.weapon_angle = 0.0
        self.shoot_cooldown = 0
        
        self.is_shooting_anim = False
        self.weapon_anim_index = 0
        self.weapon_anim_timer = 0
        self.weapon_anim_speed = 25
    
    def load_animations(self):
        sprite_size = (96, 96)
        
        rest_filenames = [
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
    
    def load_weapon_sprites(self):
        self.weapon_frames = []
        weapon_size = (64, 32)
        
        for i in range(1, 13):
            filename = f"AK 47_SHOOT_{i:02d}.png"
            path = os.path.join(self.sprites_dir, filename)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.weapon_frames.append(pygame.transform.scale(img, weapon_size))
            except (pygame.error, FileNotFoundError):
                pass
        if not self.weapon_frames:
            fallback = pygame.Surface(weapon_size)
            fallback.fill((80, 80, 80))
            self.weapon_frames = [fallback]
            
    def update(self, bullets_group):
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
        
        mouse_pos = pygame.mouse.get_pos()
        rel_x = mouse_pos[0] - self.rect.centerx
        rel_y = mouse_pos[1] - self.rect.centery
        self.weapon_angle = math.atan2(rel_y, rel_x)
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and self.shoot_cooldown == 0:
            self.shoot(bullets_group)
            self.shoot_cooldown = 12
            
        self.animate_weapon()
        
    def shoot(self, bullets_group):
        muzzle_distance = 45
        spawn_x = self.rect.centerx + math.cos(self.weapon_angle) * muzzle_distance
        spawn_y = self.rect.centery + math.sin(self.weapon_angle) * muzzle_distance

        bullet = Bullet(spawn_x, spawn_y, self.weapon_angle)
        bullets_group.add(bullet)
        
        self.is_shooting_anim = True
        self.weapon_anim_index = 0
        self.weapon_anim_timer = pygame.time.get_ticks()
        
    def animate_weapon(self):
        if self.is_shooting_anim:
            now = pygame.time.get_ticks()
            if now - self.weapon_anim_timer > self.weapon_anim_speed:
                self.weapon_anim_timer = now
                self.weapon_anim_index += 1
                if self.weapon_anim_index >= len(self.weapon_frames):
                    self.weapon_anim_index = 0
                    self.is_shooting_anim = False
            
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
            
    def draw_weapon(self, surface):
        current_img = self.weapon_frames[self.weapon_anim_index]
        angle_deg = math.degrees(self.weapon_angle)
        
        if abs(angle_deg) > 90:
            current_img = pygame.transform.flip(current_img, False, True)
            
        rotated_weapon = pygame.transform.rotate(current_img, -angle_deg)
        
        orbit_radius = 28
        weapon_x = self.rect.centerx + math.cos(self.weapon_angle) * orbit_radius
        weapon_y = self.rect.centery + math.sin(self.weapon_angle) * orbit_radius

        weapon_rect = rotated_weapon.get_rect(center=(weapon_x, weapon_y))
        surface.blit(rotated_weapon, weapon_rect.topleft)