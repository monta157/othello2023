class OthelloAI(object):
    def __init__(self, face, name):
        self.face = face
        self.name = name

    def __repr__(self):
        return f"{self.face}{self.name}"

    def move(self, board: np.array, piece: int)->tuple[int, int]:
        valid_moves = get_valid_moves(board, piece)
        return valid_moves[0]

    def say(self, board: np.array, piece: int)->str:
        if count_board(board, piece) >= count_board(board, -piece):
            return 'やったー'
        else:
            return 'がーん'

def board_play(player: OthelloAI, board, piece: int):
    display_board(board, sleep=0)
    if len(get_valid_moves(board, piece)) == 0:
        print(f"{player}は、置けるところがありません。スキップします。")
        return True
    try:
        start_time = time.time()
        r, c = player.move(board.copy(), piece)
        end_time = time.time()
    except:
        print(f"{player.face}{player.name}は、エラーを発生させました。反則まけ")
        return False
    if not is_valid_move(board, r, c, piece):
        print(f"{player}が返した({r},{c})には、置けません。反則負け。")
        return False
    display_move(board, r, c, piece)
    return True

def comment(player1: OthelloAI, player2: OthelloAI, board):
    try:
        print(f"{player1}: {player1.say(board, BLACK)}")
    except:
        pass
    try:
        print(f"{player2}: {player2.say(board, WHITE)}")
    except:
        pass

def game(player1: OthelloAI, player2: OthelloAI,N=6):
    board = init_board(N)
    display_board(board, black=f'{player1}', white=f'{player2}')
    while count_board(board, EMPTY) > 0:
        if not board_play(player1, board, BLACK):
            break
        if not board_play(player2, board, WHITE):
            break
    comment(player1, player2, board)

class GinbisuAI(object):
    def __init__(self, face, name, depth=3):
        self.face = face
        self.name = name
        self.max_depth = depth

    def __repr__(self):
        return f"{self.face}{self.name}"

    def move(self, board: np.array, piece: int) -> tuple[int, int]:
        _, best_move = self.minimax(board, piece, self.max_depth, float('-inf'), float('inf'))
        return best_move

    def say(self, board: np.array, piece: int) -> str:
        if count_board(board, piece) >= count_board(board, -piece):
            return 'やったー'
        else:
            return 'がーん'

    def minimax(self, board, piece, depth, alpha, beta):
        if depth == 0 or not get_valid_moves(board, piece):
            return self.evaluate_board(board), None

        valid_moves = get_valid_moves(board, piece)
        best_move = None

        if piece == WHITE:  # Maximizing player
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = board.copy()
                stones_to_flip = flip_stones(new_board, move[0], move[1], piece)
                new_board[move[0], move[1]] = piece
                eval_val, _ = self.minimax(new_board, -piece, depth - 1, alpha, beta)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = move
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:  # Minimizing player
            min_eval = float('inf')
            for move in valid_moves:
                new_board = board.copy()
                stones_to_flip = flip_stones(new_board, move[0], move[1], piece)
                new_board[move[0], move[1]] = piece
                eval_val, _ = self.minimax(new_board, -piece, depth - 1, alpha, beta)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = move
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, board):
        # Implement your own board evaluation function
        # This is a simple example, you may need a more sophisticated one
        return count_board(board, WHITE) - count_board(board, BLACK)

# Example Usage
# advanced_ai = AdvancedOthelloAI('🤖', 'Advanced AI', depth=4)
# selected_move = advanced_ai.move(board, WHITE)
# display_move(board, selected_move[0], selected_move[1], WHITE)
# print(advanced_ai.say(board, WHITE))
