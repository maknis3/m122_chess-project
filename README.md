# Chess Engine Project

## Game Description
Welcome to my chess project! This project is an implementation of chess written in Python. Chess is a classic two-player strategy board game that has been enjoyed for centuries. This engine allows players to engage in chess matches, either against each other, over the board, or against a computer opponent.

## Rules
Chess follows standard rules where each player commands an army with different types of pieces, including pawns, knights, bishops, rooks, queens, and kings. The objective is to checkmate the opponent's king, putting it in a position where it cannot escape capture. This implementation of chess follows the [FIDE LAWS of CHESS](https://www.fide.com/FIDE/handbook/LawsOfChess.pdf).

## End Goal of the Player
The primary goal for players is to strategize and make moves that lead to the checkmate of their opponent's king. This requires careful planning, understanding piece movements, and predicting the opponent's moves. The winning condition is putting the enemy king in a checkmate situation. The draw conditions are the free-fold-repetition, fifty-move-rule, and stalemate. These conditions are further explained in the FIDE chess laws.

## What's Different in My Implementation Compared to Others
- **All-Around Implementation**: My chess implementation, in contrast to most chess projects and engines, includes an all-around implementation of all chess rules and mechanics from the ground up. No external chess libraries or APIs have been used for this project.
- **Chess Engine**: If you select the single-player option, you will play against my attempt at a chess engine implementation. The chess engine incorporates the alpha-beta pruning algorithm to optimize the minimax search for move selection, making the engine more efficient.
- **Game Menu**: The game menu, on the right side of the board, allows the player to look at all past game states via the arrow buttons. Further, the menu displays information as well as possible promotion pieces if a pawn reaches the last rank.
- **Opening Preparation**: The engine includes an opening preparation module, loading opening moves from a JSON file. This feature aims to enhance the engine's performance during the opening phase and simulate "opening knowledge."
- **PGN to JSON Converter**: A PGN (Portable Game Notation) to JSON converter is provided. This tool allows users to convert chess games stored in PGN format to a, in my developed game-notation, structured JSON representation.
- **Board-Viewer**: The board-viewer allows you to display any board-state using my game-notation. Usually used for debugging or testing.

## Getting Started
To get started with the chess engine, follow these steps:
1. Make sure [python](https://www.python.org/downloads/) is installed on your device. 
2. Install pygame.
    ```bash
    pip install pygame
    ```
3. Clone the repository:
    ```bash
    git clone https://github.com/maknis3/m122_chess-project.git
    ```
4. Navigate to the project directory:
    ```bash
    cd M122_CHESS-PROJECT
    ```
5. Execute the main Python file:
    ```bash
    python main.py
    ```

Feel free to explore and enjoy playing chess with the implemented engine or learn and copy from my code!

## PGN to JSON Converter
The PGN to JSON converter is a valuable tool included in this project. It allows users to convert any chess game(s) saved in PGN format to JSON, providing a structured and machine-readable representation of the games.
The final JSON file contains a dictionary for each color. This dictionary contains the game-state as a key and all moves made in the provided games on this game-state as entries. Note here that only the first five moves of the games are processed.
Open-source PGN-files can be found on the [FICS Games Database](https://www.ficsgames.org/download.html).

### How to Use the PGN to JSON Converter
1. **Ensure Python is Installed**: Make sure you have Python installed on your system.
2. **Ensure Python is Installed**: Change the lines 208 and 209 of the pgn_to_json.py file to your dir.
3. **Run the Converter Script**: Execute the converter script.
    ```bash
    python pgn_to_json.py
    ```
4. **Output JSON File**: The converter will generate a JSON file containing the converted game data.

## Chess Engine
My implementation of a chess engine, as mentioned above, is based on a [MiniMax](https://en.wikipedia.org/wiki/Minimax) algorithm with [alpha-beta-pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). The evaluation of the game-state is implemented in the evaluate method. This method is by far not optimal or efficient. The evaluation is based on the present pieces, their position, and if a check is present. The following implementations could enhance the evaluations but also further slow down the engine:
- **Move ordering**: When the possible moves are ordered from promising to not interesting, the alpha-beta pruning would be far more effective. This would hugely improve the engine's performance. Unfortunately, I see no possible implementation with the current code-base without enormous calculation outweighing the performance improvement.
- **Impact consideration**: If the evaluation method would implement the impact of all pieces, it could represent a much more realistic picture of the game-state. For example, if my queen is attacked by a pawn after my move, it is as good as lost, therefore not worth a lot. But with the current implementation, these situations aren't taken into consideration. Like the previous point, the implementation of this would have an enormous performance impact.
- **Exchange chain tracking**: In chess, a lot of strategic play takes place, where each player tries to have more influence over a square than the other. In that instance, it would be important to follow the exchange-chain to the end and see if one comes out on top. This would further enhance the evaluation of each move-tree at the cost of more calculation. This has been partially implemented.
- **Improved opening preparation**: The current opening preparation is based on all standard, over 2000 rated games of 2023 on the FICS Database. In the implementation, the probability for each move is equal, but in reality, they aren't. A move like e4 is much more common and promising compared to a4. Implementing the frequency of each move to the opening preparation would further enhance the set-up of the engine in the opening stage and therefore promise a better outcome.
- **Flexible promotion choice**: At the moment, the engine can't choose its promotion piece. For simplicity, it's restricted to promoting to a queen. The implementation of this would be rather easy, but that's not really a big weakness of the engine at the moment, so has been left to do for a later date.

## Next?
Implementing chess was a fun and educational challenge. Moving forward, I have exciting ideas to further enhance this project and explore new projects. Here's a glimpse into the future developments:
- **More Features**: Continuing to evolve the engine, I plan to introduce several new features. Improving the engine's logic is a priority, and enhancements to the menu are in the pipeline. This includes adding a reset button, displaying the engine's evaluation for the current board, implementing a board-flipping button, and creating a display for all captured pieces. Additionally, I'm intrigued by the challenge of incorporating a drag-and-drop mechanic for chess pieces, similar to platforms like [chess.com](https://www.chess.com/home), using the pygame library.
- **User Interface Enhancements**: Elevating the overall user experience is crucial. I intend to explore opportunities for UI enhancements, such as refining visual design elements, incorporating animations, and introducing interactive features to make the gameplay more engaging. In this aspect I'd like to switch from pygame to something newer and user friendlier.
- **Online Multiplayer**: Maybe the implementation of an online multiplayer mode would be a fun challenge. This feature will enable players to engage in chess matches with opponents over the internet.
- **Mobile App Version**: I'm considering developing a mobile app version of the chess engine. 
- **Other Language**: Despite my love for Python, I'm eager to explore implementations in other languages, such as C++. This exploration will focus on creating a more optimized solution tailored to the specific challenges posed by a chess engine.
- **Chess Library Integration**: Throughout this process, I haven't extensively explored existing chess libraries for Python. Considering the fun challenges that might arise, I'm contemplating the use of established libraries or APIs to enhance specific functionalities within the project.
The journey doesn't end here, and I'm excited about the possibilities that lie ahead, if there is time I'd like to continue my development. Your feedback and contributions are always welcome!

## Sources
- [Chess piece images](https://greenchess.net/info.php?item=downloads)
- [Chess color-selection piece images](https://www.pngegg.com/)
- [Icons](https://www.flaticon.com/)
- [Opening prep data](https://www.ficsgames.org/download.html)