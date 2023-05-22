import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width, window_height = 650, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

# Define block shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]
SHAPES_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]

# Define block properties
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (window_width - BLOCK_SIZE * GRID_WIDTH) // 2
GRID_OFFSET_Y = (window_height - BLOCK_SIZE * GRID_HEIGHT) // 2

# Define the size and position of the next piece display
NEXT_PIECE_SIZE = 4
NEXT_PIECE_OFFSET_X = GRID_OFFSET_X + GRID_WIDTH * BLOCK_SIZE + 50
NEXT_PIECE_OFFSET_Y = GRID_OFFSET_Y + BLOCK_SIZE

# Initialize the grid
grid = [[None] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Create a new block
def create_block():
    shape = random.choice(SHAPES)
    color = random.choice(SHAPES_COLORS)
    block = {
        "shape": shape,
        "color": color,
        "x": GRID_WIDTH // 2 - len(shape[0]) // 2,
        "y": 0
    }
    return block
	

# Check if a position is valid for the current block
def is_valid_position(block, dx=0, dy=0):
    for row in range(len(block["shape"])):
        for col in range(len(block["shape"][row])):
            if block["shape"][row][col]:
                x = block["x"] + col + dx
                y = block["y"] + row + dy
                if (
                    x < 0 or
                    x >= GRID_WIDTH or
                    y >= GRID_HEIGHT or
                    (y >= 0 and grid[y][x])
                ):
                    return False
    return True

# Place the current block onto the grid
def place_block(block):
    for row in range(len(block["shape"])):
        for col in range(len(block["shape"][row])):
            if block["shape"][row][col]:
                x = block["x"] + col
                y = block["y"] + row
                grid[y][x] = block["color"]
				
    global delay_time
    if delay_time>50:
        delay_time = delay_time -5 

# Remove completed rows
def remove_completed_rows():
    rows_to_remove = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            rows_to_remove.append(row)
    for row in rows_to_remove:
        del grid[row]
        grid.insert(0, [None] * GRID_WIDTH)
    return len(rows_to_remove)

# Draw the grid and blocks
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = grid[row][col]
            if color:
                pygame.draw.rect(
                    window,
                    color,
                    (GRID_OFFSET_X + col * BLOCK_SIZE, GRID_OFFSET_Y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
            pygame.draw.rect(
                window,
                WHITE,
                (GRID_OFFSET_X + col * BLOCK_SIZE, GRID_OFFSET_Y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )
			



# Draw the current block
def draw_block(block):
    for row in range(len(block["shape"])):
        for col in range(len(block["shape"][row])):
            if block["shape"][row][col]:
                pygame.draw.rect(
                    window,
                    block["color"],
                    (
                        GRID_OFFSET_X + (block["x"] + col) * BLOCK_SIZE,
                        GRID_OFFSET_Y + (block["y"] + row) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    )
                )

def draw_next_piece(next_piece):
    shape = next_piece["shape"]
    color = next_piece["color"]
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                x = NEXT_PIECE_OFFSET_X + col * BLOCK_SIZE
                y = NEXT_PIECE_OFFSET_Y + row * BLOCK_SIZE
                pygame.draw.rect(window, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(window, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 2)
# Check if the game is over
def is_game_over():
    return any(grid[0])

# Game loop
clock = pygame.time.Clock()
fall_time = 0
block = create_block()
next_piece = create_block()
game_over = False
score = 0
delay_time = 500  # Delay in milliseconds before the tetromino is locked in place
last_move_time = pygame.time.get_ticks()
piece_placed = False


def update_score(rows_removed):
    global score
    score += 10
    score += rows_removed * 100  # Score for removing rows
    if rows_removed == 4:
        score += 400  # Bonus score for removing four rows
		
# Create a font for rendering the score
font = pygame.font.SysFont(None, 36)

# Render the initial score text
score_text = font.render("Score: 0", True, WHITE)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and is_valid_position(block, dx=-1):
                block["x"] -= 1
            elif event.key == pygame.K_RIGHT and is_valid_position(block, dx=1):
                block["x"] += 1
            elif event.key == pygame.K_DOWN and is_valid_position(block, dy=1):
                block["y"] += 1
            elif event.key == pygame.K_UP:
                rotated_shape = list(zip(*reversed(block["shape"])))
                if is_valid_position({"shape": rotated_shape, "x": block["x"], "y": block["y"]}):
                    block["shape"] = rotated_shape
            elif event.key == pygame.K_SPACE:
                while is_valid_position(block, dy=1):
                    block["y"] += 1
                place_block(block)
                piece_placed=True
                rows_removed = remove_completed_rows()
                update_score(rows_removed)
                
                if is_game_over():
                    game_over = True
				

    # Update
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > delay_time:
        if is_valid_position(block, dy=1):
            block["y"] += 1
        else:
            place_block(block)
            rows_removed = remove_completed_rows()
            update_score(rows_removed)
            block = next_piece
            if is_game_over():
                game_over = True
				
            next_piece = create_block()
        last_move_time = current_time
		
    # Choose the next piece
    

    # Render
    window.fill(BLACK)
    draw_grid()
    draw_block(block)
    window.blit(score_text, score_text_rect)
    draw_next_piece(next_piece)
    pygame.display.update()


	# Delay to achieve a consistent frame rate
    clock.tick(30)

	
	

    # Blit the score onto the window surface
    window.blit(score_text, score_text_rect)
    
    pygame.display.update()
	
	# Check if the score has changed
    new_score_text = font.render("Score: " + str(score), True, WHITE)
    if new_score_text.get_rect().width != score_text.get_rect().width:
        score_text = new_score_text
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 10)


# Print final score
print("Game Over")
print("Final Score:", score)

# Quit the game
pygame.quit()
