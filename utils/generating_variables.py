import random
import pygame
 
# sound files

sound_files = {
    'win': 'win.mp3',
    'melody': 'melody.mp3',
    'pop': 'pop.mp3',
    'welcome': 'welcome.mp3',
    'error': 'error.mp3',
}

# playing constant variables across game rounds
def generate_playing_variables():
    player1_score = 0
    player2_score = 0
    player1_break_cards = 0
    player2_break_cards = 0

    chance_turn = random.randint(1,2)
    player1_turn = True if chance_turn == 1 else False
    warning_message = ""
    winning_message = ""
    extra_turn = False

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    WHITE = (255, 255, 255)

    return player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn


# generating pyGame window
def generate_window():
    grid_size = 10
    cell_size = 35
    window_size = (grid_size * cell_size, grid_size * cell_size + 210)  # defines width then height of window, Increased height for the scores
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Chaser Game")

    return grid_size, cell_size, window_size, window


# Create the grid
def generate_grid(grid_size):
    # generating random grid
    grid = [[random.randint(1, 10) for _ in range(grid_size)] for _ in range(grid_size)]

    # random starting position on either x or x or y axis for player 1 / 2
    edge_positions = [(0, random.randint(0, grid_size - 1)), (random.randint(0, grid_size - 1), 0)]
    row, col = random.choice(edge_positions)
    grid[row][col] = "1C"

    edge_positions = [(grid_size - 1, random.randint(0, grid_size - 1)), (random.randint(0, grid_size - 1), grid_size - 1)]
    while True:
        row, col = random.choice(edge_positions)
        if grid[row][col] != "1C":
            grid[row][col] = "2C"
            break

    # generating bonus symbols and distributing them
    bonuses = []
    for i in range(grid_size-1):
        bonuses.append("*")
    
    for elem in bonuses:
        rand_x = random.randint(0, grid_size - 1)
        rand_y = random.randint(0, grid_size - 1)
        if not grid[rand_x][rand_y] in ["1C", "2C"]:
            grid[rand_x][rand_y] = "*"
            
    
    return grid


# generating round variables (i.e. that change on each playing round)
def generate_round_variables():
    used_break = False
    extra_turn = False
    
    return used_break, extra_turn


# main generating variables function, utilising the above to get all game variables
def generate_game_variables():
    grid_size, cell_size, window_size, window= generate_window()
    grid = generate_grid(grid_size)
    player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn = generate_playing_variables()

    running = True
    game_active = True
    font = pygame.font.Font(None, 36)
    alt_font = pygame.font.Font(None, 24)
    menu_font = pygame.font.Font(None, 22)

    return grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn ,running, game_active, font, alt_font, menu_font


# displays the rules / menu popup
def display_rules_popup():

    grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn ,running, game_active, font, alt_font, menu_font = generate_game_variables()

    window_size = (grid_size * cell_size, grid_size * cell_size + 210)
    rules_window = pygame.display.set_mode(window_size)
    rules_window.fill(WHITE)
    pygame.display.set_caption("Rules of the Game")

    rules_text = [
        "Welcome to the chaser game!",
        "BASICS:",
        "- You can move either horizontally or vertically",
        "- 1C / 2C show player 1 / 2's starting position",
        "- P1 / P2 show past moves for player 1 / 2",
        "HOW TO WIN:",
        "- The player with the most points wins",
        "- The game ends when a player cannot move",
        "BONUSES:",
         "- Symbols * give you bonuses ...",
         " - Extra point cards, between -5 and 20",
         " - Extra turn plus 5 points",
         " - Br cards can break P1 / P2 squares"
    ]

    i = 20
    for line in rules_text:
        if line[-1] in ("!", ":"):
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect() 
            rules_window.blit(text, (10, i))
            
            pygame.draw.line(rules_window, BLACK, (10, i + text_rect.height), (10 + text_rect.width, i + text_rect.height), 2)

        else:
            text = menu_font.render(line, True, GREEN)
            rules_window.blit(text, (10, i))
        i += 40

    rules_text = "Go to Game? ..."
    rules_message = font.render(f"{rules_text}", True, BLUE)
    window.blit(rules_message, (20, 530))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return_to_game_button = pygame.Rect(30, 530, 200, 300)
                if return_to_game_button.collidepoint(event.pos):
                    pygame.display.set_caption("Chaser Game")
                    waiting_for_input = False 