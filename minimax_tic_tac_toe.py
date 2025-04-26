import time

# --- Game Logic ---
def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

# --- Minimax AI ---
node_counter = 0

def minimax(board, is_maximizing, player, opponent):
    global node_counter
    node_counter += 1
    if is_winner(board, player):
        return 1
    if is_winner(board, opponent):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i, j in get_available_moves(board):
            board[i][j] = player
            score = minimax(board, False, player, opponent)
            board[i][j] = ' '
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = opponent
            score = minimax(board, True, player, opponent)
            board[i][j] = ' '
            best_score = min(best_score, score)
        return best_score

def best_move(board, player):
    opponent = 'O' if player == 'X' else 'X'
    best_score = float('-inf')
    move = None
    for i, j in get_available_moves(board):
        board[i][j] = player
        score = minimax(board, False, player, opponent)
        board[i][j] = ' '
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

# --- AI Game ---
def simulate_minimax_game():
    board = create_board()
    current_player = 'X'
    print("\n--- Minimax AI vs AI ---\n")
    print_board(board)
    print()

    # Randomize first move for imperfect play
    import random
    i, j = random.choice(get_available_moves(board))
    board[i][j] = current_player
    print(f"{current_player} (random start) moves to {(i, j)}")
    print_board(board)
    print()
    current_player = 'O'

    while True:
        move = best_move(board, current_player)
        if move:
            board[move[0]][move[1]] = current_player
            print(f"{current_player} moves to {move}")
            print_board(board)
            print()
        if is_winner(board, current_player):
            print(f"{current_player} wins!")
            break
        elif is_full(board):
            print("It's a tie!")
            break
        current_player = 'O' if current_player == 'X' else 'X'

# --- Performance Test ---
def test_performance():
    board = create_board()
    global node_counter
    node_counter = 0
    start = time.time()
    minimax(board, True, 'X', 'O')
    end = time.time()
    print(f"Minimax -> Time: {end - start:.4f}s, Nodes: {node_counter}")

# --- Main ---
if __name__ == "__main__":
    test_performance()
    simulate_minimax_game()
