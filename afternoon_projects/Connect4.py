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

FILLED_CELL_1 = '[◎]'
FILLED_CELL_2 = '[◍]'
FILLED_CELL_LIST = [FILLED_CELL_1, FILLED_CELL_2]
FILLED_CELL_INDICIES = {c:i for i,c in enumerate(FILLED_CELL_LIST)}
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
    print(f"Player {current_player}'s turn...\n ... GO! {FILLED_CELL_LIST[current_player-1][1]}")


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

    # Construct render string
    for row in grid:
        render_string += delimiter
        for cell in row:
            render_string += cell + delimiter
        render_string += '\n'

    # Print string
    print(render_string)


def handle_player_input():
    global grid_rows, current_player
    input_validated = False

    # Get input
    while (not input_validated):
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
            column_selection = user_input - 1

            # Determine row selection from column selection
            for i in range(grid_rows):
                if i == 0:
                    # Check first row
                    if grid[i][column_selection] in FILLED_CELL_LIST:
                        print("Thats taken. Invalid.")
                        raise Exception
                elif grid[i][column_selection] in FILLED_CELL_LIST:
                    # Get previous
                    row_selection = i - 1
                    break

        except Exception as e:
            # Check commands
            if user_input == 'q':
                return "QUIT"

            # Prompt and return to user input
            print("Unacceptable. Please enter a valid column number.\n" + str(e))
            continue
        input_validated = True

    # Update grid
    grid[row_selection][column_selection] = FILLED_CELL_LIST[current_player - 1]


def check_game_over():
    global grid
    result = -1

    # Check board full
    board_full = True
    for i in range(grid_columns):
        if grid[0][i] == EMPTY_CELL:
            board_full = False
    if board_full == True:
        result = 0

    # Evaluate result
    if result == 0:
        print("Draw! No winner.")
        return True


    # Check player win
    # Check horizontal chain
    cell_indicies = {c:i for i,c in enumerate(FILLED_CELL_LIST)}
    for row in grid:
        tracking_cell = ""
        chain_length = 0
        for cell in row:
            if cell == tracking_cell:
                chain_length += 1
                if chain_length == 4:
                    result = cell_indicies[cell]
                    break
            else:
                chain_length = 1
                if cell in FILLED_CELL_LIST:
                    tracking_cell = cell
                else:
                    tracking_cell = ""
        if result > -1: break

    if result > -1:
        print(f"STOP!!\n... \nPlayer {result+1} WINS! {FILLED_CELL_LIST[result][1]}")
        return True

    # Check vertical chain
    for col in range(grid_columns):
        tracking_cell = ""
        chain_length = 0
        for row in range(grid_rows):
            if grid[row][col] == tracking_cell:
                chain_length += 1
                if chain_length == 4:
                    result = cell_indicies[grid[row][col]]
                    break
            else:
                chain_length = 1
                if grid[row][col] in FILLED_CELL_LIST:
                    tracking_cell = grid[row][col]
                else:
                    tracking_cell = ""
        if result > -1: break

    if result > -1:
        print(f"STOP!!\n... \nPlayer {result+1} WINS! {FILLED_CELL_LIST[result][1]}")
        return True

    # Check diagonal chain
    match_found = False
    for row in range(grid_rows):
        for col in range(grid_columns):
            # Check diagonal cells in SE direction
            resp = check_diagonal_match(1,
                                     (row, col),
                                     (row+1, col+1),
                                     1,
                                     1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break

            # Check diagonal cells in NE direction
            resp = check_diagonal_match(1,
                                     (row, col),
                                     (row-1, col+1),
                                     -1,
                                     1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break

            # Check diagonal cells in SW direction
            resp = check_diagonal_match(1,
                                     (row, col),
                                     (row+1, col-1),
                                     1,
                                     -1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break

            # Check diagonal cells in NW direction
            resp = check_diagonal_match(1,
                                     (row, col),
                                     (row-1, col-1),
                                     -1,
                                     -1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break
        if match_found:
            break

    if result > -1:
        print(f"STOP!!\n... \nPlayer {result+1} WINS! {FILLED_CELL_LIST[result][1]}")
        return True
def check_diagonal_match(count, cell, target, increment_row, increment_col):
    # Checks for a sequential match of 4 in the direction set by incrementing values
    # Count should be passed in as 1 initially, as each non-empty cell is the 1st item in the start of its own chain
    # Validate target increment values to make sure we have not hit the edge of the grid
    if target[0] > grid_rows - 1 or target[0] < 0:
        return (-1, -1)
    if target[1] > grid_columns - 1 or target[1] < 0:
        return (-1, -1)

    if cell == EMPTY_CELL:
        count = 1
    elif(count == 3):
        # Base case: if we need one more match
        if grid[cell[0]][cell[1]] == grid[target[0]][target[1]]:
            # if this cell matches the target cell
            return (target[0], target[1])
    else: # Give it 1 if its not a match, 2 if it is,
        if grid[cell[0]][cell[1]] == grid[target[0]][target[1]]:
            # if this cell matches the target cell then increase count and call again
            count += 1
        else:
            count = 1

    result = check_diagonal_match(
        count,
        target,
        (target[0] + increment_row, target[1] + increment_col),
        increment_row,
        increment_col
    )

    if result != (-1, -1):
        return result

    # If no match found in the recursive call, continue the search
    return (-1, -1)

def test_diagonal():
    global grid
    for r in range(grid_rows):
        for c in range(grid_columns):
            if r > 1:
                grid[r][c] = FILLED_CELL_LIST[1]
    render_grid()

    # Check diagonal chain
    match_found = False
    for row in range(grid_rows):
        for col in range(grid_columns):
            # Check diagonal cells in SE direction
            resp = check_diagonal_match(1,
                                        (row, col),
                                        (row + 1, col + 1),
                                        1,
                                        1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break

            # Check diagonal cells in NE direction
            resp = check_diagonal_match(1,
                                        (row, col),
                                        (row - 1, col + 1),
                                        -1,
                                        1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break

            # Check diagonal cells in SW direction
            resp = check_diagonal_match(1,
                                        (row, col),
                                        (row + 1, col - 1),
                                        1,
                                        -1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break

            # Check diagonal cells in NW direction
            resp = check_diagonal_match(1,
                                        (row, col),
                                        (row - 1, col - 1),
                                        -1,
                                        -1)
            if (resp > (-1, -1)):
                result = FILLED_CELL_INDICIES[grid[resp[0]][resp[1]]]
                match_found = True
                break
        if match_found:
            print(f"Check: {resp}\n{grid[resp[0]][resp[1]]}")

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
    while (run_flag):
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
            render_grid()
            break


if __name__ == '__main__':
    # main()
    test_diagonal()