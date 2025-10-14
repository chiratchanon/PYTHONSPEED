import pygame
import sys
import random

#>> Setup <<

# Configurations
pygame.init() # Initialize pygame
clock = pygame.time.Clock()
Mute = False

# Screen
screen_width, screen_height = 800, 600
display_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PYTHON SPEEDTYPE v0.1")

# -- Game States --
# We use an enum-like pattern for clarity
class GameState:
    MAIN_MENU = 1
    SETTING = 2
    DIFFICULTY_SELECT = 3
    PLAYING = 4
    GAME_OVER = 5

current_state = GameState.MAIN_MENU

# -- Asset --
background_image = pygame.image.load("Images/Background.png").convert()
button_surface = pygame.image.load("Images/Button.png").convert_alpha()
mute_surface = pygame.image.load("Images/Mute.png").convert_alpha()
unmute_surface = pygame.image.load("Images/Unmute.png").convert_alpha()

# Scale assets
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
button_surface = pygame.transform.scale(button_surface, (180, 50))
mute_surface  = pygame.transform.scale(mute_surface, (30, 30))
unmute_surface  = pygame.transform.scale(unmute_surface, (30, 30))

# BGM
pygame.mixer.init()
BGM = pygame.mixer.music.load("BGM.mp3")
BGM = pygame.mixer.music.set_volume(0.5)
BGM = pygame.mixer.music.play(loops=-1)

# SFX
click_sound = pygame.mixer.Sound("SFXs/Click.mp3")
fail_sound = pygame.mixer.Sound("SFXs/Fail.mp3")
wrong_sound = pygame.mixer.Sound("SFXs/Wrong.mp3")
click_sound.set_volume(.25)
fail_sound.set_volume(.25)
wrong_sound.set_volume(.05)

