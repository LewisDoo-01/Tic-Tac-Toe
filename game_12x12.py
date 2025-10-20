import pygame
import sys
import math

# --- Cài đặt hằng số cho game ---
BOARD_SIZE = 12
WIN_CONDITION = 5
SQUARE_SIZE = 50  # Kích thước mỗi ô
WIDTH = HEIGHT = BOARD_SIZE * SQUARE_SIZE
RADIUS = SQUARE_SIZE // 2 - 5
AI_SEARCH_DEPTH = 2 # Độ sâu AI nhìn trước. Tăng lên sẽ mạnh hơn nhưng chậm hơn.

# --- Màu sắc ---
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
PLAYER_COLOR = (242, 235, 211) # Người chơi (Trắng)
AI_COLOR = (84, 84, 84)       # AI (Đen)

# --- ĐÃ SỬA / FIXED: Khởi tạo Pygame ngay tại đây ---
pygame.init()

# --- Font chữ ---
# Bây giờ dòng này sẽ hoạt động vì pygame đã được init
FONT = pygame.font.Font(None, 40)

# --- Tạo màn hình game ---
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Gomoku 12x12 - Player (White) vs AI (Black)")

# --- Biến game ---
board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
game_over = False
winner = None
# AI (Đen) đi trước trong luật Gomoku/Caro
turn = 'AI' # 'PLAYER' or 'AI'

def draw_grid():
    """Vẽ lưới bàn cờ."""
    for x in range(BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x * SQUARE_SIZE, 0), (x * SQUARE_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, LINE_COLOR, (0, x * SQUARE_SIZE), (WIDTH, x * SQUARE_SIZE), 2)

def draw_pieces():
    """Vẽ các quân cờ."""
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
            if board[r][c] == 'PLAYER':
                pygame.draw.circle(screen, PLAYER_COLOR, center, RADIUS)
            elif board[r][c] == 'AI':
                pygame.draw.circle(screen, AI_COLOR, center, RADIUS)

