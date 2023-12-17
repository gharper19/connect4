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
FILLED_CELL = '[0]'
EMPTY_CELL = '[ ]'

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
    delimiter = " | "
    render_string = ""
    
    # Contstruct render string
    for row in grid:
        render_string += delimiter
        for cell in row:
            render_string += cell + delimiter
        render_string += '\n'
    
    # Print string
    print(render_string)

def handle_player_input():
    input_validated = False

    # Get input
    while(not input_validated):
        column_selection = -1
        row_selection = -1

        # Get column selection
        user_input = input("Enter the column of your selected cell: ")
        try:    
            # Validate column selection
            assert isinstance(user_input, numbers.Real)
            user_input = int(user_input)
            assert user_input <= grid_columns

            column_selection = user_input-1
        except Exception as e: 
            print("Unacceptable. Please enter a valid column number.\n"+ e)
            continue

        # Get row selection
        user_input = input("Enter the row of your selected cell: ")
        try:    
            # Validate row selection
            assert isinstance(user_input, numbers.Real)
            user_input = int(user_input)
            assert user_input <= grid_rows

            row_selection = user_input-1
        except Exception as e: 
            print("Unacceptable. Please enter a valid row number.\n"+ e)
            continue
            
        print(f"Selection ({column_selection+1},{row_selection+1}) confirmed.")
        input_validated=True
    
    # Update grid
    grid[column_selection][row_selection] = FILLED_CELL

def update_grid():
    pass

def check_game_over():
    # Check if a player has won or if the board is full
    pass

def end_game():
    end_string = "STOP!!\n" + 
                "... \n" +
                f"Player {current_player} WINS!!!"
    print(end_string)

def main():
    # global current_player
    run_flag = True

    # Intro text
    intro_text = "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n" +
                "Connect 4 : Connect 4 to win!!\n" +
                "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
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
        game_over = check_winner_exists()
        if game_over: 
            end_game()
            break

if __name__=='__main__':
    main()







