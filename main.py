import pygame, random, asyncio # Import modules ต่างๆ

# SETUP init
pygame.init()

screen_width, screen_height = 800, 600 # Screen size
display_screen = pygame.display.set_mode((screen_width, screen_height)) # Setup หน้าจอ
pygame.display.set_caption("PYTHON SPEEDTYPE v0.1") # ชื่อเกม

# หน้าต่างเกม
class GameState:
    MAIN_MENU = 1
    DIFFICULTY_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4

current_state = GameState.MAIN_MENU # หน้าต่างเกม = หน้าเมนูหลัก

# พื้นหลังต่างๆ
Background = ["GRASS_PLAIN", "FOREST", "MUSHROOM_FOREST", "UNDERGROUND_DUNGEON", "CRYSTALIZED_CAVE", "DRAGON_HIDEOUT"]
current_place = Background[1] # Set พื้นหลังหลัก = GRASS PLAIN


def load_image(path): # ฟังชั่นในการโหลดไฟล์รูปภาพ
    """ docstring """
    try: 
        image = pygame.image.load(path).convert_alpha()
        return image
        # ถ้าหาไฟล์ Image เจอ > return image
    except pygame.error as e:
        print(f"Error loading image: {path} - {e}") # แจ้งเตือน Error
        surface = pygame.Surface((100, 100)) # สร้าง Surface ใหม่
        surface.fill(COLOR_RED)
        text = pygame.font.Font(None, 20).render("Missing", True, COLOR_WHITE)
        text_rect = text.get_rect(center=(50, 50))
        surface.blit(text, text_rect)
        return surface
        # ถ้าหาไฟล์ Image ไม่เจอ > สร้าง Surface ใหม่ > return surface

def load_sound(path): # ฟังชั่นในการโหลดไฟล์เสียง
    """ docstring """
    try:
        sound = pygame.mixer.Sound(path)
        return sound
        # ถ้าหาไฟล์เสียงเจอ > return sound
    except pygame.error as e:
        print(f"Error loading sound: {path} - {e}")
        return pygame.mixer.Sound(buffer=b"") # Return เสียงเปล่าให้ไม่ Error

