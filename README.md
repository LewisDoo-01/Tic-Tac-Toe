# Gomoku (Caro) 12x12 Game with AI
## Project Overview

This repository contains a 12x12 Gomoku (also known as "5-in-a-row" or Caro) game implemented in Python using the Pygame library. A human player (White) competes against an AI opponent (Black) that uses the Minimax algorithm with Alpha-Beta Pruning.

<img width="593" height="678" alt="image" src="https://github.com/user-attachments/assets/f80cc718-b50b-44cb-9075-8625a7e2b0d1" />
## How to Play

### Prerequisites

* Python 3.x
* Pygame library

### Installation

1.  Ensure you have a compatible version of Python 3 installed.
2.  Install the Pygame library via pip:
    ```bash
    pip install pygame
    ```

### Running the Game

Execute the main game file from your terminal:

```bash
python game_12x12.py

*Game Rules*
Board: The game is played on a 12x12 grid.

Players: The human is 'Player' (White) ⚪ and the computer is 'AI' (Black) ⚫.

First Move: The AI (Black) always makes the first move, placing a piece in the center of the board.

Objective: The winner is the first player to form an unbroken chain of five of their own pieces, either horizontally, vertically, or diagonally.

Turns: Players alternate turns placing one piece on an empty intersection.

AI Implementation
The AI opponent's logic is based on the Minimax algorithm, a recursive decision-making algorithm for two-player, zero-sum games.

Algorithm: Minimax explores a tree of possible game states. The 'AI' (maximizing player) tries to maximize its score, while assuming the 'Player' (minimizing player) will always play optimally to minimize the AI's score.

Optimization: Alpha-Beta Pruning is implemented to significantly reduce the number of nodes evaluated in the search tree. This optimization "prunes" branches that are guaranteed not to influence the final decision, allowing the AI to search to a greater depth in less time.

Search Depth: The AI's difficulty is controlled by the AI_SEARCH_DEPTH constant, which is set to 2 by default. Increasing this value will result in a stronger AI, but will also increase the time it takes for the AI to compute its move.

Heuristic Evaluation: The score_position and evaluate_window functions provide a heuristic evaluation of the board state. The AI scores potential moves based on creating threats (e.g., 3-in-a-row, 4-in-a-row) and blocking the opponent's threats.

File Descriptions
game_12x12.py: The main executable file containing the game logic, Pygame rendering, and the Minimax AI implementation.

train_ai.py / policy.json: (Unrelated) These files belong to a separate, unrelated project for a 3x3 Tic-Tac-Toe AI. They use Value Iteration (a Reinforcement Learning method) to generate a policy. They are not used by the 12x12 Gomoku game.
