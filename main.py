import pygame, random, asyncio

#SETUP
pygame.init()

# Screen
screen_width, screen_height = 800, 600
display_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PYTHON SPEEDTYPE v0.1")

# -- Game States --
# We use an enum-like pattern for clarity
class GameState:
    MAIN_MENU = 1
    DIFFICULTY_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4

current_state = GameState.MAIN_MENU

Background = ["GRASS_PLAIN", "FOREST", "MUSHROOM_FOREST", "UNDERGROUND_DUNGEON", "CRYSTALIZED_CAVE", "DRAGON_HIDEOUT"]
current_place = Background[1]


def load_image(path):
    """Loads an image and handles potential FileNotFoundError."""
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Error loading image: {path} - {e}")
        # Create a placeholder surface
        surface = pygame.Surface((100, 100))
        surface.fill(COLOR_RED)
        text = pygame.font.Font(None, 20).render("Missing", True, COLOR_WHITE)
        text_rect = text.get_rect(center=(50, 50))
        surface.blit(text, text_rect)
        return surface

def load_sound(path):
    """Loads a sound and handles potential FileNotFoundError."""
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error as e:
        print(f"Error loading sound: {path} - {e}")
        # Return a dummy sound object
        return pygame.mixer.Sound(buffer=b"") # Empty sound