def check_win(r, c):
    """Kiểm tra thắng thua chỉ xung quanh nước đi cuối cùng."""
    player = board[r][c]
    if not player: return None
    
    # Duyệt 4 hướng (ngang, dọc, chéo chính, chéo phụ)
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        count = 1
        # Đếm xuôi theo hướng
        for i in range(1, WIN_CONDITION):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        # Đếm ngược theo hướng
        for i in range(1, WIN_CONDITION):
            nr, nc = r - i * dr, c - i * dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        
        if count >= WIN_CONDITION:
            return player
            
    # Kiểm tra hòa
    if all(board[r][c] != '' for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return 'DRAW'
        
    return None

def evaluate_window(window, piece):
    """Chấm điểm cho một cửa sổ (chuỗi 5 ô)."""
    score = 0
    opponent_piece = 'PLAYER' if piece == 'AI' else 'AI'

    if window.count(piece) == 5:
        score += 100000
    elif window.count(piece) == 4 and window.count('') == 1:
        score += 5000
    elif window.count(piece) == 3 and window.count('') == 2:
        score += 200
    
    if window.count(opponent_piece) == 4 and window.count('') == 1:
        score -= 4000
    elif window.count(opponent_piece) == 3 and window.count('') == 2:
        score -= 500

    return score

def score_position(piece):
    """Tính tổng điểm của một bên trên toàn bàn cờ."""
    score = 0
    # Ngang
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - WIN_CONDITION + 1):
            window = [board[r][c+i] for i in range(WIN_CONDITION)]
            score += evaluate_window(window, piece)
    # Dọc
    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE - WIN_CONDITION + 1):
            window = [board[r+i][c] for i in range(WIN_CONDITION)]
            score += evaluate_window(window, piece)
    # Chéo
    for r in range(BOARD_SIZE - WIN_CONDITION + 1):
        for c in range(BOARD_SIZE - WIN_CONDITION + 1):
            window = [board[r+i][c+i] for i in range(WIN_CONDITION)]
            score += evaluate_window(window, piece)
            window = [board[r+i][c+WIN_CONDITION-1-i] for i in range(WIN_CONDITION)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations():
    """Lấy các nước đi hợp lệ (chỉ xét các ô gần các quân đã đi)."""
    valid_locations = set()
    if all(cell == '' for row in board for cell in row):
        return [(BOARD_SIZE//2, BOARD_SIZE//2)]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != '':
                for i in range(r-1, r+2):
                    for j in range(c-1, c+2):
                        if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == '':
                            valid_locations.add((i, j))
    return list(valid_locations)

def minimax(depth, alpha, beta, maximizing_player):
    """Thuật toán Minimax với cắt tỉa Alpha-Beta."""
    valid_locations = get_valid_locations()
    
    # Kiểm tra điều kiện dừng (thắng/thua/hòa)
    is_terminal = False
    if winner: # Biến toàn cục winner
        is_terminal = True

    if depth == 0 or is_terminal:
        if is_terminal:
            if winner == 'AI': return (None, 10000000)
            elif winner == 'PLAYER': return (None, -10000000)
            else: return (None, 0)
        else: # Hết độ sâu tìm kiếm
            return (None, score_position('AI') - score_position('PLAYER'))

    if maximizing_player:
        value = -math.inf
        best_move = valid_locations[0] if valid_locations else None
        for r, c in valid_locations:
            board[r][c] = 'AI'
            # Tạm thời kiểm tra thắng thua để truyền vào đệ quy
            temp_winner = check_win(r,c)
            if temp_winner:
                # Đặt lại biến winner toàn cục nếu có kết quả
                globals()['winner'] = temp_winner
            
            new_score = minimax(depth - 1, alpha, beta, False)[1]
            board[r][c] = ''
            globals()['winner'] = None # Reset lại sau khi thử

            if new_score > value:
                value = new_score
                best_move = (r, c)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_move, value
    else: # Minimizing player
        value = math.inf
        best_move = valid_locations[0] if valid_locations else None
        for r, c in valid_locations:
            board[r][c] = 'PLAYER'
            temp_winner = check_win(r,c)
            if temp_winner:
                globals()['winner'] = temp_winner
            
            new_score = minimax(depth - 1, alpha, beta, True)[1]
            board[r][c] = ''
            globals()['winner'] = None # Reset lại sau khi thử

            if new_score < value:
                value = new_score
                best_move = (r, c)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_move, value

def show_message(message):
    pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT, WIDTH, 50))
    text = FONT.render(message, True, PLAYER_COLOR)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT + 25))
    screen.blit(text, text_rect)

# --- Vòng lặp chính của game ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if turn == 'PLAYER':
                mouseX, mouseY = event.pos
                if mouseY < HEIGHT:
                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE

                    if board[row][col] == '':
                        board[row][col] = 'PLAYER'
                        winner = check_win(row, col)
                        if winner:
                            game_over = True
                        turn = 'AI'

    if turn == 'AI' and not game_over:
        move, score = minimax(AI_SEARCH_DEPTH, -math.inf, math.inf, True)
        if move and board[move[0]][move[1]] == '':
            row, col = move
            board[row][col] = 'AI'
            print(f"AI plays at ({row}, {col}) with score: {score}")
            winner = check_win(row, col)
            if winner:
                game_over = True
            turn = 'PLAYER'

    # Vẽ mọi thứ
    screen.fill(BG_COLOR)
    draw_grid()
    draw_pieces()
    
    # Hiển thị thông báo
    if game_over:
        if winner == 'DRAW':
            show_message("Draw!")
        else:
            show_message(f"'{winner}' won!")
    elif turn == 'PLAYER':
        show_message("Your move (White)")
    else:
        show_message("AI are thinking...")
        
    pygame.display.update()