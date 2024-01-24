# Chess Engine Project

## Game Description
Welcome to my chess project! This project is an implementation of chess written in Python. Chess is a classic two-player strategy board game that has been enjoyed for centuries. This engine allows players to engage in chess matches, either against each other, over the board, or against a computer opponent.

## Rules
Chess follows standard rules where each player commands an army with different types of pieces, including pawns, knights, bishops, rooks, queens, and kings. The objective is to checkmate the opponent's king, putting it in a position where it cannot escape capture. This implementation of chess follows the [FIDE LAWS of CHESS](https://www.fide.com/FIDE/handbook/LawsOfChess.pdf). 

## End Goal of the Player
The primary goal for players is to strategize and make moves that lead to the checkmate of their opponent's king. This requires careful planning, understanding piece movements, and predicting the opponent's moves. The winning-condition is putting the enemy king in a checkmate situation. The draw conditions are the free-fold-repetition, fifty-move-rule and stalemate. These conditions are further explained in the FIDE-chesslaws. 

## What's Different in My Implementation Compared to Others
- **All-Around Implementation**: My chess-implementation, in contrast to most chessprojects and engines, includes an all-around implementation of all chess-rules and mechanics from ground up. No external chess-librarys or APIs in have been used for this project.
- **Chess Engine**: If you select the single-player option, you will play against my try of an chess-engine-implementation. The chess engine incorporates the alpha-beta pruning algorithm to optimize the minimax search for move selection, making the engine more efficient.
- **Game Menu**: The game menu, on the rightside of the board, allows the player to look at all past game-states via the arrow-buttons. Further does the menu display information as well as display the possible promotion pieces, if a pawn reaches the last rank. 
- **Opening Preparation**: The engine includes an opening preparation module, loading opening moves from a JSON file. This feature aims to enhance the engine's performance during the opening phase and simulate "opening knowledge".
- **PGN to JSON Converter**: A PGN (Portable Game Notation) to JSON converter is provided. This tool allows users to convert chess games stored in PGN format to a, in my developed game-notation, structured JSON representation.

## Getting Started
To get started with the chess engine, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/chess-engine.git
    ```
2. Navigate to the project directory:
    ```bash
    cd M122_CHESS-PROJECT
    ```
3. Execute the main python file:
    ```bash
    python main.py
    ```

Feel free to explore and enjoy playing chess with the implemented engine or learn and copy from my code!

## PGN to JSON Converter
The PGN to JSON converter is a valuable tool included in this project. It allows users to convert any chess game(s) saved in PGN format to JSON, providing a structured and machine-readable representation of the games. 
The final JSON file contains a dictionary for each color. This dictionary contains the game-state as a key and all moves made in the provided games on this game-state as entrys. Note here that only the first five moves of the games are processed. 
Open-source PGN-files can be found on the [FICS Games Database](https://www.ficsgames.org/download.html).

### How to Use the PGN to JSON Converter
1. **Ensure Python is Installed**: Make sure you have Python installed on your system.
2. **Run the Converter Script**: Execute the converter script, providing the path to the PGN file as an argument.
    ```bash
    python pgn_to_json_converter.py your_chess_game.pgn
    ```
3. **Output JSON File**: The converter will generate a JSON file containing the converted game data.

## Chess Engine
My implementation of a chess engine, as mentioned above, is based on a [MiniMax](https://en.wikipedia.org/wiki/Minimax) algorithm with [alpha-beta-pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). The evaluation of the game-state is implemented in the evaluate method. This method is by far not optimal or efficient. The evaluation is based on the present pieces, their position and if a check is present. The following immplementations could enhance the evaluations but also further slow down the engine: 
- **Move ordering**: When the possible moves are ordered from promising to not interesting the alpha-beta pruning would be far more effective. This would houghely improve the engines performance. Unfortunately i see no possible implementation with the current code-base without enormous calulation outweighing the perfomance improvement. 
- **Consider impact**: If the evaluation method would implement the impact of all pieces, it could represent a much more realistic picture of the game-state. For example if my queen is attacked by a pawn after my move, it is as good as lost, therefore not worth a lot. But with the current implementation these situations aren't take into consideration. Like the previous point, the implementation of this would have an enormous performance-impact. 
- **Follow exchange**: In chess a lot of strategic play takes place, where each player trys to have more influence over a square than the other. In that instance it would be important to follow the exchange-chain to the end and see if one comes out on top. This would further enhance the evaluation of each move-tree at a cost of more calculation. This has been partially implemented. 
- **Opening Preparation**: The current opening preparation is based on all standart, over 2000 rated games of 2023 on the FICS Database. In the implementation the probability for each move is equal, but in reality they aren't. A move like e4 is much more commen and promising compared to a4. Implementing the frequency of each move to the opening preparation would further enhance the set-up of the engine in the opening-stage and therefore promise a better outcome. 
- **Promotion**: At the moment the engine can't choose its promotion piece. For simplicity it's restricted to promoting to a queen. The implementation of this would be rather easy, but that's not really a big weakness of the engine at the moment, so has been left to do for a later date. 