# COLOURs - สีต่างๆ
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (50, 255, 50)
COLOR_RED = (255, 50, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (100, 150, 255)
COLOR_ACTIVE_INPUT = pygame.Color('dodgerblue2')
COLOR_INACTIVE_INPUT = pygame.Color('lightskyblue3')

# พื้นหลัง
GRASS_PLAIN_SURFACE = load_image("Images/Backgrounds/Grass_Plain.png")
FOREST_SURFACE = load_image("Images/Backgrounds/FOREST.jpg")
MUSHROOM_FOREST_SURFACE = load_image("Images/Backgrounds/Mushroom_Forest.jpg")
UNDERGROUND_DUNGEON_SURFACE = load_image("Images/Backgrounds/Underground_Dungeon.jpg")
CRYSTALIZED_CAVE_SURFACE = load_image("Images/Backgrounds/Crystalized_Cave.jpg")
DRAGON_HIDEOUT_SURFACE = load_image("Images/Backgrounds/Dragons_Hideout.jpg")

# รูปภาพปุ่มหลักๆ
title_image = load_image("Images/Title.png")
button_surface = load_image("Images/Button.png")
mute_surface = load_image("Images/Mute.png")
unmute_surface = load_image("Images/Unmute.png")

# ปรับขนาดภาพพื้นหลังให้ตรงกับหน้าจอหลัก(display_screen)
BackgroundImages = {
    "GRASS_PLAIN" : pygame.transform.scale(GRASS_PLAIN_SURFACE, (screen_width, screen_height)),
    "FOREST" : pygame.transform.scale(FOREST_SURFACE, (screen_width, screen_height)),
    "MUSHROOM_FOREST" : pygame.transform.scale(MUSHROOM_FOREST_SURFACE, (screen_width, screen_height)),
    "UNDERGROUND_DUNGEON" : pygame.transform.scale(UNDERGROUND_DUNGEON_SURFACE, (screen_width, screen_height)),
    "CRYSTALIZED_CAVE" : pygame.transform.scale(CRYSTALIZED_CAVE_SURFACE, (screen_width, screen_height)),
    "DRAGON_HIDEOUT" : pygame.transform.scale(DRAGON_HIDEOUT_SURFACE, (screen_width, screen_height)),
}


# ปรับขนาดภาพของปุ่ม
title_image = pygame.transform.scale(title_image, (350, 300))
button_surface = pygame.transform.scale(button_surface, (150, 70))
mute_surface  = pygame.transform.scale(mute_surface, (35, 35))
unmute_surface  = pygame.transform.scale(unmute_surface, (35, 35))

# เสียงเพลงพื้นหลัง
pygame.mixer.init() # Setup mixer

# เสียงเพลงพื้นหลังทั้งหมด
MAIN_THEME = "BGMs/8.ogg" # เสียงเพลงพื้นหลังหลัก = หน้าเมนู
BGMs = {
    "GRASS_PLAIN": "BGMs/5.ogg",
    "FOREST": "BGMs/6.ogg",
    "MUSHROOM_FOREST": "BGMs/3.ogg",
    "UNDERGROUND_DUNGEON": "BGMs/0.ogg",
    "CRYSTALIZED_CAVE": "BGMs/2.ogg",
    "DRAGON_HIDEOUT": "BGMs/1.ogg"
} # ให้เสียงเพลงสอดคล้องกับพื้นหลัง

pygame.mixer.music.load(MAIN_THEME)
current_music = MAIN_THEME

# เสียง
click_sound = load_sound("SFXs/Click.ogg")
fail_sound = load_sound("SFXs/Fail.ogg")
wrong_sound = load_sound("SFXs/Wrong.ogg")
heal_sound = load_sound("SFXs/Heal.ogg")
# ปรับเสียง
click_sound.set_volume(.25)
fail_sound.set_volume(.25)
wrong_sound.set_volume(.05)
heal_sound.set_volume(.25)

# Set fonts และปรับขนาดของตัวหนังสือ
title_font = pygame.font.Font(None, 50)
main_font = pygame.font.Font(None, 35)
game_font = pygame.font.Font(None, 50)
ui_font = pygame.font.Font(None, 35)

# Function ใช้ในการสร้างปุ่ม
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

        hover_size = (int(self.image_base.get_width() * self.hover_scale), int(self.image_base.get_height() * self.hover_scale))

        self.image_hover = pygame.transform.scale(self.image_base, hover_size)
        self.rect_hover = self.image_hover.get_rect(center=(self.x_pos, self.y_pos))
        self.text_hover = self.font.render(self.text_input, True, self.hover_color)
        self.text_rect_hover = self.text_hover.get_rect(center=(self.x_pos, self.y_pos))

        self.image = self.image_base
        self.rect = self.rect_base
        self.text = self.text_base
        self.text_rect = self.text_rect_base
        
        self.collision_rect = self.rect_hover.copy()

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if self.collision_rect.collidepoint(position):
            click_sound.play()
            return True
        return False

    def change_color(self, position):
        if self.collision_rect.collidepoint(position):
            self.image = self.image_hover
            self.rect = self.rect_hover
            self.text = self.text_hover
            self.text_rect = self.text_rect_hover
        else:
            self.image = self.image_base
            self.rect = self.rect_base
            self.text = self.text_base
            self.text_rect = self.text_rect_base

# สร้างปุ่มโดยใช้ Function Button
play_button = Button(button_surface, screen_width / 2, 450, "PLAY", COLOR_WHITE, COLOR_GREEN, font=main_font)
easy_button = Button(button_surface, screen_width / 2, 250, "EASY", COLOR_WHITE, COLOR_GREEN, font=main_font)
medium_button = Button(button_surface, screen_width / 2, 325, "MEDIUM", COLOR_WHITE, COLOR_YELLOW, font=main_font)
hard_button = Button(button_surface, screen_width / 2, 400, "HARD", COLOR_WHITE, COLOR_RED, font=main_font)
retry_button = Button(button_surface, screen_width / 2, 325, "RETRY", COLOR_WHITE, COLOR_GREEN, font=main_font)
menu_button = Button(button_surface, screen_width / 2, 400, "MENU", COLOR_WHITE, COLOR_GREEN, font=main_font)
return_button = Button(button_surface, 120, 550, "RETURN", COLOR_RED, COLOR_RED, font=main_font)
mute_button = Button(mute_surface, 755, 565, "", COLOR_WHITE, COLOR_GREEN, font=main_font)
unmute_button = Button(unmute_surface, 755, 565, "", COLOR_WHITE, COLOR_GREEN, font=main_font)

#คลังคำศัพท์ตามระดับความยาก
easy_words = ["return","for", "while", "if", "elif", "else", "and", "or", "continue", "break", "import"]
medium_words = easy_words + ["self", "class", "in", "try", "expect", "from", "True", "False","await", "pass", "None", "lambda", "assert", "del", "global", "async", "yield", "with","asyncio"]
hard_words = medium_words + ["def()", "sum()", "print()", "append()", "add()", "range()", "len()", "str()", "int()", "float()", "list()", "dict()", "sum()", "max()", "min()", "abs()", "round()"]
special_word = [ "__init__", "__repr__", "__str__", "__name__", "__main__", "__import__", "__await__", "StopIteration", "NotImplementedError", "ZeroDivisionError", "AttributeError", "FileNotFoundError", "StopAsyncIteration", "isinstance", "issubclass"]

# ระดับความยาก
difficulty_settings = {
    "EASY": (easy_words, 5), 
    "MEDIUM": (medium_words, 4),
    "HARD": (hard_words, 3)
    # ระดับความยาก: (คำศัพท์, เวลาในการพิมพ์)
}

word_list = [] # สร้าง Table เอาไว้เก็บคำศัพท์
word_time_limit = 5 # เวลาในการพิมพ์เพื่อบากคะแนน
special = False # Toggle สำหรับคำพิเศษ
heal = False # Toggle สำหรับคำทีเพิ่มเลือด

current_word = "" # คำศัพท์ขณะเล่น
score = 0 # คะแนนของผู้เล่น
lives = 3 # พลังชีวิต
input_text = '' # Input ของผู้เล่น
current_word_start_time = 0
input_box = pygame.Rect(screen_width/2 - 300, 500, 600, 50) # กล่องสำหรับรองรับ Input ของผุ้เล่น

# ฟังชั่นสำหรับการเริ่มเกม
def start_new_game(difficulty): # รับค่าระดับความยาก
    # รับค่า Variables ต่างๆเข้ามาเพื่อใช้ปรับแต่ง
    global current_difficulty, word_list, word_time_limit, current_word, score, lives, input_text, current_word_start_time, current_state, current_music

    current_difficulty = difficulty
    word_list, word_time_limit = difficulty_settings[difficulty] # Set ให้ตรงกับระดับความยาก
    random.shuffle(word_list) # สุ่มคำใน word_list
    
    score = 0
    lives = 3
    input_text = ''
    current_word = random.choice(word_list) # สุ่มคำใน word_list
    current_word_start_time = pygame.time.get_ticks()
    current_state = GameState.PLAYING # เริ่มเล่น
    
    #ตั้งค่าเสียงเพลงตามพื้นหลัง
    music_to_play = BGMs.get(current_place, MAIN_THEME)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_to_play)
    pygame.mixer.music.play(-1)
    current_music = music_to_play


