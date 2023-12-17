import numbers
# # Connect4
# Board Representation:


# Implement a function to get input from players. Make sure to validate the input (e.g., ensure the column is not full, accept only valid column numbers).
# Making Moves:

# Write a function to update the board based on the player's move.
# Check for a Win:

# Implement a function to check if a player has won the game. This involves checking for four consecutive discs in a row, column, or diagonal.
# Switching Players:

# Write a mechanism to switch between players after each move.
# Main Game Loop:

# Create a loop to keep the game running until there's a winner or the board is full (resulting in a draw).
# End of Game:

# Display the winner or announce a draw at the end of the game.

FILLED_CELL_1 = '[0]'
FILLED_CELL_2 = '[O]'
FILLED_CELL_LIST = [FILLED_CELL_1, FILLED_CELL_2]
EMPTY_CELL = '[ ]'
GRID_ROW_LENGTH = 43

grid_columns = 7
grid_rows = 6
grid = [ 
    # 7-column, 6-row
    [EMPTY_CELL for i in range(grid_columns)] for j in range(grid_rows)
]
current_player = 0
total_players = 2


def render_ui():
    global current_player
    print(f"Player {current_player}'s turn...\n... GO!")

def render_grid():
    global grid, grid_columns
    delimiter = " | "
    render_string = ""
    
    # Construct grid header
    header_string = " | "
    col_number = 1
    for col in range(grid_columns):
        header_string += " " + str(col_number) + " " + delimiter 
        col_number += 1
    print(header_string)

    # Contstruct render string
    for row in grid:
        render_string += delimiter
        for cell in row:
            render_string += cell + delimiter
        render_string += '\n'
    
    # Print string
    print(render_string)

    # # Print tail string
    # tail_string = "+="*((GRID_ROW_LENGTH-1)) + "+\n" + "|" + " "*(GRID_ROW_LENGTH-2) + "|"
    # print(tail_string)
    # print()

def handle_player_input():
    global grid_rows, current_player
    input_validated = False

    # Get input
    while(not input_validated):
        column_selection = -1
        row_selection = -1

        # Get column selection
        user_input = input("Enter the column of your selected cell: ")
        try:    
            # Validate column selection
            assert isinstance(int(user_input), int)
            user_input = int(user_input)
            assert user_input <= grid_columns

            # Convert to index
            column_selection = user_input-1

            # Determine row selection from column selection
            for i in range(grid_rows):
                if i == 0:
                    # Check first row
                    if grid[i][column_selection] in FILLED_CELL_LIST:
                        print("Thats taken. Invalid.")
                        raise Exception
                elif grid[i][column_selection] in FILLED_CELL_LIST:
                    # Get previous
                    row_selection = i-1
                    break

        except Exception as e: 
            # Check commands
            if user_input == 'q':
                return "QUIT"
            
            # Prompt and return to user input
            print("Unacceptable. Please enter a valid column number.\n"+ str(e))
            continue
        input_validated = True

    # Update grid
    grid[row_selection][column_selection] = FILLED_CELL_LIST[current_player-1]

def check_game_over():
    global grid
    result = ""
    # Check if a player has won or if the board is full
    
    # Check board full
    board_full = True
    for i in range(grid_columns):
        if grid[0][i] == EMPTY_CELL:
            board_full = False
    if board_full == False:
        result = "DRAW"
    
    # Check player win
    


    return False

def end_game():
    end_string = "STOP!!\n" + "... \n" + f"Player {current_player} WINS!!!"
    print(end_string)

def main():
    global grid, current_player, total_players
    # global current_player
    run_flag = True

    # Intro text
    intro_text = "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n" + "Connect 4 : Connect 4 to win!!\n" + "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
    print(intro_text)

    # Initialize Game
    current_player = 1

    # Game loop
    while(run_flag):
        # Render UI
        render_ui()

        # Render grid
        render_grid()

        # Handle input
        response = handle_player_input()
        if response == "QUIT":
            print("Game Over... \nNo winner decided.")
            break

        # Switch Players
        current_player += 1
        if current_player > total_players:
            current_player = 1

        # Check if game is over
        game_over = check_game_over()
        if game_over: 
            end_game()
            break

if __name__=='__main__':
    main()