#COLOURs
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (50, 255, 50)
COLOR_RED = (255, 50, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (100, 150, 255)
COLOR_ACTIVE_INPUT = pygame.Color('dodgerblue2')
COLOR_INACTIVE_INPUT = pygame.Color('lightskyblue3')

# Load images with error handling
GRASS_PLAIN_SURFACE = load_image("Images/Backgrounds/Grass_Plain.png")
FOREST_SURFACE = load_image("Images/Backgrounds/FOREST.jpg")
MUSHROOM_FOREST_SURFACE = load_image("Images/Backgrounds/Mushroom_Forest.jpg")
UNDERGROUND_DUNGEON_SURFACE = load_image("Images/Backgrounds/Underground_Dungeon.jpg")
CRYSTALIZED_CAVE_SURFACE = load_image("Images/Backgrounds/Crystalized_Cave.jpg")
DRAGON_HIDEOUT_SURFACE = load_image("Images/Backgrounds/Dragons_Hideout.jpg")

title_image = load_image("Images/Title.png")
button_surface = load_image("Images/Button.png")
mute_surface = load_image("Images/Mute.png")
unmute_surface = load_image("Images/Unmute.png")

# Scale assets
GRASS_PLAIN_IMAGE = pygame.transform.scale(GRASS_PLAIN_SURFACE, (screen_width, screen_height))
FOREST_IMAGE = pygame.transform.scale(FOREST_SURFACE, (screen_width, screen_height))
MUSHROOM_FOREST_IMAGE = pygame.transform.scale(MUSHROOM_FOREST_SURFACE, (screen_width, screen_height))
UNDERGROUND_DUNGEON_IMAGE = pygame.transform.scale(UNDERGROUND_DUNGEON_SURFACE, (screen_width, screen_height))
CRYSTALIZED_CAVE_IMAGE = pygame.transform.scale(CRYSTALIZED_CAVE_SURFACE, (screen_width, screen_height))
DRAGON_HIDEOUT_IMAGE = pygame.transform.scale(DRAGON_HIDEOUT_SURFACE, (screen_width, screen_height))

title_image = pygame.transform.scale(title_image, (350, 300))
button_surface = pygame.transform.scale(button_surface, (150, 70))
mute_surface  = pygame.transform.scale(mute_surface, (35, 35))
unmute_surface  = pygame.transform.scale(unmute_surface, (35, 35))

# BGMs
pygame.mixer.init() #Setup mixer

#Background Music
MAIN_THEME = "BGMs/8.ogg"
BGMs = {
    "GRASS_PLAIN": "BGMs/5.ogg",
    "FOREST": "BGMs/6.ogg",
    "MUSHROOM_FOREST": "BGMs/3.ogg",
    "UNDERGROUND_DUNGEON": "BGMs/0.ogg",
    "CRYSTALIZED_CAVE": "BGMs/2.ogg",
    "DRAGON_HIDEOUT": "BGMs/1.ogg"
}

# Load main theme, handle error
try:
    pygame.mixer.music.load(MAIN_THEME)
    current_music = MAIN_THEME
except pygame.error as e:
    print(f"Error loading main theme: {MAIN_THEME} - {e}")
    current_music = None

# SFX
fail_sound = load_sound("SFXs/Fail.ogg")
wrong_sound = load_sound("SFXs/Wrong.ogg")
heal_sound = load_sound("SFXs/Heal.ogg")

# --- New Keypress Sound Management ---
# 1. Load all sound objects
#    NOTE: Make sure you have these files in your SFXs/ folder!
click_sound_1 = load_sound("SFXs/Click.ogg")
click_sound_1.set_volume(.25)

# 3. Create a list to cycle through
#    (Name for display, Sound Object)
keypress_sounds = [
    ("Click", click_sound_1),
]
current_sound_index = 0
click_sound = keypress_sounds[current_sound_index][1] # This is the global variable the game will use
# --- End of New Sound Management ---

fail_sound.set_volume(.25)
wrong_sound.set_volume(.05)
heal_sound.set_volume(.25)

#Sprite

# --- FONT LOADING ---
# Use default system font by passing None
title_font = pygame.font.Font(None, 50)
main_font = pygame.font.Font(None, 35)
game_font = pygame.font.Font(None, 50)
ui_font = pygame.font.Font(None, 35)

#Button
class Button():
    def __init__(self, image, x_pos, y_pos, text_input, text_color, hover_color, font=main_font, hover_scale=1.1):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.text_input = text_input
        self.base_color, self.hover_color = text_color, hover_color
        self.hover_scale = hover_scale

        # --- Base (non-hovered) assets ---
        self.image_base = image
        self.rect_base = self.image_base.get_rect(center=(self.x_pos, self.y_pos))
        self.text_base = self.font.render(self.text_input, True, self.base_color)
        self.text_rect_base = self.text_base.get_rect(center=(self.x_pos, self.y_pos))

        # --- Hovered assets ---
        # Calculate new size
        hover_size = (int(self.image_base.get_width() * self.hover_scale), int(self.image_base.get_height() * self.hover_scale))
        # Scale the image
        self.image_hover = pygame.transform.scale(self.image_base, hover_size)
        self.rect_hover = self.image_hover.get_rect(center=(self.x_pos, self.y_pos))
        self.text_hover = self.font.render(self.text_input, True, self.hover_color)
        self.text_rect_hover = self.text_hover.get_rect(center=(self.x_pos, self.y_pos))

        # --- Current state ---
        # These will be swapped by update_visuals()
        self.image = self.image_base
        self.rect = self.rect_base
        self.text = self.text_base
        self.text_rect = self.text_rect_base
        
        # Use the *larger* hover rect for collision detection
        # This prevents the button from "flickering" at the edges
        self.collision_rect = self.rect_hover.copy()

    def update(self, screen):
        # Draw the current image and text
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        # Use the static collision_rect for the check
        if self.collision_rect.collidepoint(position):
            click_sound.play() # Play sound only on a successful click
            return True
        return False

    def change_color(self, position):
        # This method now also handles scaling
        if self.collision_rect.collidepoint(position):
            # Set to hover state
            self.image = self.image_hover
            self.rect = self.rect_hover
            self.text = self.text_hover
            self.text_rect = self.text_rect_hover
        else:
            # Set to base state
            self.image = self.image_base
            self.rect = self.rect_base
            self.text = self.text_base
            self.text_rect = self.text_rect_base

# Create Buttons for all menus
play_button = Button(button_surface, screen_width / 2, 450, "PLAY", COLOR_WHITE, COLOR_GREEN, font=main_font)

easy_button = Button(button_surface, screen_width / 2, 250, "EASY", COLOR_WHITE, COLOR_GREEN, font=main_font)
medium_button = Button(button_surface, screen_width / 2, 325, "MEDIUM", COLOR_WHITE, COLOR_YELLOW, font=main_font)
hard_button = Button(button_surface, screen_width / 2, 400, "HARD", COLOR_WHITE, COLOR_RED, font=main_font)

retry_button = Button(button_surface, screen_width / 2, 325, "RETRY", COLOR_WHITE, COLOR_GREEN, font=main_font)
menu_button = Button(button_surface, screen_width / 2, 400, "MENU", COLOR_WHITE, COLOR_GREEN, font=main_font)

return_button = Button(button_surface, 120, 550, "RETURN", COLOR_RED, COLOR_RED, font=main_font)

mute_button = Button(mute_surface, 755, 565, "", COLOR_WHITE, COLOR_GREEN, font=main_font)
unmute_button = Button(unmute_surface, 755, 565, "", COLOR_WHITE, COLOR_GREEN, font=main_font)

#Words
easy_words = ["return","for", "while", "if", "elif", "else", "and", "or", "continue", "break", "import"]
medium_words = easy_words + ["self", "class", "in", "try", "expect", "from", "True", "False","await", "pass", "None", "lambda", "assert", "del", "global", "async", "yield", "with","asyncio"]
hard_words = medium_words + ["def()", "sum()", "print()", "append()", "add()", "range()", "len()", "str()", "int()", "float()", "list()", "dict()", "sum()", "max()", "min()", "abs()", "round()"]
special_word = [ "__init__", "__repr__", "__str__", "__name__", "__main__", "__import__", "__await__", "StopIteration", "NotImplementedError", "ZeroDivisionError", "AttributeError", "FileNotFoundError", "StopAsyncIteration", "isinstance", "issubclass"]

difficulty_settings = {
    "EASY": (easy_words, 5),
    "MEDIUM": (medium_words, 4),
    "HARD": (hard_words, 3)
}

current_difficulty = "MEDIUM" # Default
word_list = []
word_time_limit = 5
special = False
heal = False

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
    global current_difficulty, word_list, word_time_limit, current_word, score, lives, input_text, current_word_start_time, current_state, current_music

    current_difficulty = difficulty
    word_list, word_time_limit = difficulty_settings[difficulty]
    random.shuffle(word_list) # Shuffle words for variety
    
    score = 0
    lives = 3
    input_text = ''
    current_word = random.choice(word_list)
    current_word_start_time = pygame.time.get_ticks()
    current_state = GameState.PLAYING
    
    music_to_play = BGMs.get(current_place, MAIN_THEME) 
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_to_play)
        pygame.mixer.music.play(-1)
        current_music = music_to_play
        print(f"Playing music: {current_music}")
    except pygame.error as e:
        print(f"Error playing music: {music_to_play} - {e}")
        current_music = None


