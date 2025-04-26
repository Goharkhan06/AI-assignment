import time
import random

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

# --- Alpha-Beta Pruning AI ---
node_counter = 0

def minimax_alpha_beta(board, is_maximizing, player, opponent, alpha, beta):
    global node_counter
    node_counter += 1
    if is_winner(board, player):
        return 1
    if is_winner(board, opponent):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i, j in get_available_moves(board):
            board[i][j] = player
            eval = minimax_alpha_beta(board, False, player, opponent, alpha, beta)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = opponent
            eval = minimax_alpha_beta(board, True, player, opponent, alpha, beta)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, player):
    opponent = 'O' if player == 'X' else 'X'
    best_score = float('-inf')
    move = None
    for i, j in get_available_moves(board):
        board[i][j] = player
        score = minimax_alpha_beta(board, False, player, opponent, float('-inf'), float('inf'))
        board[i][j] = ' '
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

# --- AI Game ---
def simulate_alpha_beta_game():
    board = create_board()
    current_player = 'X'
    print("\n--- Alpha-Beta AI vs AI ---\n")
    print_board(board)
    print()

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
    minimax_alpha_beta(board, True, 'X', 'O', float('-inf'), float('inf'))
    end = time.time()
    print(f"Alpha-Beta -> Time: {end - start:.4f}s, Nodes: {node_counter}")

# --- Main ---
if __name__ == "__main__":
    test_performance()
    simulate_alpha_beta_game()
