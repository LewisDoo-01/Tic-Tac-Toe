# File: train_ai.py (FIXED VERSION)
import json
from collections import defaultdict

# --- Cài đặt cơ bản ---
WIN_REWARD = 1.0
LOSE_REWARD = -1.0
DRAW_REWARD = 0.0
STEP_REWARD = 0.0
GAMMA = 0.9  # Hệ số chiết khấu

def get_winner(board):
    """Kiểm tra xem ai thắng hoặc hòa."""
    # Hàng và Cột
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ': return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ': return board[0][i]
    # Đường chéo
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ': return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ': return board[0][2]
    # Hòa
    if ' ' not in [cell for row in board for cell in row]: return 'DRAW'
    return None

def generate_states(board, player, all_states):
    """Đệ quy để sinh ra tất cả các trạng thái có thể của bàn cờ."""
    winner = get_winner(board)
    if winner is not None:
        return

    # THAY ĐỔI / FIXED: Biểu diễn trạng thái thành một chuỗi 9 ký tự duy nhất.
    state_key = "".join("".join(row) for row in board)
    
    if state_key in all_states:
        return
    all_states.add(state_key)

    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                new_board = [list(row) for row in board]
                new_board[r][c] = player
                next_player = 'O' if player == 'X' else 'X'
                generate_states(new_board, next_player, all_states)

def train():
    """Chạy Value Iteration để tính giá trị các trạng thái và tạo policy."""
    print("Bắt đầu sinh ra các trạng thái...")
    initial_board = [[' ' for _ in range(3)] for _ in range(3)]
    all_states = set()
    generate_states(initial_board, 'X', all_states)
    print(f"Đã tìm thấy {len(all_states)} trạng thái hợp lệ.")

    V = defaultdict(float) # Bảng giá trị V(s), khởi tạo bằng 0
    
    # Khởi tạo giá trị cho các trạng thái kết thúc
    for state_key in all_states:
        # THAY ĐỔI / FIXED: Tái tạo board từ chuỗi 9 ký tự.
        board = [list(state_key[i:i+3]) for i in range(0, 9, 3)]
        winner = get_winner(board)
        if winner == 'X': V[state_key] = LOSE_REWARD   # AI là 'O' nên nếu 'X' thắng, AI thua
        elif winner == 'O': V[state_key] = WIN_REWARD  # Ngược lại
        elif winner == 'DRAW': V[state_key] = DRAW_REWARD

    print("Bắt đầu Value Iteration...")
    # Lặp cho đến khi hội tụ
    for i in range(100): # 100 lần lặp là quá đủ cho Tic Tac Toe
        V_old = V.copy()
        for state_key in all_states:
            # THAY ĐỔI / FIXED: Tái tạo board từ chuỗi 9 ký tự.
            board = [list(state_key[i:i+3]) for i in range(0, 9, 3)]
            
            if get_winner(board) is not None: continue
                
            num_x = state_key.count('X')
            num_o = state_key.count('O')
            player = 'X' if num_x == num_o else 'O'
            
            action_values = []
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = player
                        # THAY ĐỔI / FIXED: Tạo key cho trạng thái tiếp theo
                        next_state_key = "".join("".join(row) for row in board)
                        action_values.append(STEP_REWARD + GAMMA * V_old[next_state_key])
                        board[r][c] = ' ' # Hoàn tác
            
            if not action_values: continue

            if player == 'X':
                V[state_key] = max(action_values)
            else: # AI's turn ('O')
                V[state_key] = min(action_values)


    print("Value Iteration hoàn tất. Đang trích xuất chính sách...")
    policy = {}
    for state_key in all_states:
        # THAY ĐỔI / FIXED: Tái tạo board từ chuỗi 9 ký tự.
        board = [list(state_key[i:i+3]) for i in range(0, 9, 3)]
        
        num_x = state_key.count('X')
        num_o = state_key.count('O')
        
        if num_x <= num_o or get_winner(board) is not None:
            continue

        best_move = None
        min_val = float('inf') 
        
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'O'
                    # THAY ĐỔI / FIXED: Tạo key cho trạng thái tiếp theo
                    next_state_key = "".join("".join(row) for row in board)
                    if V[next_state_key] < min_val:
                        min_val = V[next_state_key]
                        best_move = (r, c)
                    board[r][c] = ' ' # Hoàn tác
        
        policy[state_key] = best_move

    # Lưu policy vào file
    with open('policy.json', 'w') as f:
        # Bây giờ key đã là string sẵn nên không cần chuyển đổi
        json.dump(policy, f)
        
    print("Đã lưu chính sách vào file 'policy.json'. Bạn có thể chạy game.py ngay bây giờ.")

if __name__ == "__main__":
    train()