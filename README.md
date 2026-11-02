# Ping-Pong

A two-player ping-pong game written in Python with object-oriented programming.
It uses Python's built-in `turtle` graphics, so no third-party packages are
needed.

## Run

```powershell
python main.py
```

## Controls

- Left player: **W** to move up, **S** to move down
- Right player: **Up Arrow** to move up, **Down Arrow** to move down
- Hold a movement key to move continuously; release it to stop.
- **Space**: pause or resume
- **Escape**: quit

## Project files

- `main.py` starts the game.
- `game.py` sets up the screen, handles collisions and scoring, and runs the
  animation loop.
- `court.py` draws the court markings.
- `paddle.py` defines the player paddles.
- `ball.py` defines the ball and its movement.
- `scoreboard.py` displays both players' scores.
- `settings.py` contains shared game settings.