# Gameplay Loop
async def main():
    # Declare all variables from the *outer* scope that this loop *changes*
    global running, Mute, current_state, mouse_pos, current_place, current_word, score, lives, input_text, current_word_start_time, current_music
    global special, heal, current_sound_index, click_sound # <-- ADDED sound globals

    running = True
    Mute = False
    mouse_pos = (0, 0)

    if current_music:
        pygame.mixer.music.play(-1)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        if current_state != GameState.PLAYING:
            display_screen.blit(GRASS_PLAIN_IMAGE, (0, 0))          
            
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

                elif current_state == GameState.DIFFICULTY_SELECT:
                    if easy_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game("EASY")
                    if medium_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game("MEDIUM")
                    if hard_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game("HARD")
                    if return_button.check_for_input(mouse_pos):
                        current_state = GameState.MAIN_MENU

                elif current_state == GameState.GAME_OVER:
                    if retry_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game(current_difficulty) # Retry with the same difficulty
                    if menu_button.check_for_input(mouse_pos):
                        current_state = GameState.MAIN_MENU
                        if current_music != MAIN_THEME and current_music is not None:
                            try:
                                pygame.mixer.music.load(MAIN_THEME)
                                pygame.mixer.music.play(-1)
                                current_music = MAIN_THEME
                            except pygame.error as e:
                                print(f"Error loading main theme: {MAIN_THEME} - {e}")
                                current_music = None
    
            if current_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    click_sound.play() # Uses the globally selected sound
                    if event.key == pygame.K_RETURN:
                        if input_text.strip() == current_word:
                            if special:
                                score += (len(current_word))*2
                                special = False
                                lives = 3
                            else:
                                score += len(current_word)
                            if heal:
                                heal_sound.play()
                                if lives < 3:
                                    lives += 1
                                heal = False
                            current_word = random.choice(word_list)
                            if random.randint(1, 10) == 1:
                                chances = random.randint(1,2)
                                if chances == 1:
                                    current_word = random.choice(special_word)
                                    special = True
                                elif chances == 2:
                                    heal = True
                            current_word_start_time = pygame.time.get_ticks() # Reset timer
                        else:
                            wrong_sound.play()
                        input_text = '' # Clear input text on enter, regardless of correct/wrong
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
        
        # --- Game Logic & State Updates ---
        if current_state == GameState.PLAYING:
            if current_place == "GRASS_PLAIN":
                display_screen.blit(GRASS_PLAIN_IMAGE, (0, 0))
            elif current_place == "FOREST":
                display_screen.blit(FOREST_IMAGE, (0, 0))
            elif current_place == "MUSHROOM_FOREST":
                display_screen.blit(MUSHROOM_FOREST_IMAGE, (0, 0))
            elif current_place == "UNDERGROUND_DUNGEON":
                display_screen.blit(UNDERGROUND_DUNGEON_IMAGE, (0, 0))
            elif current_place == "CRYSTALIZED_CAVE":
                display_screen.blit(CRYSTALIZED_CAVE_IMAGE, (0, 0))
            elif current_place == "DRAGON_HIDEOUT":
                display_screen.blit(DRAGON_HIDEOUT_IMAGE, (0, 0))
    
            elapsed_time = (pygame.time.get_ticks() - current_word_start_time) / 1000
            if elapsed_time > word_time_limit:
                fail_sound.play()
                lives -= 1
                input_text = ''
                current_word = random.choice(word_list)
                special = False
                heal = False
                if random.randint(1, 5) == 1:
                    chances = random.randint(1,2)
                    if chances == 1:
                        current_word = random.choice(special_word)
                        special = True
                    elif chances == 2:
                        heal = True
                current_word_start_time = pygame.time.get_ticks() # Reset timer
                if lives <= 0:
                    current_state = GameState.GAME_OVER

        # --- Drawing to Screen based on State ---
        if current_state == GameState.MAIN_MENU:
            title_rect = title_image.get_rect(center=(screen_width/2, 150))
            display_screen.blit(title_image, title_rect)
            for button in [play_button]: # Added quit
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
            if current_music:
                pygame.mixer.music.stop()
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
            lives_surface = ui_font.render(f"Lives: {lives}", True, COLOR_RED)
            display_screen.blit(score_surface, (20, 20))
            display_screen.blit(lives_surface, (screen_width - lives_surface.get_width() - 20, 20))

            #words
            word_color = COLOR_YELLOW
            if heal:
                word_color = COLOR_GREEN
            if special:
                word_color = COLOR_RED

            # Create a semi-transparent background for the word
            word_surface = game_font.render(current_word, True, word_color)
            word_bg_rect = word_surface.get_rect(center=(screen_width/2, 250))
            word_bg_rect.inflate_ip(20, 10) # Add padding
            
            # Create a separate surface for transparency
            bg_surface = pygame.Surface(word_bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 128)) # Black with 128 alpha
            display_screen.blit(bg_surface, word_bg_rect.topleft)

            # Blit the word on top of the transparent bg
            word_rect = word_surface.get_rect(center=word_bg_rect.center)
            display_screen.blit(word_surface, word_rect)


            #input box
            pygame.draw.rect(display_screen, COLOR_ACTIVE_INPUT, input_box, 2, border_radius=5)
            input_surface = game_font.render(input_text, True, COLOR_WHITE)
            display_screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

            #timer
            time_left_ratio = max(0, 1 - (elapsed_time / word_time_limit))
            timer_bar_width = (input_box.width - 4) * time_left_ratio

            # Interpolate color from Green to Red
            if time_left_ratio > 0.5:
                # Green to Yellow
                r = int((1.0 - time_left_ratio) * 2 * 255)
                g = 255
            else:
                # Yellow to Red
                r = 255
                g = int(time_left_ratio * 2 * 255)
            timer_color = (r, g, 50)
            
            timer_bar_rect = pygame.Rect(input_box.x + 2, input_box.y - 20, timer_bar_width, 10)
            pygame.draw.rect(display_screen, timer_color, timer_bar_rect, border_radius=5)

        
        # Mute button is drawn last, on top of everything
        if Mute == False:
            unmute_button.update(display_screen)
            if current_music:
                pygame.mixer.music.set_volume(0.35)
        elif Mute == True:
            mute_button.update(display_screen)
            if current_music:
                pygame.mixer.music.set_volume(0)

        pygame.display.update()
        await asyncio.sleep(0) # Give control back to the event loop

if __name__ == "__main__":
    asyncio.run(main())
