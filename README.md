# Hand Tracking Game - Grip The Finger Game

This project is a hand tracking game that challenges players to fold specific fingers in a sequence using their hands. The game uses `MediaPipe` for hand tracking, `OpenCV` for displaying the game and handling video capture, and `NumPy` for image manipulation.

## Features

- Hand tracking with MediaPipe to detect fingers.
- A timer to challenge players to complete finger sequences within a given time limit.
- Randomly generated sequences of finger folding.
- Score tracking based on correct finger sequences.
- A simple GUI for starting the game, selecting the timer duration, and displaying the game-over screen.
- Ability to replay or quit the game after it ends.

## Installation

To run this game, you need to have Python 3.6 or later installed.

### Step 1: Clone the repository

bash
git clone https://github.com/yourusername/hand-tracking-game.git
cd GRIP_THE_FINGER_GAME

### Step 2: Set up a Python virtual environment (optional but recommended)
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

### Step 3: Install dependencies
echo "Installing required dependencies..."
pip install -r requirements.txt

### Step 4: Running the game
echo "Running the game..."
python game.py

### Instructions for the user
cat <<EOF
Game Instructions:

1. **Start the Game:**
   - When the game starts, press **S** to proceed to the timer selection.
   
2. **Select Timer:**
   - Choose a timer duration by pressing:
     - **1** for 15 seconds
     - **2** for 30 seconds
     - **3** for 60 seconds
   - Press **B** to return to the start screen if you want to return the menu.

3. **Play the Game:**
   - Follow the on-screen instructions to fold the correct fingers in the sequence.
   - The game will detect folded fingers and check them against the current sequence.
   - If you fold the wrong fingers, the game will give you a warning.

4. **Game Over:**
   - Once the timer runs out, the game will show your score.
   - You can press **R** to replay or **Q** to quit the game.

Libraries Used:
- OpenCV
- MediaPipe
- NumPy

EOF

echo "Setup complete! Enjoy the game!"