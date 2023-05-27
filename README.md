# tetris-python-game
a python tetris game, to be used for rl, it works ok.<br>
FEATURES<br>
##############<br>
1 Incrementing speed based on blocks placed(from 500 up to 50ms ) its the time the tetromino needs to get to the next line<br>
2 scoring system shown on screen(10 for every block placed,100 for a row,800 for a tetris)<br>
3 Next piece Shown on screen(top right)<br>
4 Movement buffer 500ms after being placed (you can still do an input or 2)<br>
5 movement of block(left, right , rotate, drop in place)<br>
<br>
<br>
Changes made for the agent<br>
reward variable for rl<br>
the grid is represented as a 10x20 grid everytime a piece is placed<br>
when a new piece is created the tuple is saved and padded to become a 4x4 matrix<br>
the same happens for the next piece shown top right <br>
if the piexe is rotated the 4x4 matrix is updated<br>
look at game_screen.png and game_states.png for example<br>
