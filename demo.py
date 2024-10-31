import pygame
import sys
import random
import time
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.mixer.init()

global gos
gos = 0
gy = 0
gyi = 0
ary = 375
optsx = 400

# Set up the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dodgenada DEMO")

font = pygame.font.SysFont("Gochi Hand", 60)  # Choose a font and size

# Load assets
icon = pygame.image.load("assets/images/gui/other/windIcon.png")
pygame.display.set_icon(icon)

go_img = pygame.image.load("assets/images/gui/gameover/txt.png")

plrx = 336
plry = 460
cb = False
gstate = "title"
retrying = False
score = 0
enemies = [] 
key_delay = 0.3  # Delay in seconds between key presses
last_key_press_time = 0  # Time of the last key press

plr_def = pygame.image.load("assets/images/plr/plr.png")
plr_l = pygame.image.load("assets/images/plr/left.png")
plr_r = pygame.image.load("assets/images/plr/right.png")
txtm_img = pygame.image.load("assets/images/gui/title/txt.png")
opts_img = pygame.image.load("assets/images/gui/title/buttons/opts.png")
ar_img = pygame.image.load("assets/images/gui/title/buttons/arrow.png")
sb_img = pygame.image.load("assets/images/gui/other/sidebars.png")
beep_sound = pygame.mixer.Sound("assets/sounds/beep.wav")

def spawn_enemy():
    en_x = random.randint(0, window_width)  # Random x position within window bounds
    enemy_type = random.randint(1, 5)  # Random enemy type
    enemy_img = pygame.image.load(f"assets/images/enemies/{cb}/{enemy_type}.png")  # Load enemy image
    enemies.append([enemy_img, en_x, 0, enemy_type])  # Add enemy to the list

clock = pygame.time.Clock()
vel = 5 

running = False
warn = True

