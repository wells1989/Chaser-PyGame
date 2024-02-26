import pygame
import random
import os
from utils.generating_variables import generate_game_variables, generate_round_variables, display_rules_popup, sound_files
from utils.playing_functions import cell_clicked, no_move, is_touching, determine_winner

# Set up the paths to the sound files
current_directory = os.path.dirname(__file__)
effects_directory = os.path.join(current_directory, 'effects')

## key variable generation
pygame.init()
grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables()

sounds = {name: pygame.mixer.Sound(os.path.join(effects_directory, path)) for name, path in sound_files.items()}
player1_wins = 0 
player2_wins = 0
welcome = True

## Game Loop
while running:
    for event in pygame.event.get():
        if welcome:
            sounds['welcome'].play()
            display_rules_popup()
            welcome = False
            continue
        
        # Game round variables
        used_break, extra_turn = generate_round_variables()
        

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            row = event.pos[1] // cell_size 
            col = event.pos[0] // cell_size
            

            # if winning_message, create the play again button and if clicked starting new game
            if winning_message:
                play_again_button_rect = pygame.Rect(10, grid_size * cell_size + 90, window_size[0]-20, 30)
                if play_again_button_rect.collidepoint(event.pos):
                    grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables() 
                    continue
            else:
                restart_button = pygame.Rect(grid_size * cell_size // 2 + 10, grid_size * cell_size + 170, 155, 34)
                if restart_button.collidepoint(event.pos):
                    grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables() 
                    continue
            

            # showing rules button to trigger the display_rules_popup screen
            show_rules_button = pygame.Rect(10, grid_size * cell_size + 170, 155, 34)
            if show_rules_button.collidepoint(event.pos):
                display_rules_popup()
                continue
            

            # if not game_active, players are unable to click etc, and will just show the winning message / play again option
            if not game_active:
                continue 


            # warning messages
            warning_message = ""
            if not (0 <= row < grid_size and 0 <= col < grid_size):
                message = f"Clicked outside grid parameters."
                warning_message = message
                sounds['error'].play()
                continue

            if cell_clicked(row, col, grid):
                if player1_turn and player1_break_cards > 0 and grid[row][col] not in ["1C", "2C"]:
                    player1_break_cards -= 1
                    message = "player 1 using break ability"
                    warning_message = message
                    used_break = True
                elif not player1_turn and player2_break_cards > 0 and grid[row][col] not in ["1C", "2C"]:
                    player2_break_cards -= 1
                    message = "player 2 using break ability"
                    warning_message = message
                    used_break = True
                else:
                    message = "Warning! Cell has already been clicked."
                    warning_message = message
                    sounds['error'].play()
                    continue 
            

            if not is_touching(row, col, player1_turn, grid, grid_size):
                message = "horizontal / diagonal moves only!"
                warning_message = message
                sounds['error'].play()
                continue
            
            if used_break:
                value = 0
            else:
                value = grid[row][col]


            # * cells generate a random bonus
            if grid[row][col] == "*":
                rand_chance = random.randint(1,3)

                if rand_chance == 1:
                    value = random.randint(-5, 20)
                    message = f'Random bonus gives {value}'
                elif rand_chance == 2:
                    value = random.randint(0, 5)
                    message = f'You win {value} and gain a break card!'
                    if player1_turn:
                        player1_break_cards += 1
                    else:
                        player2_break_cards += 1
                else:
                    value = random.randint(0, 20)
                    extra_turn = True
                    message = f'You win {value} and gain a turn'
                
                warning_message = message


            # Updating scores and grid, checking for winning conditions and if no winning conditions switching player turn
            if player1_turn:
                player1_score += value
                for r in range(grid_size):
                    for c in range(grid_size):
                        if grid[r][c] == "1C":
                            grid[r][c] = "P1"
                        if grid[r][c] == "2C":
                            player2_current = (r, c)
                grid[row][col] = "1C"
                player1_current = (row, col)
                
                if no_move(player2_current[0], player2_current[1], grid, grid_size) and player2_break_cards == 0 or no_move(row, col, grid, grid_size) and player1_turn and player1_break_cards == 0 or no_move(row, col, grid, grid_size) and not player1_turn and player2_break_cards == 0:
                    player1_wins, player2_wins, winning_message, game_active = determine_winner(player1_score, player2_score, player1_wins, player2_wins)
                    sounds['win'].play()

                if extra_turn:
                    player1_turn = True
                else:
                    player1_turn = False
                
            else:
                player2_score += value
                for r in range(grid_size):
                    for c in range(grid_size):
                        if grid[r][c] == "2C":
                            grid[r][c] = "P2"
                        if grid[r][c] == "1C":
                            player1_current = (r, c)
                grid[row][col] = "2C"
                player2_current = (row, col)

                if no_move(player1_current[0], player1_current[1], grid, grid_size) and player1_break_cards == 0 or no_move(row, col, grid, grid_size) and player1_turn and player1_break_cards == 0 or no_move(row, col, grid, grid_size) and not player1_turn and player2_break_cards == 0:
                    player1_wins, player2_wins, winning_message, game_active = determine_winner(player1_score, player2_score, player1_wins, player2_wins)
                    sounds['win'].play()

                if extra_turn:
                    player1_turn = False
                else:
                    player1_turn = True

            if not warning_message and not winning_message:
                sounds['pop'].play()


    ## Update the window
    window.fill(BLACK)

    for row in range(grid_size):
        for col in range(grid_size):
            value = grid[row][col]
            pygame.draw.rect(window, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 2)
            

            # changing cell values / colors based on P1 or P2 clicking on them
            if value == "P1":
                color = RED
            elif value == "P2":
                color = BLUE
            elif value == "1C" or value == "2C":
                color = GREEN
            else:
                color = GRAY
            pygame.draw.rect(window, color, (col * cell_size + 2, row * cell_size + 2, cell_size - 4, cell_size - 4))

            text = font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            window.blit(text, text_rect)


    # Drawing player scores below the grid
    if player1_turn:
        player1_text = font.render(f"P1 Score: {player1_score}, wins {player1_wins}, br {player1_break_cards}", True, RED)
        pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 10, grid_size * cell_size-10, 30))
        window.blit(player1_text, (10, grid_size * cell_size + 10))

        player2_text = font.render(f"P2 Score: {player2_score}, wins {player2_wins}, br {player2_break_cards}", True, BLUE)
        window.blit(player2_text, (10, grid_size * cell_size + 50))
    else:
        player2_text = font.render(f"P2 Score: {player2_score}, wins {player2_wins}, br {player2_break_cards}", True, BLUE)
        pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 50, grid_size * cell_size-10 ,30))
        window.blit(player2_text, (10, grid_size * cell_size + 50))

        player1_text = font.render(f"P1 Score: {player1_score}, wins {player1_wins}, br {player1_break_cards}", True, RED)
        window.blit(player1_text, (10, grid_size * cell_size + 10))


    # drawing message displaying whose turn it is
    pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 90, grid_size * cell_size-10, 30))
    turn_text = "Player 1's turn!" if player1_turn else "Player 2's turn!"
    color = RED if player1_turn else BLUE
    turn_message = font.render(f"{turn_text}", True, color)
    window.blit(turn_message, (15, grid_size * cell_size + 90))


    # potential warning_message displaying warnings / player info (e.g. if using a break card)
    if warning_message:
        if warning_message in ["Warning! Cell has already been clicked.", "horizontal / diagonal moves only!", "Clicked outside grid parameters."]:
            pygame.draw.rect(window, RED, (10, grid_size * cell_size + 130, grid_size * cell_size-10, 30))
            warning_text = alt_font.render(f"{warning_message}", True, BLACK)
            window.blit(warning_text, (15, grid_size * cell_size + 135))
        else:
            pygame.draw.rect(window, GREEN, (10, grid_size * cell_size + 130, grid_size * cell_size-10, 30))
            warning_text = alt_font.render(f"{warning_message}", True, BLACK)
            window.blit(warning_text, (15, grid_size * cell_size + 135))


    # displaying winning message and play again option
    if winning_message:
        pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 130, grid_size * cell_size-10, 30))
        color = RED if player1_score > player2_score  else BLUE
        winning_text = alt_font.render(f"{winning_message}", True, color)
        window.blit(winning_text, (15, grid_size * cell_size + 135))

        pygame.draw.rect(window, GREEN, (10, grid_size * cell_size + 90, grid_size * cell_size-10, 30))
        play_again_text = "Play Again?"
        play_again_message = font.render(f"{play_again_text}", True, BLACK)
        window.blit(play_again_message, (15, grid_size * cell_size + 95))


    # showing rules message
    rules_text = "Show Rules?"
    rules_message = font.render(f"{rules_text}", True, BLACK)
    rules_text_rect = rules_message.get_rect()
    pygame.draw.rect(window, GREEN, (10, grid_size * cell_size + 170, rules_text_rect.width, rules_text_rect.height + 10))

    window.blit(rules_message, (10 , grid_size * cell_size + 175))


    # optional restart option if there is no winning message
    if not winning_message:
        restart_text = "Restart"
        restart_message = font.render(f"{restart_text}", True, BLACK)
        restart_text_rect = restart_message.get_rect()
        pygame.draw.rect(window, BLUE, (grid_size * cell_size // 2 + 10, grid_size * cell_size + 170, rules_text_rect.width, restart_text_rect.height + 10))

        window.blit(restart_message, (grid_size * cell_size // 2 + 30 , grid_size * cell_size + 175))

    pygame.display.flip()

pygame.quit()
