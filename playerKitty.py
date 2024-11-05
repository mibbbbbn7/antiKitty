import pygame
import os

class Bullet_heart (pygame.sprite.Sprite):
    def __init__(self, bullet_surface, pos, groups):
        super().__init__(groups)
        self.image = bullet_surface
        self.rect = self.image.get_frect(midleft = pos)
    
    def update(self, delta_t, window_w, window_h):
        self.rect.x += 1000 * delta_t
        if self.rect.right > window_w:
            self.kill()


class Kitty(pygame.sprite.Sprite):
    def __init__(self, groups, spawn_x, spawn_y, bullet_heart_image):
        super().__init__(groups) #eredito da pygame.sprite.Sprite
        self.image = pygame.image.load(os.path.join("data", "kitty", "kittyx40.png")).convert_alpha() #1100/4=27.5
        self.rect = self.image.get_frect(center = (spawn_x, spawn_y))
            #le classi Sprite ereditano dal parent pygame.sprite.Sprite
            #al quale sostituisco i self.surf e self rect con la superficie 
            #e il rect del mio player(nell init infati inizializzo anche il super)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 800 

        self.bullet_heart_image = bullet_heart_image
        self.gruppo = groups

        #dash cool down
        self.can_dash = True
        self.dash_time = 0
        self.dash_cooldown = 5000

        #fire cool down
        self.can_fire = True
        self.fire_time = 0
        self.fire_cooldown = 150
        
    
    def dash_timer(self):
        
        if not self.can_dash:
            current_time = pygame.time.get_ticks() #millisecondi passati dall'avvio del gioco
            if current_time - self.dash_time >= self.dash_cooldown:
                self.can_dash = True
                print("Dash ready!!!")

    def fire_timer(self):

        if not self.can_fire:
            current_time = pygame.time.get_ticks()
            if current_time - self.fire_time >= self.fire_cooldown:
                self.can_fire = True
                print("Fire ready!!!")

    def update(self, delta_t, window_w, window_h):
        key = pygame.key.get_pressed()

        self.direction.x = int(key[pygame.K_d]) - int(key[pygame.K_a])
        self.direction.y = int(key[pygame.K_s]) - int(key[pygame.K_w])
            #kye[pygame.K_tasto] sono dei booleani quindi se li sommo in 
            #questo modo trasformati in int mi danno la direzione corrette,
            #inoltre quando i tasti non sono premuti assumono False che è 0
            #percio il player se ne ritorna con la direction x e/o y a 0
        
        if self.direction:        #un vector restituisce true quando è diverso da 0
            self.direction = self.direction.normalize()
            #se la player_direction è diversa da 0 la normalizzo, ovvero
            #anche quando mi muovo diagonalmente ho la stessa velocità normalizzata
        else:
            self.direction = self.direction
        self.rect.center += self.direction * self.speed * delta_t
    
        if pygame.key.get_pressed()[pygame.K_k] and self.can_fire:
            self.can_fire = False
            print("Fire!!!")
            Bullet_heart(self.bullet_heart_image, self.rect.midright, self.gruppo)
            self.fire_time = pygame.time.get_ticks()
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.can_dash:
            self.can_dash = False
            print("Dash!!!")
            self.dash_time = pygame.time.get_ticks()
        
        self.dash_timer()
        self.fire_timer()