while warn:
    font_large = pygame.font.SysFont("Arial", 60)
    font_small = pygame.font.SysFont("Arial", 30)

    icon = pygame.image.load("assets/images/gui/other/windIcon.png")
    pygame.display.set_icon(icon)

    rw = True
    while rw:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Check if spacebar is pressed
                    rw = False
                    warn = False
                    running = True
                     
        window.fill((0, 0, 0))

        text_surface = font_large.render("WARNING!", True, (234, 5, 25))
        text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2 - 250))
        window.blit(text_surface, text_rect)

        lines = [
            "This game is in a very,",
            "very early demo stage.",
            "A lot, even most, of",
            "the game is either incomplete",
            "or entirely missing.",
            "Press space to continue."
        ]

        for i, line in enumerate(lines):
            text_surface = font_small.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2 - 100 + i * 30))
            window.blit(text_surface, text_rect)

        pygame.display.flip()

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((255, 255, 255))  # Clear the screen

    if gstate == "game":
        # Player movement
        if keys[pygame.K_w]:
            plry -= vel
            plr_img = plr_def
        if keys[pygame.K_s]:
            plry += vel
            plr_img = plr_def
        if keys[pygame.K_a]:
            plrx -= vel
            plr_img = plr_l
        if keys[pygame.K_d]:
            plrx += vel
            plr_img = plr_r

        if plrx < 125:
            plrx = 125
        if plrx > 570:
            plrx = 570

        if not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_w]:
            vel = 5
            plr_img = plr_def
        else:
            vel = min(vel + 0.2, 15)

        s_plr_w = plr_img.get_width() * 0.7
        s_plr_h = plr_img.get_height() * 0.7
        s_plr_img = pygame.transform.scale(plr_img, (s_plr_w, s_plr_h))

        window.blit(s_plr_img, (plrx, plry))  # Draw player
        
        hb_ps_h = s_plr_h // 1.5
        hb_ps_w = s_plr_w // 1.5
        plr_hb = pygame.Rect(plrx, plry, hb_ps_w, hb_ps_h)

        # Spawn enemy randomly
        if random.randint(0, 50) == 15:
            spawn_enemy()

        for enemy in enemies:
            enemy_img, en_x, en_y, enemy_type = enemy
            s_en_img = pygame.transform.scale(enemy_img, (int(enemy_img.get_width() * 0.7), int(enemy_img.get_height() * 0.7)))
            window.blit(s_en_img, (en_x, en_y))

            if enemy_type == 1 or enemy_type == 4:
                en_y += 10 
            if enemy_type == 2:
                en_y += 20
            if enemy_type == 3:
                en_y += 30
            if enemy_type == 5:
                en_y += random.randint(-30, 30)
                en_x += random.randint(-30, 30)

            enemy[2] = en_y

            en_hb = pygame.Rect(en_x, en_y, hb_ps_w, hb_ps_h)
            if plr_hb.colliderect(en_hb):
                if enemy_type == 4:
                    score += 1
                    enemies.remove(enemy)
                else:
                    gos = 50
                    gy = window_height // 2
                    retrying = False
                    gy = 300
                    gyi = 0
                    gstate = "gameover"
                    root = tk.Tk()
                    root.withdraw() 
                    messagebox.showinfo("Info", "Press \'R\" to retry.")

            if en_y > window_height:
                if enemy_type == 4:
                    score -= 1
                    enemies.remove(enemy)
                else:
                    score += 1
                    enemies.remove(enemy)

        # Remove enemies that went off the screen
        enemies = [enemy for enemy in enemies if enemy[2] <= window_height]

    if gstate == "gameover":
        # Draw Game Over screen
        goss = gos // 5
        gosp2k = goss
        gosp = gos + goss
        gosa = gos // 5
        s_go_img = pygame.transform.scale(go_img, (gosp, gosp2k))  # Scale the game over image
        go_rect = s_go_img.get_rect(center=(window_width // 2, gy))
        gos += gosa
        if gos >= 600:
            gos = 600

        if retrying == True:
            if gyi < 800:
                gyi = gy // 20
                gy += gyi
            else:
                plrx, plry = 336, 460  
                enemies.clear()
                gstate = "game"
                score = 0

        if retrying == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                retrying = True

    if gstate == "title":        
        plr_img = plr_def
        s_plr_w = plr_img.get_width() * 2
        s_plr_h = plr_img.get_height() * 2
        s_plr_img = pygame.transform.scale(plr_img, (s_plr_w, s_plr_h))
        
        plrx = (window_width - s_plr_w) // 2 
        plry = (window_height - s_plr_h) // 2
        window.blit(s_plr_img, (plrx, plry)) 

        s_opts_img = pygame.transform.scale(opts_img, (600, 50))
        opts_rect = s_opts_img.get_rect()
        opts_rect.center = (optsx, 350)
        window.blit(s_opts_img, opts_rect)

        s_ar_img = pygame.transform.scale(ar_img, (50, 50))
        ar_rect = s_opts_img.get_rect()
        if ary < 385:
            ary += 1
        else:
            ary = 375
        ar_rect.center = (675, ary)
        window.blit(s_ar_img, ar_rect)

        current_time = time.time()

        if keys[pygame.K_RIGHT] and (current_time - last_key_press_time >= key_delay):
            if optsx == 400:
                optsx = 270
            elif optsx == 270:
                optsx = 150
            elif optsx == 650:
                optsx = 530
            elif optsx == 530:
                optsx = 400
            beep_sound.play()
            last_key_press_time = current_time

        if keys[pygame.K_LEFT] and (current_time - last_key_press_time >= key_delay):
            if optsx == 400:
                optsx = 530
            elif optsx == 530:
                optsx = 650
            elif optsx == 270:
                optsx = 400
            elif optsx == 150:
                optsx = 270
            beep_sound.play()
            last_key_press_time = current_time

        if keys[pygame.K_RETURN] and (current_time - last_key_press_time >= key_delay):
            if optsx == 400:
                plrx, plry = 336, 460 
                enemies.clear()
                gstate = "game"
                root = tk.Tk()
                root.withdraw() 
                messagebox.showinfo("How to play", "Enemies spawn from the top of the screen and go down to the bottom.\nRed, yellow, and magenta enemies move at different speeds, but they both give you a game over upon collision.\nWhen one of these enemies reach the bottom of the screen, you gain a point.\nGreen enemies, however, give you a point upon collision, and take away a point upon going through the bottom.\nWASD movement controls.")
                score = 0

            elif optsx == 650:
                root = tk.Tk()
                root.withdraw() 
                messagebox.showinfo("Error", "This feature is not in Dodgenada yet!")

            elif optsx == 150:
                pygame.quit()
                sys.exit()

            elif optsx == 270:
                root = tk.Tk()
                root.withdraw() 
                messagebox.showinfo("Error", "This feature is not in Dodgenada yet!")

            beep_sound.play()
            print(optsx)

    window.blit(sb_img, (672, 0))
    window.blit(sb_img, (0, 0))
    window.blit(sb_img, (672, 300))
    window.blit(sb_img, (0, 300))

    if gstate == "title":
        s_txtm_img = pygame.transform.scale(txtm_img, (600, 160))
        txt_rect = s_txtm_img.get_rect()
        txt_rect.center = (400, 170)
        window.blit(s_txtm_img, txt_rect)

    if gstate == "gameover":
        window.blit(s_go_img, go_rect)

    text_surface = font.render(str(score), True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft=(10, 0))  # Center the text
    window.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(60)