# -- Colors & Fonts --
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (50, 255, 50)
COLOR_RED = (255, 50, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (100, 150, 255)
COLOR_ACTIVE_INPUT = pygame.Color('dodgerblue2')
COLOR_INACTIVE_INPUT = pygame.Color('lightskyblue3')

title_font = pygame.font.SysFont("comicsansms", 40)
main_font = pygame.font.SysFont("comicsansms", 25)
game_font = pygame.font.SysFont("consolas", 40)
ui_font = pygame.font.SysFont("comicsansms", 25)

# -- Button Class --
class Button():
    def __init__(self, image, x_pos, y_pos, text_input, text_color, hover_color, font=main_font):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.base_color, self.hover_color = text_color, hover_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        click_sound.play()
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# Create Buttons for all menus
play_button = Button(button_surface, screen_width / 2, 300, "PLAY", COLOR_WHITE, COLOR_GREEN)
setting_button = Button(button_surface, screen_width / 2, 400, "SETTING", COLOR_WHITE, COLOR_WHITE)
quit_button = Button(button_surface, screen_width / 2, 500, "QUIT", COLOR_WHITE, COLOR_RED)

easy_button = Button(button_surface, screen_width / 2, 300, "EASY", COLOR_WHITE, COLOR_GREEN)
medium_button = Button(button_surface, screen_width / 2, 400, "MEDIUM", COLOR_WHITE, COLOR_YELLOW)
hard_button = Button(button_surface, screen_width / 2, 500, "HARD", COLOR_WHITE, COLOR_RED)

retry_button = Button(button_surface, screen_width / 2, 350, "RETRY", COLOR_WHITE, COLOR_GREEN)
menu_button = Button(button_surface, screen_width / 2, 450, "MENU", COLOR_WHITE, COLOR_GREEN)

return_button = Button(button_surface, 120, 550, "RETURN", COLOR_RED, COLOR_RED)

mute_button = Button(mute_surface, 750, 550, "", COLOR_WHITE, COLOR_GREEN)
unmute_button = Button(unmute_surface, 750, 550, "", COLOR_WHITE, COLOR_GREEN)

#>> Speed Typing Gameplay Variables <<
# Expanded word lists
easy_words = ["code", "font", "game", "java", "list", "loop", "text", "user", "run", "bug", "key", "data"]
medium_words = ["python", "pygame", "event", "string", "player", "sprite", "button", "while", "return", "class", "object", "render", "update"]
hard_words = ["algorithm", "function", "variable", "conditional", "recursion", "debugger", "instance", "polymorphism", "encapsulation", "inheritance", "asynchronous", "framework", "library"]
# random_words = easy_words + medium_words + hard_words

# Difficulty settings: {word_list, time_limit}
difficulty_settings = {
    "EASY": (easy_words, 5),
    "MEDIUM": (medium_words, 4.25),
    "HARD": (hard_words, 3.5)
}

current_difficulty = "MEDIUM" # Default
word_list = []
word_time_limit = 5

# Game state variables
current_word = ""
score = 0
lives = 3
input_text = ''
current_word_start_time = 0
input_box = pygame.Rect(screen_width/2 - 300, 500, 600, 50)


# Function to reset and start a new game
def start_new_game(difficulty):
    global current_difficulty, word_list, word_time_limit, current_word
    global score, lives, input_text, current_word_start_time, current_state

    current_difficulty = difficulty
    word_list, word_time_limit = difficulty_settings[difficulty]
    random.shuffle(word_list) # Shuffle words for variety
    
    score = 0
    lives = 3
    input_text = ''
    current_word = random.choice(word_list)
    current_word_start_time = pygame.time.get_ticks()
    current_state = GameState.PLAYING

#>> Main Game Loop <<
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    display_screen.blit(background_image, (0, 0))
    if Mute == False:
        BGM = pygame.mixer.music.set_volume(0.5)
        unmute_button.update(display_screen)
    elif Mute == True:
        BGM = pygame.mixer.music.set_volume(0)
        mute_button.update(display_screen)
        
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # if click_sound: click_sound.play()
            if mute_button.check_for_input(mouse_pos):
                if Mute == True:
                    Mute = False
                elif Mute == False:
                    Mute = True

                 
            print(Mute)
            if current_state == GameState.MAIN_MENU:
                if play_button.check_for_input(mouse_pos):
                    current_state = GameState.DIFFICULTY_SELECT
                if setting_button.check_for_input(mouse_pos):
                    current_state = GameState.SETTING
                if quit_button.check_for_input(mouse_pos):
                    running = False
                    
            elif current_state == GameState.SETTING:
                if return_button.check_for_input(mouse_pos):
                    current_state = GameState.MAIN_MENU

            elif current_state == GameState.DIFFICULTY_SELECT:
                if easy_button.check_for_input(mouse_pos):
                    start_new_game("EASY")
                if medium_button.check_for_input(mouse_pos):
                    start_new_game("MEDIUM")
                if hard_button.check_for_input(mouse_pos):
                    start_new_game("HARD")
                if return_button.check_for_input(mouse_pos):
                    current_state = GameState.MAIN_MENU

            elif current_state == GameState.GAME_OVER:
                if retry_button.check_for_input(mouse_pos):
                    start_new_game(current_difficulty) # Retry with the same difficulty
                if menu_button.check_for_input(mouse_pos):
                    current_state = GameState.MAIN_MENU

        if current_state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN:
                click_sound.play()
                if event.key == pygame.K_RETURN:
                    if input_text.strip().lower() == current_word:
                        score += len(current_word) # Score based on word length
                        current_word = random.choice(word_list)
                        current_word_start_time = pygame.time.get_ticks() # Reset timer
                        if lives >= 3:
                            pass
                        else:
                            lives += 1
                    else:
                        wrong_sound.play()
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    
    # --- Game Logic & State Updates ---
    if current_state == GameState.PLAYING:
        elapsed_time = (pygame.time.get_ticks() - current_word_start_time) / 1000
        if elapsed_time > word_time_limit:
            fail_sound.play()
            lives -= 1
            current_word = random.choice(word_list)
            current_word_start_time = pygame.time.get_ticks() # Reset timer
            if lives <= 0:
                current_state = GameState.GAME_OVER

    # --- Drawing to Screen based on State ---
    if current_state == GameState.MAIN_MENU:
        title_text = title_font.render("PYTHON SPEEDTYPE", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(screen_width/2, 150))
        display_screen.blit(title_text, title_rect)
        for button in [play_button, setting_button ,quit_button]:
            button.change_color(mouse_pos)
            button.update(display_screen)

    elif current_state == GameState.SETTING:
        title_text = title_font.render("Setting", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(screen_width/2, 120))
        display_screen.blit(title_text, title_rect)
        for button in [return_button]:
            button.change_color(mouse_pos)
            button.update(display_screen)
        
    elif current_state == GameState.DIFFICULTY_SELECT:
        title_text = title_font.render("Select Difficulty", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(screen_width/2, 120))
        display_screen.blit(title_text, title_rect)
        for button in [easy_button, medium_button, hard_button, return_button]:
            button.change_color(mouse_pos)
            button.update(display_screen)

    elif current_state == GameState.GAME_OVER:
        game_over_text = title_font.render("GAME OVER", True, COLOR_RED)
        score_text = main_font.render(f"Final Score: {score}", True, COLOR_WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen_width/2, 150))
        score_rect = score_text.get_rect(center=(screen_width/2, 220))
        display_screen.blit(game_over_text, game_over_rect)
        display_screen.blit(score_text, score_rect)
        for button in [retry_button, menu_button]:
            button.change_color(mouse_pos)
            button.update(display_screen)

    elif current_state == GameState.PLAYING:
        # Draw Score and Lives
        score_surface = ui_font.render(f"Score: {score}", True, COLOR_WHITE)
        lives_surface = ui_font.render(f"Lives: {lives}", True, COLOR_WHITE)
        display_screen.blit(score_surface, (20, 20))
        display_screen.blit(lives_surface, (screen_width - lives_surface.get_width() - 20, 20))

        # Draw the word to type
        word_surface = game_font.render(current_word, True, COLOR_YELLOW)
        word_rect = word_surface.get_rect(center=(screen_width/2, 250))
        display_screen.blit(word_surface, word_rect)

        # Draw the input box and typed text
        pygame.draw.rect(display_screen, COLOR_ACTIVE_INPUT, input_box, 2, border_radius=5)
        input_surface = game_font.render(input_text, True, COLOR_WHITE)
        display_screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

        # Draw Timer Bar
        time_left_ratio = max(0, 1 - (elapsed_time / word_time_limit))
        timer_bar_width = (input_box.width - 4) * time_left_ratio
        timer_color = COLOR_GREEN if time_left_ratio > 2 else COLOR_RED
        timer_bar_rect = pygame.Rect(input_box.x + 2, input_box.y - 20, timer_bar_width, 10)
        pygame.draw.rect(display_screen, timer_color, timer_bar_rect, border_radius=5)


    # Update the full display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