# ลูป asyncio / ลูปเกมเพลย์หลัก
async def main():
    # รับ Variables
    global running, Mute, current_state, mouse_pos, current_place, current_word, score, lives
    global special, heal, click_sound, input_text, current_word_start_time, current_music

    running = True # เกมเล่นอยู่
    Mute = False # เปิด-ปิด เสียงเพลงพื้นหลัง
    mouse_pos = (0, 0) # ตำแหน่งหลักของเมาส์

    if current_music:
        pygame.mixer.music.play(-1) # เล่นเพลง

    while running: # ถ้าเกมเล่นอยู่
        mouse_pos = pygame.mouse.get_pos() # รับตำแหน่งของ Cursor mouse
        if current_state != GameState.PLAYING: # ถ้าเกมยังไม่เริ่มจะ Blit รูปพื้นหลังหลัก
            display_screen.blit(BackgroundImages["GRASS_PLAIN"], (0, 0))          
            
        # รับ Events ต่างๆ
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ถ้าผุ้เล่นกด ESC
                running = False # หยุดเกม

            if event.type == pygame.MOUSEBUTTONDOWN: # ถ้าผุ้เล่นกดคลิกเมาส์
                if mute_button.check_for_input(mouse_pos) or unmute_button.check_for_input(mouse_pos): # ถ้าตำแหน่งของเมาส์ = ปุ่ม mute
                    if Mute == True:
                        Mute = False
                    elif Mute == False:
                        Mute = True

                if current_state == GameState.MAIN_MENU:# ถ้าผู้เล่นอยู่หน้าเมนู
                    if play_button.check_for_input(mouse_pos): # ถ้าตำแหน่งของเมาส์ = ปุ่ม PLAY
                        current_state = GameState.DIFFICULTY_SELECT

                elif current_state == GameState.DIFFICULTY_SELECT: # ถ้าผู้เล่นอยู่หน้าเลือกระดับความยาก

                    # เลือกระดับคสามยาก
                    if easy_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game("EASY")
                    if medium_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game("MEDIUM")
                    if hard_button.check_for_input(mouse_pos):
                        current_place = random.choice(Background)
                        start_new_game("HARD")
                    if return_button.check_for_input(mouse_pos): # ปุ่มย้อนกลับไปหน้าเมนู
                        current_state = GameState.MAIN_MENU

                elif current_state == GameState.GAME_OVER: # ถ้าผู้เล่นอยู่หน้า Gameover
                    if retry_button.check_for_input(mouse_pos): # ถ้ากดปุ่ม Retry
                        current_place = random.choice(Background)
                        start_new_game(current_difficulty) # เล่นอีกครั้งพร้อมกับระดับความยากที่เลือกครั้งแรก
                    if menu_button.check_for_input(mouse_pos):
                        current_state = GameState.MAIN_MENU
                        if current_music != MAIN_THEME and current_music is not None: # ถ้าเสียงเพลงไม่ใช่เพลงหลักของหน้าเมนู และ Variables ของเสียงเพลงไม่ว่าง
                            pygame.mixer.music.load(MAIN_THEME)
                            pygame.mixer.music.play(-1) # เล่นเพลงพื้นหลังของหน้าเมนู
                            current_music = MAIN_THEME 

            # รับ Input จากคีย์บอร์ด
            if current_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN: # รับ Input ปุ่มที่ผู้เล่นกด
                    click_sound.play() # เล่นเสียงพิมพ์
                    if event.key == pygame.K_RETURN: # กด Enter
                        if input_text.strip() == current_word: # ถ้า Input ตรงกับ คำศัพท์ที่ให้มา

                            time_taken = (pygame.time.get_ticks() - current_word_start_time) / 1000 # เวลาที่ใช้ในการพิมพ์
                            base_score = len(current_word) * 10 # คะแนน = ตัวอักศรทั้งหมด * 10

                            time_ratio = max(0, time_taken) / word_time_limit # เวลาทั้งหมดที่ใช้
                            speed_bonus = 0 # Bonus ความเร็วในการพิมพ์

                            # คำนวนเวลาในการพิมพ์
                            if time_ratio < 0.25:
                                speed_bonus = base_score * 2
                            elif time_ratio < 0.5:
                                speed_bonus = base_score * 1
                            elif time_ratio < 0.75:
                                speed_bonus = base_score * 0.5
                            
                            total_gain = base_score + int(speed_bonus) # รวมคะแนนที่ได้
                            
                            if special: # ถ้าเป็นคำศัพท์พิเศษ
                                total_gain *= 2 # คะแนนที่ได้ * 2
                                score += total_gain # คะแนนทั้งหมด + คะแนนที่ได้
                                special = False # Toggle คำพิเศษ
                                lives = 3 # ฟื้นฟูพลังชีวิตทั้งหมด
                            else: # ถ้าไม่เป็นคำศัพท์พิเศษ
                                score += total_gain # คะแนนทั้งหมด + คะแนนที่ได้

                            if heal: # ถ้าเป็นคำศัพท์ที่เพิ่มพลังชีวิต
                                heal_sound.play() # เล่นเสียง Heal
                                if lives < 3: # ถ้าเลือดน้อยกว่า 3
                                    lives += 1 # บวกเลือด
                                heal = False # Toggle คำฟื้นฟู
                                
                            current_word = random.choice(word_list) # สุ่มคำศัพท์
                            if random.randint(1, 10) == 1: # สุ่ม 1 ใน 10
                                chances = random.randint(1,2) # สุ่ม 1 ใน 2 อีกที
                                if chances == 1: # สุ่มได้ 1 = ศัพท์พิเศษ
                                    current_word = random.choice(special_word)
                                    special = True
                                elif chances == 2: # สุ่มได้ 2 = คำฟื้นฟู
                                    heal = True
                            current_word_start_time = pygame.time.get_ticks() # รีเซ็ตเวลาจำกัด
                        else: # ถ้า Input ไม่ตรงกับ คำศัพท์ที่ให้มา
                            wrong_sound.play() # เล่นเสียงผิด
                        input_text = '' # ลบ Input ออกเพื่อความพร้อมในการพิมพ์คำถัดไป
                    elif event.key == pygame.K_BACKSPACE: # กดปุ่ม Backspace
                        input_text = input_text[:-1] # ลบ Input จากด้านหลังสุดออก 1 ตัว
                    else:
                        input_text += event.unicode
        
        # Logic เกม
        if current_state == GameState.PLAYING: # Logic เกม
            if current_place in BackgroundImages: # ถ้าค่าของ current_place มีอยู่ใน BackgroundImages
                display_screen.blit(BackgroundImages[current_place], (0, 0)) # Blit พื้นหลังตาม current_place
    
            elapsed_time = (pygame.time.get_ticks() - current_word_start_time) / 1000
            if elapsed_time > word_time_limit: # ถ้าเวลามากกว่าที่กำหนด
                fail_sound.play() # เล่นเสียงเวลาหมด
                lives -= 1 # ลบพลังชีวิต
                input_text = '' # ลบ Input ผู้เล่น
                current_word = random.choice(word_list) # สุ่มคำศัพท์
                special = False # Toggle 
                heal = False # Toggle
                if random.randint(1, 5) == 1: # สุ่ม
                    chances = random.randint(1,2)
                    if chances == 1:
                        current_word = random.choice(special_word)
                        special = True
                    elif chances == 2:
                        heal = True
                current_word_start_time = pygame.time.get_ticks() # รีเซ็ตเวลาจำกัด
                if lives <= 0: # ถ้าพลังชีวิตน้อยกว่าหรือเท่ากับ 0
                    current_state = GameState.GAME_OVER # เปลี่ยน current_state เป็น GameOver

        # Blit หน้าต่าง
        if current_state == GameState.MAIN_MENU:
            title_rect = title_image.get_rect(center=(screen_width/2, 150))
            display_screen.blit(title_image, title_rect)
            for button in [play_button]: # โชว์ปุ่ม
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
            score_text = main_font.render(f"Final Score: {score}", True, COLOR_WHITE) # โชว์คะแนนทีได้
            game_over_rect = game_over_text.get_rect(center=(screen_width/2, 150))
            score_rect = score_text.get_rect(center=(screen_width/2, 220))
            display_screen.blit(game_over_text, game_over_rect)
            display_screen.blit(score_text, score_rect)
            for button in [retry_button, menu_button]:
                button.change_color(mouse_pos)
                button.update(display_screen)

        elif current_state == GameState.PLAYING:
            score_surface = ui_font.render(f"Score: {score}", True, COLOR_WHITE) # สร้าง text คะแนน
            lives_surface = ui_font.render(f"Lives: {lives}", True, COLOR_RED) # สร้าง text พลังชีวิต
            display_screen.blit(score_surface, (20, 20)) # โชว์คะแนน
            display_screen.blit(lives_surface, (screen_width - lives_surface.get_width() - 20, 20)) # โชว์พลังชีวิต

            word_color = COLOR_YELLOW # สีหลัก
            if heal: 
                word_color = COLOR_GREEN # สีคำศัพท์ฟื้นฟู
            if special:
                word_color = COLOR_RED # สีคำศัพท์พิเศษ

            # สร้าง text แสดง current_word
            word_surface = game_font.render(current_word, True, word_color)
            word_bg_rect = word_surface.get_rect(center=(screen_width/2, 250))
            word_bg_rect.inflate_ip(20, 10) # Add padding
            
            # สร้างพื้นหลังสำหรับ text
            bg_surface = pygame.Surface(word_bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 128)) # Black with 128 alpha
            display_screen.blit(bg_surface, word_bg_rect.topleft)

            # Blit text และ พื้นหลัง
            word_rect = word_surface.get_rect(center=word_bg_rect.center)
            display_screen.blit(word_surface, word_rect)

            # สร้างกล่องใส่ Input
            pygame.draw.rect(display_screen, COLOR_ACTIVE_INPUT, input_box, 2, border_radius=5)
            input_surface = game_font.render(input_text, True, COLOR_WHITE)
            display_screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

            # สร้างหลอดโชว์เวลา
            time_left_ratio = max(0, 1 - (elapsed_time / word_time_limit))
            timer_bar_width = (input_box.width - 4) * time_left_ratio

            # เปลี่ยนสี
            if time_left_ratio > 0.5:
                # เปลี่ยนสีจากเขียวไปเหลือง
                r = int((1.0 - time_left_ratio) * 2 * 255)
                g = 255
            else:
                # เปลี่ยนสีจากเหลืองไปแดง
                r = 255
                g = int(time_left_ratio * 2 * 255)
            timer_color = (r, g, 50)
            
            timer_bar_rect = pygame.Rect(input_box.x + 2, input_box.y - 20, timer_bar_width, 10)
            pygame.draw.rect(display_screen, timer_color, timer_bar_rect, border_radius=5)

        
        # Update ปุ่มเปิด-ปิดเสียง
        if Mute == False:
            unmute_button.update(display_screen)
            if current_music:
                pygame.mixer.music.set_volume(0.35) # เปิดเสียง
        elif Mute == True:
            mute_button.update(display_screen)
            if current_music:
                pygame.mixer.music.set_volume(0) # ปิดเสียง

        pygame.display.update() # update หน้าจอ
        await asyncio.sleep(0) # Give control back to the event loop

if __name__ == "__main__":
    asyncio.run(main()) # รันฟังชั่น main() ผ่าน asyncio เพื่อใช้ใน Browser
