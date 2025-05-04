import math

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]):
            return True
        if all(row[i] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell in ["X", "O"] for row in board for cell in row)

def get_valid_moves(board):
    return [(i, j) for i in range(3) for j in range(3)
            if board[i][j] not in ["X", "O"]]

def minimax(board, depth, is_maximizing, ai, human):
    if check_winner(board, ai):
        return 1
    if check_winner(board, human):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i, j in get_valid_moves(board):
            board[i][j] = ai
            score = minimax(board, depth + 1, False, ai, human)
            board[i][j] = str(i * 3 + j + 1)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i, j in get_valid_moves(board):
            board[i][j] = human
            score = minimax(board, depth + 1, True, ai, human)
            board[i][j] = str(i * 3 + j + 1)
            best_score = min(score, best_score)
        return best_score

def best_ai_move(board, ai, human):
    best_score = -math.inf
    move = None
    for i, j in get_valid_moves(board):
        board[i][j] = ai
        score = minimax(board, 0, False, ai, human)
        board[i][j] = str(i * 3 + j + 1)
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

def tic_tac_toe():
    board = [["1", "2", "3"],
             ["4", "5", "6"],
             ["7", "8", "9"]]

    human = "X"
    ai = "O"
    current_player = human

    while True:
        print_board(board)

        if current_player == human:
            move = input("Your move (1-9): ")

            if not move.isdigit() or int(move) not in range(1, 10):
                print("Invalid input! Please enter a number between 1 and 9.")
                continue

            move = int(move) - 1
            row, col = divmod(move, 3)

            if board[row][col] in ["X", "O"]:
                print("Cell already taken! Try a different move.")
                continue
        else:
            print("AI is thinking...")
            row, col = best_ai_move(board, ai, human)

        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            winner = "You" if current_player == human else "AI"
            print(f"🎉 {winner} win!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = ai if current_player == human else human


tic_tac_toe()
