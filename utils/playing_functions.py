# getting the values to either side / above or below a cell
def get_adjacent_values(row,col, grid, grid_size):
    
    adjacent_values = {
        "x-1": grid[row - 1][col] if row - 1 >= 0 else None,
        "x+1": grid[row + 1][col] if row + 1 < grid_size else None,
        "y-1": grid[row][col - 1] if col - 1 >= 0 else None,
        "y+1": grid[row][col + 1] if col + 1 < grid_size else None,
    }
    return adjacent_values


# returns True if the cell clicked on is next to, below or above the current P1 / P2 cell
def is_touching(row, col, player1_turn, grid, grid_size):
    code = "1C" if player1_turn else "2C"

    adjacent_values = get_adjacent_values(row, col, grid, grid_size)

    for key, value in adjacent_values.items():
        if value == code:
            return True
    else:
        return False
    

# returns True if there is no available move, i.e. all taken cells so cannot move
def no_move(row, col, grid, grid_size):
    adjacent_values = get_adjacent_values(row, col, grid, grid_size)

    for key, value in adjacent_values.items():
        if value and value not in ["P1", "P2", "1C", "2C"]:
            return False
    return True


# returns True if the cell has already been clicked
def cell_clicked(row,col, grid):
    if grid[row][col] in ["P1", "P2", "1C", "2C"]:
        return True
    

# determines the winner based on scores
def determine_winner(player1_score, player2_score, player1_wins, player2_wins):
                if player1_score > player2_score:
                    player1_wins += 1
                    message = "winner, player 1 "
                elif player2_score > player1_score:
                    player2_wins += 1
                    message = "winner, player 2 "
                else:
                    message = "it's a draw!"
                winning_message = message
                game_active = False
                return player1_wins, player2_wins, winning_message, game_active