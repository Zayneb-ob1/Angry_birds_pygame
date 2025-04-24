import pygame
import physics_engine
import interface
import sys

# Initialisation de pygame
pygame.init()

# Variables pour l'écran
width = None
height = None
display = None
clock = pygame.time.Clock()

# Hauteur de la plateforme
ground = 50
# Vitesse de déplacement des objets
d_velocity = 2.0

def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    height -= ground
    interface.init(display)
    
# cherche mouvement
def all_rest(pigs, birds, blocks):
    threshold = 0.15
    for pig in pigs:
        if pig.velocity.magnitude >= threshold:
            return False
    for bird in birds:
        if bird.velocity.magnitude >= threshold:
            return False
    for block in blocks:
        if block.velocity.magnitude >= threshold:
            return False
    return True

def close():
    pygame.quit()
    sys.exit()

# Classe pour gérer les niveaux (Maps)
class Maps:
    def __init__(self):
        self.level = 1
        self.max_level = 2
        self.color = {'background': (240, 128, 128)}
        self.score = 0

    def wait_level(self):
        time = 0
        while time < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
            time += 1
            clock.tick(1)

    def check_win(self, pigs, birds):
        if not pigs:
            print("WON!")
            return True
        if pigs and not birds:
            print("LOST!")
            return False

    def pause(self):
        pause_text = interface.Label(700, 200, 350, 150, None, self.color['background'])
        pause_text.add_text("GAME PAUSED", 60, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = interface.Button(350, 500, 250, 80, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.add_text("RESTART", 50, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        resume = interface.Button(750, 500, 250, 80, None, (88, 214, 141), (171, 235, 198))
        resume.add_text("RESUME", 50, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = interface.Button(1150, 500, 250, 80, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 50, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if resume.isActive():
                        return
                    if exit.isActive():
                        exit.action()

            replay.draw()
            resume.draw()
            exit.draw()
            pause_text.draw()
            pygame.display.update()
            clock.tick(60)

# creation level 1 et level 2
    def draw_map(self):
        birds = []
        pigs = []
        blocks = []

        if self.level == 1:
            for i in range(3):
                birds.append(physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD"))
            pigs.append(physics_engine.Pig(1100, height - 40, 20))
            pigs.append(physics_engine.Pig(1500, height - 40, 20))
            blocks.append(physics_engine.Block(1300, height - 60, 60))
        elif self.level == 2:
            for i in range(3):
                birds.append(physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD"))
            pigs.append(physics_engine.Pig(1000, height - 40, 20))
            pigs.append(physics_engine.Pig(1400, height - 40, 20))
            blocks.append(physics_engine.Block(1200, height - 60, 60))
            blocks.append(physics_engine.Block(1200, height - 2*35, 60))
            blocks.append(physics_engine.Block(1500, height - 60, 60))

        # Load image
        background_img = pygame.image.load(r"C:\Users\HP\Documents\Angry_birds\assets\game.jpg")
        background_img = pygame.transform.scale(background_img, (width, height))  

        # Draw the background image
        display.blit(background_img, (0, 0))  

        # Lancer le jeu pour le niveau actuel
        self.start_level(birds, pigs, blocks)

    def replay_level(self):
        self.level -= 1
        self.draw_map()

    def start_again(self):
        self.level = 1
        self.draw_map()

    # Fonction pour afficher le texte lorsque le niveau est terminé
    def level_cleared(self):
        self.level += 1
        screen_center_x = width // 2 
        level_cleared_text = interface.Label(screen_center_x, 100, 500, 80, None, self.color['background'])
        if self.level <= self.max_level:
            level_cleared_text.add_text("LEVEL " + str(self.level - 1) + " CLEARED!", 60, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        else:
            level_cleared_text.add_text("ALL LEVELS CLEARED!", 70, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        score_text = interface.Label(screen_center_x, 200, 300, 80, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 40, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        button_width = 250
        button_height = 80
        button_y = 400 
        space_between = 75
        total_width = (3 * button_width) + (2 * space_between)
        start_x = screen_center_x - (total_width // 2)
        
        
        continue_btn = interface.Button(start_x + button_width + space_between, button_y, button_width, button_height, 
        self.draw_map, (88, 214, 141), (171, 235, 198))
        
        if self.level <= self.max_level:
            continue_btn.add_text("CONTINUE", 40, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        else:
            continue_btn = interface.Button(start_x + button_width + space_between, button_y, button_width, button_height, 
        self.start_again, (88, 214, 141), (171, 235, 198))
            continue_btn.add_text("START AGAIN", 35, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        
        quit_btn = interface.Button(start_x + (2 * button_width) + (2 * space_between), button_y, 
        button_width, button_height, close, (88, 214, 141), (171, 235, 198))
        quit_btn.add_text("QUIT", 40, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_q, pygame.K_ESCAPE):
                    close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if continue_btn.isActive():
                        continue_btn.action()
                    if quit_btn.isActive():
                        quit_btn.action()
            display.fill(self.color['background'])
            color = self.color['background']
            for i in range(3):
                color = (color[0] + 5, color[1] + 5, color[2] + 5)
                pygame.draw.rect(display, color, (0, i*300, width, 300))
            pygame.draw.rect(display, (77, 86, 86), (0, height, width, 50))
            continue_btn.draw()
            quit_btn.draw()
            level_cleared_text.draw()
            score_text.draw()
            pygame.display.update()
            clock.tick(60)
            
    def level_failed(self):
        screen_center_x = width // 2
        level_failed_text = interface.Label(screen_center_x, 120, 600, 100, None, self.color['background'])
        level_failed_text.add_text("LEVEL FAILED!", 70, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        score_text = interface.Label(screen_center_x, 220, 350, 80, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 50, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        button_width = 250
        button_height = 80
        button_y = 400  
        space_between = 100
        total_width = (2 * button_width) + space_between
        start_x = screen_center_x - (total_width // 2)
        try_again_btn = interface.Button(start_x, button_y, button_width, button_height, 
        self.draw_map, (244, 208, 63), (247, 220, 111))
        try_again_btn.add_text("TRY AGAIN", 40, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        
        quit_btn = interface.Button(start_x + button_width + space_between, button_y, 
        button_width, button_height, close, (241, 148, 138), (245, 183, 177))
        quit_btn.add_text("QUIT", 40, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_q, pygame.K_ESCAPE):
                    close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_btn.isActive():
                        try_again_btn.action()
                    if quit_btn.isActive():
                        quit_btn.action()

            display.fill(self.color['background'])
            color = self.color['background']
            for i in range(3):
                color = (color[0] + 5, color[1] + 5, color[2] + 5)
                pygame.draw.rect(display, color, (0, i*300, width, 300))
                
            pygame.draw.rect(display, (77, 86, 86), (0, height, width, 50))
            
            try_again_btn.draw()
            quit_btn.draw()
            level_failed_text.draw()
            score_text.draw()
            pygame.display.update()
            clock.tick(60)

    def start_level(self, birds, pigs, blocks):
        loop = True
        slingshot = physics_engine.Slingshot(200, height - 200, 30, 200)
        birds[0].load(slingshot)
        mouse_click = False
        flag = 1
        pigs_to_remove = []
        blocks_to_remove = []

        score_text = interface.Label(50, 10, 90, 40, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 20, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        birds_remaining = interface.Label(120, 50, 90, 40, None, self.color['background'])
        birds_remaining.add_text("BIRDS REMAINING: " + str(len(birds)), 20, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        pigs_remaining = interface.Label(110, 90, 90, 40, None, self.color['background'])
        pigs_remaining.add_text("PIGS REMAINING: " + str(len(pigs)), 20, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        self.draw_map()
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.pause()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if birds[0].mouse_selected():
                        mouse_click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = False
                    if birds[0].mouse_selected():
                        flag = 0

            if (not birds[0].loaded) and all_rest(pigs, birds, blocks):
                birds.pop(0)
                if self.check_win(pigs, birds) == 1:
                    self.score += len(birds)*100
                    self.level_cleared()
                elif self.check_win(pigs,birds) == 0:
                    self.level_failed()

                if birds:
                    birds[0].load(slingshot)
                flag = 1

            if mouse_click:
                birds[0].reposition(slingshot, mouse_click)

            if not flag:
                birds[0].unload()

            color = self.color['background']
            for i in range(3):
                color = (color[0] + 5, color[1] + 5, color[2] + 5)
                pygame.draw.rect(display, color, (0, i*300, width, 300))

            pygame.draw.rect(display, (77, 86, 86), (0, height, width, 50))
            slingshot.draw(birds[0])

            for i in range(len(pigs)):
                for j in range(len(blocks)):
                    pig_v, block_v = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude
                    pigs[i], blocks[j], result_block_pig = physics_engine.collision_handler(pigs[i], blocks[j], "BALL_N_BLOCK")
                    pig_v1, block_v1 = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block_pig:
                        if abs(pig_v - pig_v1) > d_velocity:
                            blocks_to_remove.append(blocks[j])
                            blocks[j].destroy()
                        if abs(block_v - block_v1) > d_velocity:
                            pigs_to_remove.append(pigs[i])
                            pigs[i].dead()

            for i in range(len(birds)):
                if not (birds[i].loaded or birds[i].velocity.magnitude == 0):
                    for j in range(len(blocks)):
                        birds_v, block_v = birds[i].velocity.magnitude, blocks[j].velocity.magnitude
                        birds[i], blocks[j], result_bird_block = physics_engine.collision_handler(birds[i], blocks[j], "BALL_N_BLOCK")
                        birds_v1, block_v1 = birds[i].velocity.magnitude, blocks[j].velocity.magnitude

                        if result_bird_block:
                            if abs(birds_v - birds_v1) > d_velocity:
                                if blocks[j] not in blocks_to_remove:
                                    blocks_to_remove.append(blocks[j])
                                    blocks[j].destroy()

            for i in range(len(pigs)):
                pigs[i].move()
                for j in range(i+1, len(pigs)):
                    pig1_v, pig2_v = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    pigs[i], pigs[j], result = physics_engine.collision_handler(pigs[i], pigs[j], "BALL")
                    pig1_v1, pig2_v1 = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    if result:
                        if abs(pig1_v - pig1_v1) > d_velocity:
                            if pigs[j] not in pigs_to_remove:
                                pigs_to_remove.append(pigs[j])
                                pigs[j].dead()
                        if abs(pig2_v - pig2_v1) > d_velocity:
                            if pigs[i] not in pigs_to_remove:
                                pigs_to_remove.append(pigs[i])
                                pigs[i].dead()
                pigs[i].draw()

            for i in range(len(birds)):
                if (not birds[i].loaded) and birds[i].velocity.magnitude:
                    birds[0].move()
                    for j in range(len(pigs)):
                        bird_v, pig_v = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        birds[i], pigs[j], result_bird_pig = physics_engine.collision_handler(birds[i], pigs[j], "BALL")
                        bird_v1, pig_v1 = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        if result_bird_pig:
                            if abs(bird_v - bird_v1) > d_velocity:
                                if pigs[j] not in pigs_to_remove:
                                    pigs_to_remove.append(pigs[j])
                                    pigs[j].dead()

                if birds[i].loaded:
                    birds[i].project_path()
                birds[i].draw()

            for i in range(len(blocks)):
                for j in range(i + 1, len(blocks)):
                    block1_v, block2_v = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude
                    blocks[i], blocks[j], result_block = physics_engine.block_collision_handler(blocks[i], blocks[j])
                    block1_v1, block2_v1 = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block:
                        if abs(block1_v - block1_v1) > d_velocity:
                            if blocks[j] not in blocks_to_remove:
                                blocks_to_remove.append(blocks[j])
                                blocks[j].destroy()
                        if abs(block2_v - block2_v1) > d_velocity:
                            if blocks[i] not in blocks_to_remove:
                                blocks_to_remove.append(blocks[i])
                                blocks[i].destroy()
                blocks[i].move()
                blocks[i].draw()

            score_text.add_text("SCORE: " + str(self.score), 20, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            score_text.draw()

            birds_remaining.add_text("BIRDS REMAINING: " + str(len(birds)), 20, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            birds_remaining.draw()

            pigs_remaining.add_text("PIGS REMAINING: " + str(len(pigs)), 20, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            pigs_remaining.draw()

            pygame.display.update()

            if all_rest(pigs, birds, blocks):
                for pig in pigs_to_remove:
                    if pig in pigs:
                        pigs.remove(pig)
                        self.score += 100

                for block in blocks_to_remove:
                    if block in blocks:
                        blocks.remove(block)
                        self.score += 50
                pigs_to_remove = []
                blocks_to_remove = []
            clock.tick(60)