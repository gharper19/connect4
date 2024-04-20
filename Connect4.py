# Connect4
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

def clear_grid():
    global grid
    grid = [
        # 7-column, 6-row
        [EMPTY_CELL for i in range(grid_columns)] for j in range(grid_rows)
    ]

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
            user_input = int(user_input)
            assert isinstance(user_input, int)
            assert user_input <= grid_columns
            assert user_input > 0

            # Convert to index
            column_selection = user_input - 1

            # Determine row selection from column selection
            for i in range(grid_rows):
                if i == 0:
                    # Check first row
                    if grid[i][column_selection] in FILLED_CELL_LIST:
                        print("What are you doing? That column is full.")
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
        run_draw_sequence()
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
        print(f"STOP!!\n... \n{FILLED_CELL_LIST[result][1]}")
        run_player_win_sequence(result)
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
        print(f"STOP!!\n... \n{FILLED_CELL_LIST[result][1]}")
        run_player_win_sequence(result)
        return True

    # Check diagonal chain
    matched_cell = check_diagonal_connect_four()
    if (not matched_cell == None):
        result = FILLED_CELL_INDICIES[grid[matched_cell[0]][matched_cell[1]]]

    if result > -1:
        print(f"STOP!!\n... \n{FILLED_CELL_LIST[result][1]}")
        run_player_win_sequence(result)
        return True
def check_diagonal_connect_four():
    def is_winning_diagonal(start_row, start_col, row_increment, col_increment):
        MATCH_COUNT_NEEDED = 4
        current_piece = grid[start_row][start_col]
        match_count = 1

        for i in range(1, MATCH_COUNT_NEEDED):
            next_row = start_row + i * row_increment
            next_col = start_col + i * col_increment
            if not (0 <= next_row < grid_rows and 0 <= next_col < grid_columns):
                break
            if grid[next_row][next_col] == current_piece:
                match_count += 1
                if match_count == MATCH_COUNT_NEEDED:
                    return next_row, next_col  # Return the winning cell coordinates
            else:
                break

        return None

    # Check diagonals from top-left to bottom-right (↘)
    for row in range(grid_rows):
        for col in range(grid_columns):
            if grid[row][col] != EMPTY_CELL:
                winning_cell = is_winning_diagonal(row, col, 1, 1)
                if winning_cell:
                    return winning_cell

    # Check diagonals from top-right to bottom-left (↙)
    for row in range(grid_rows):
        for col in range(grid_columns - 1, -1, -1):
            if grid[row][col] != EMPTY_CELL:
                winning_cell = is_winning_diagonal(row, col, 1, -1)
                if winning_cell:
                    return winning_cell

    return None

def run_intro():
    # Intro text
    intro_text = "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n" + "Connect 4 : Connect 4 to win!!\n" + "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
    print(intro_text)

def run_player_win_sequence(player):
    # Win text
    win_text = "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n" + f"Player {player+1} WINS!! {FILLED_CELL_LIST[player][1]}\n" + "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n"
    print(win_text)

def run_draw_sequence():
    # Draw text
    draw_text = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n" + f"DRAW! Victory was abandoned.\n" + "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
    print(draw_text)

def main():
    global grid, current_player, total_players
    run_flag = True

    # Initialize Game
    current_player = 1
    run_intro()

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
            resp = input("Play again? (y/n)")
            if resp == 'y':
                clear_grid()
                run_intro()
                current_player = 1
                continue
            else:
                break


if __name__ == '__main__':
    main()