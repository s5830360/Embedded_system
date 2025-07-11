import pygame
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 230, 0)
PINK = (255, 100, 180)
BLUE = (0, 180, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BG_PINK = (255, 200, 220)

def draw_text_center(screen, text, y, color=BLACK, font_obj=None):
    if not font_obj:
        raise ValueError("font_obj must be provided")
    txt = font_obj.render(text, True, color)
    screen_width = screen.get_width()
    screen.blit(txt, (screen_width // 2 - txt.get_width() // 2, y - 5))

def draw_start_screen(screen, font_obj, start_select_idx):
    screen.fill(BG_PINK)
    screen_width = screen.get_width()
    offset_y = 100  # 전체 요소들을 아래로 내리는 오프셋

    draw_text_center(screen, "다마고치 친구들", 100 + offset_y, RED, font_obj=font_obj)

    start_rect = pygame.Rect(screen_width // 2 - 120, 220 + offset_y, 240, 50)
    instr_rect = pygame.Rect(screen_width // 2 - 120, 290 + offset_y, 240, 50)

    if start_select_idx == 0:
        pygame.draw.rect(screen, BLUE, start_rect, border_radius=8)
        pygame.draw.rect(screen, GRAY, instr_rect, border_radius=8)
    else:
        pygame.draw.rect(screen, GRAY, start_rect, border_radius=8)
        pygame.draw.rect(screen, BLUE, instr_rect, border_radius=8)

    draw_text_center(screen, "다마고치 키우기", 233 + offset_y, WHITE if start_select_idx == 0 else BLACK, font_obj=font_obj)
    draw_text_center(screen, "설명", 303 + offset_y, WHITE if start_select_idx == 1 else BLACK, font_obj=font_obj)
def draw_instruction_screen(screen, font_obj, instruction_pages, page=0): 
    screen.fill(WHITE) 
    title_font = pygame.font.SysFont("Arial", 36, bold=True) 
    draw_text_center(screen, "Instruction Manual", 60, (0, 0, 0), title_font)

    if page < 0 or page >= len(instruction_pages):
        return

    for i, line in enumerate(instruction_pages[page]):
        draw_text_center(screen, line, 140 + i * 36, font_obj=font_obj)

    # 페이지 넘김 안내
    tip = f"← {page+1}/{len(instruction_pages)} →"
    draw_text_center(screen, tip, screen.get_height() - 60, (100, 100, 100), font_obj)

def draw_virtual_keyboard(screen, font_obj, vkeys, vk_row, vk_col):
    screen_width = screen.get_width()
    key_w, key_h = 55, 55
    padding = 10
    total_row_widths = [len(row) * (key_w + padding) - padding for row in vkeys]
    vk_y = screen.get_height() - 330  # 키보드 전체 위로 올림

    for r, row in enumerate(vkeys):
        vk_x = screen_width // 2 - total_row_widths[r] // 2
        for c, key in enumerate(row):
            if key == "SPACE" or key == "DEL" or key == "ENTER":
                rect = pygame.Rect(vk_x + c * (key_w + padding), vk_y + r * (key_h + padding), key_w, key_h)
                color = BG_PINK if (r == vk_row and c == vk_col) else BG_PINK
                pygame.draw.rect(screen, color, rect, border_radius=6)
                disp_key = " " if key == "SPACE" else key
                text_color = BG_PINK if (r == vk_row and c == vk_col) else BG_PINK
                key_text = font_obj.render(disp_key, True, text_color)
                text_rect = key_text.get_rect(center=rect.center)
                screen.blit(key_text, text_rect)  
            else:
                rect = pygame.Rect(vk_x + c * (key_w + padding), vk_y + r * (key_h + padding), key_w, key_h)
                color = BLUE if (r == vk_row and c == vk_col) else GRAY
                pygame.draw.rect(screen, color, rect, border_radius=6)
                disp_key = " " if key == "SPACE" else key
                text_color = WHITE if (r == vk_row and c == vk_col) else BLACK
                key_text = font_obj.render(disp_key, True, text_color)
                text_rect = key_text.get_rect(center=rect.center)
                screen.blit(key_text, text_rect)

    special_labels = ["SPACE", "DEL", "ENTER"]
    special_key_w = 100
    spacing = 20
    total_width = len(special_labels) * (special_key_w + spacing) - spacing
    base_x = screen_width // 2 - total_width // 2
    y_offset = vk_y + len(vkeys) * (key_h + padding) + 10

    for i, label in enumerate(special_labels):
        rect = pygame.Rect(base_x + i * (special_key_w + spacing), y_offset, special_key_w, key_h)
        color = BLUE if (vk_row == 2 and vkeys[vk_row][vk_col] == label) else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=6)
        text_color = WHITE if (vk_row == 2 and vkeys[vk_row][vk_col] == label) else BLACK
        key_text = font_obj.render(label, True, text_color)
        text_rect = key_text.get_rect(center=rect.center)
        screen.blit(key_text, text_rect)


def draw_nickname_screen(screen, font_obj, nickname, vkeys, vk_row, vk_col):
    screen.fill(BG_PINK)
    screen_width = screen.get_width()
    draw_text_center(screen, "닉네임을 입력하세요 : ", 80, font_obj=font_obj)

    input_box = pygame.Rect(screen_width // 2 - 200, 160, 400, 60)  # 아래로 내림
    pygame.draw.rect(screen, WHITE, input_box, border_radius=8)
    pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=8)

    cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0
    display_text = nickname + ("_" if cursor_visible else "")
    txt_surface = font_obj.render(display_text, True, BLACK)
    screen.blit(txt_surface, (input_box.x + 15, input_box.y + 15))

    draw_virtual_keyboard(screen, font_obj, vkeys, vk_row, vk_col)

def draw_hello_screen(screen, font_obj, nickname):
    screen.fill(WHITE)
    screen_height = screen.get_height()
    draw_text_center(screen, f"안녕 {nickname}!", screen_height // 2 - 20, font_obj=font_obj)
    draw_text_center(screen, "아무 키나 누르면 시작합니다.", screen_height // 2 + 20, font_obj=font_obj)
