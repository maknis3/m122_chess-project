# Chess Engine Project

## Game Description
Welcome to the Chess Engine project! This project is an implementation of a chess engine written in Python. Chess is a classic two-player strategy board game that has been enjoyed for centuries. This engine allows players to engage in chess matches, either against each other or against a computer opponent.

## Rules
Chess follows standard rules where each player commands an army with different types of pieces, including pawns, knights, bishops, rooks, queens, and kings. The objective is to checkmate the opponent's king, putting it in a position where it cannot escape capture.

## Target/End Goal of the Player
The primary goal for players is to strategize and make moves that lead to the checkmate of their opponent's king. This requires careful planning, understanding piece movements, and predicting the opponent's moves.

## What's Different in My Implementation Compared to Others
- **Alpha-Beta Pruning**: The chess engine incorporates the alpha-beta pruning algorithm to optimize the minimax search for move selection, making the engine more efficient.
- **Opening Preparation**: The engine includes an opening preparation module, loading opening moves from a JSON file. This feature aims to enhance the engine's performance during the opening phase.
- **PGN to JSON Converter**: A PGN (Portable Game Notation) to JSON converter is provided. This tool allows users to convert chess games stored in PGN format to a structured JSON representation.

## PGN to JSON Converter
The PGN to JSON converter is a valuable tool included in this project. It allows users to convert chess games saved in PGN format to JSON, providing a structured and machine-readable representation of the games.

### How to Use the PGN to JSON Converter
1. **Ensure Python is Installed**: Make sure you have Python installed on your system.
2. **Run the Converter Script**: Execute the converter script, providing the path to the PGN file as an argument.
    ```bash
    python pgn_to_json_converter.py your_chess_game.pgn
    ```
3. **Output JSON File**: The converter will generate a JSON file containing the converted game data.

## Getting Started
To get started with the chess engine, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/chess-engine.git
    ```
2. Navigate to the project directory:
    ```bash
    cd chess-engine
    ```
3. Run the chess engine:
    ```bash
    python chess_engine.py
    ```

Feel free to explore and enjoy playing chess with the implemented engine!

## Contributors
- Your Name
- Any additional contributors

## License
This project is licensed under the [MIT License](LICENSE).
