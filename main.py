import pygame, sys, random, asyncio

#SETUP
pygame.init() # Initialize pygame
# clock = pygame.time.Clock() # No longer needed for the web version

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
# NOTE: Make sure your asset paths (Images/, SFXs/, etc.) are correct!
background_image = pygame.image.load("Images/Background.png").convert_alpha()
title_image = pygame.image.load("Images/Title.png").convert_alpha()
button_surface = pygame.image.load("Images/Button.png").convert_alpha()
mute_surface = pygame.image.load("Images/Mute.png").convert_alpha()
unmute_surface = pygame.image.load("Images/Unmute.png").convert_alpha()

# Scale assets
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
title_image = pygame.transform.scale(title_image, (350, 300))
button_surface = pygame.transform.scale(button_surface, (150, 70))
mute_surface  = pygame.transform.scale(mute_surface, (30, 30))
unmute_surface  = pygame.transform.scale(unmute_surface, (30, 30))

# BGMs
pygame.mixer.init()
BGM = pygame.mixer.music.load("BGM.ogg")
BGM = pygame.mixer.music.set_volume(0.5)
BGM = pygame.mixer.music.play(loops=-1)

# SFX
click_sound = pygame.mixer.Sound("SFXs/Click.ogg")
fail_sound = pygame.mixer.Sound("SFXs/Fail.ogg")
wrong_sound = pygame.mixer.Sound("SFXs/Wrong.ogg")
click_sound.set_volume(.25)
fail_sound.set_volume(.25)
wrong_sound.set_volume(.05)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (50, 255, 50)
COLOR_RED = (255, 50, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (100, 150, 255)
COLOR_ACTIVE_INPUT = pygame.Color('dodgerblue2')
COLOR_INACTIVE_INPUT = pygame.Color('lightskyblue3')

# --- FONT LOADING CHANGED ---
# You can't use SysFont in the browser.
# You must load a font file (like .ttf or .otf)
# 1. Create a folder (e.g., "Fonts")
# 2. Add a font file (e.g., "ComicNeue-Regular.ttf")
# 3. Update the path below to match your file.
try:
    # Update this path to your font file
    font_path = "Fonts/ComicNeue-Regular.ttf" 
    title_font = pygame.font.Font(font_path, 40)
    main_font = pygame.font.Font(font_path, 25)
    game_font = pygame.font.Font(font_path, 40)
    ui_font = pygame.font.Font(font_path, 25)
except FileNotFoundError:
    print("Font file not found! Using default font.")
    # Fallback to default Pygame font if file is missing
    title_font = pygame.font.Font(None, 50)
    main_font = pygame.font.Font(None, 35)
    game_font = pygame.font.Font(None, 50)
    ui_font = pygame.font.Font(None, 35)


#Button
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
play_button = Button(button_surface, screen_width / 2, 350, "PLAY", COLOR_WHITE, COLOR_GREEN, font=main_font)
setting_button = Button(button_surface, screen_width / 2, 425, "SETTING", COLOR_WHITE, COLOR_GREEN, font=main_font)
quit_button = Button(button_surface, screen_width / 2, 500, "QUIT", COLOR_WHITE, COLOR_RED, font=main_font)

easy_button = Button(button_surface, screen_width / 2, 350, "EASY", COLOR_WHITE, COLOR_GREEN, font=main_font)
medium_button = Button(button_surface, screen_width / 2, 425, "MEDIUM", COLOR_WHITE, COLOR_YELLOW, font=main_font)
hard_button = Button(button_surface, screen_width / 2, 500, "HARD", COLOR_WHITE, COLOR_RED, font=main_font)

retry_button = Button(button_surface, screen_width / 2, 325, "RETRY", COLOR_WHITE, COLOR_GREEN, font=main_font)
menu_button = Button(button_surface, screen_width / 2, 400, "MENU", COLOR_WHITE, COLOR_GREEN, font=main_font)

return_button = Button(button_surface, 120, 550, "RETURN", COLOR_RED, COLOR_RED, font=main_font)

mute_button = Button(mute_surface, 750, 550, "", COLOR_WHITE, COLOR_GREEN, font=main_font)
unmute_button = Button(unmute_surface, 750, 550, "", COLOR_WHITE, COLOR_GREEN, font=main_font)

#Words
easy_words = ["def()", "sum()", "print()", "True", "False", "if", "elif", "else", "and", "or", "continue", "break"]
medium_words = easy_words + ["return", "self", "class", "import", "append()", "add()", "for", "while", "in", "range()", "try", "expect", "from"]
hard_words = medium_words + ["await", "pass", "None", "lambda", "assert", "del", "global", "async", "yield", "with", "len()", "str()", "int()", "float()", "list()", "dict()", "sum()", "max()", "min()", "abs()", "round()"]
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
    # These variables are modified by this function, so they must be global
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


# --- MAIN ASYNC LOOP ---
# This is the new structure for the web
async def main():
    # Declare all variables from the *outer* scope that this loop *changes*
    global running, Mute, current_state, mouse_pos
    global current_word, score, lives, input_text, current_word_start_time, BGM

    running = True
    Mute = False
    mouse_pos = (0, 0)

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
                if mute_button.check_for_input(mouse_pos) or unmute_button.check_for_input(mouse_pos):
                    if Mute == True:
                        Mute = False
                    elif Mute == False:
                        Mute = True

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
                        if input_text.strip() == current_word:
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
            title_rect = title_image.get_rect(center=(screen_width/2, 150))
            display_screen.blit(title_image, title_rect)
            for button in [play_button, setting_button]:
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
            #score 
            score_surface = ui_font.render(f"Score: {score}", True, COLOR_WHITE)
            lives_surface = ui_font.render(f"Lives: {lives}", True, COLOR_WHITE)
            display_screen.blit(score_surface, (20, 20))
            display_screen.blit(lives_surface, (screen_width - lives_surface.get_width() - 20, 20))

            #words
            word_surface = game_font.render(current_word, True, COLOR_YELLOW)
            word_rect = word_surface.get_rect(center=(screen_width/2, 250))
            display_screen.blit(word_surface, word_rect)

            #input box
            pygame.draw.rect(display_screen, COLOR_ACTIVE_INPUT, input_box, 2, border_radius=5)
            input_surface = game_font.render(input_text, True, COLOR_WHITE)
            display_screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

            #timer
            time_left_ratio = max(0, 1 - (elapsed_time / word_time_limit))
            timer_bar_width = (input_box.width - 4) * time_left_ratio

            if time_left_ratio > 0.5:
                r = int((1.0 - time_left_ratio) * 2 * 255)
                g = 255
            else:
                r = 255
                g = int(time_left_ratio * 2 * 255)
            timer_color = (r, g, 50)
            
            timer_bar_rect = pygame.Rect(input_box.x + 2, input_box.y - 20, timer_bar_width, 10)
            pygame.draw.rect(display_screen, timer_color, timer_bar_rect, border_radius=5)


        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
