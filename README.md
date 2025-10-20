<h1> Gomoku (Caro) 12x12 Game with AI </h1>

<img width="593" height="678" alt="image" src="https://github.com/user-attachments/assets/f80cc718-b50b-44cb-9075-8625a7e2b0d1" />

This is a Gomoku (also known as Caro or 5-in-a-row) game written in Python and Pygame. You (White pieces) will compete against an AI (Black pieces) on a 12x12 board.

Features
12x12 Board: A simple graphical interface using Pygame.

Gomoku Rules: The objective is to get 5 of your pieces in a continuous line (horizontally, vertically, or diagonally).

AI Opponent: The AI uses the Minimax algorithm with Alpha-Beta Pruning to find the optimal move.

First Move: Following standard Gomoku rules, the AI (Black) plays first.

How to Run
Prerequisites
Python 3

Pygame library

Installation
Ensure you have Python 3 installed.

Install the Pygame library using pip:

Bash

pip install pygame
Running the Game
You only need to run the game_12x12.py file to start the game:

Bash

python game_12x12.py
Important Note: The files train_ai.py and policy.json are not used for this 12x12 Gomoku game. They belong to a different project (an AI for a 3x3 Tic-Tac-Toe game).

Game Rules
Player: You control the White pieces (PLAYER_COLOR).

AI: The computer controls the Black pieces (AI_COLOR).

First Move: The AI (Black) always goes first.

Objective: The first player to get 5 pieces in a row (horizontal, vertical, or diagonal) wins.

Your Turn: When it's your turn, click on an empty square on the board to place your piece.

About the AI
The AI for this game is programmed using the Minimax algorithm:

Minimax: This is a recursive algorithm used to find the best move in two-player, zero-sum games. It simulates all possible moves up to a certain depth.

Alpha-Beta Pruning: An optimization technique for Minimax that safely prunes (cuts off) unnecessary branches of the search tree, allowing the AI to look deeper in the same amount of time.

Heuristic Evaluation: The AI uses an evaluation function (score_position, evaluate_window) to score the board state. It gives high priority to creating 4-in-a-row and 3-in-a-row threats while simultaneously blocking the player's similar threats.

Search Depth: The AI's difficulty is determined by the AI_SEARCH_DEPTH variable (default is 2). You can increase this value in the code to make the AI stronger, but it will also take longer to think.
