def on_up_pressed():
    doAction(3)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def on_b_pressed():
    global speed_ms
    if speed_ms < 1000:
        speed_ms = speed_ms + 50
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def on_a_pressed():
    global speed_ms
    if speed_ms > 50:
        speed_ms = speed_ms - 50
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def getReward(state_index: number, action_index: number):
    if state_index >= 3072:
        return getRewardWithLocationOffset(state_index, action_index, 3072, 2, 1)
    elif state_index >= 2048:
        return getRewardWithLocationOffset(state_index, action_index, 2048, 2, 0)
    elif state_index >= 1024:
        return getRewardWithLocationOffset(state_index, action_index, 1024, 3, 0)
    else:
        return getRewardWithLocationOffset(state_index, action_index, 0, 3, 1)

def on_left_pressed():
    doAction(1)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def eatFood():
    if snake_head.overlaps_with(snake_food):
        while snake_head.overlaps_with(snake_food) or tiles.tile_at_location_equals(snake_food.tilemap_location(), body_tile):
            tiles.place_on_tile(snake_food,
                tiles.get_tile_location(randint(2, 11), randint(2, 9)))
        snake_list.unshift(snake_head.tilemap_location())
        info.change_score_by(1)
def updateQualityTable(state_index2: number, action_index2: number, alpha: number, gamma: number):
    quality_table[state_index2][action_index2] = (1 - alpha) * quality_table[state_index2][action_index2] + (alpha * getReward(getStateIndex(), action_index2) + alpha * gamma * getMaxReward(action_index2))
    print(quality_table[state_index2])

def on_right_pressed():
    doAction(0)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def getStateIndex():
    if snake_head.tilemap_location().column >= snake_food.tilemap_location().column and snake_head.tilemap_location().row >= snake_food.tilemap_location().row:
        return 0 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    elif snake_head.tilemap_location().column < snake_food.tilemap_location().column and snake_head.tilemap_location().row >= snake_food.tilemap_location().row:
        return 1024 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    elif snake_head.tilemap_location().column < snake_food.tilemap_location().column and snake_head.tilemap_location().row < snake_food.tilemap_location().row:
        return 2048 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    elif snake_head.tilemap_location().column >= snake_food.tilemap_location().column and snake_head.tilemap_location().row < snake_food.tilemap_location().row:
        return 3072 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    return 0
def initGame(food_img: Image, head_img: Image, body_img: Image, bgrd_img: Image, wall_img: Image):
    global speed_ms, snake_food, snake_head, body_tile, bgrd_tile, wall_tile
    speed_ms = 350
    snake_food = sprites.create(food_img, SpriteKind.food)
    snake_head = sprites.create(head_img, SpriteKind.player)
    scene.camera_follow_sprite(snake_head)
    body_tile = body_img
    bgrd_tile = bgrd_img
    wall_tile = wall_img
def moveSnake():
    global index2
    index2 = 0
    while index2 <= len(snake_list) - 1:
        if index2 == 0:
            tiles.set_tile_at(snake_list[index2], bgrd_tile)
        if index2 == len(snake_list) - 1:
            snake_list[index2] = tiles.get_tile_location(snake_list[index2].column + colInc,
                snake_list[index2].row + rowInc)
            tiles.place_on_tile(snake_head, snake_list[index2])
        else:
            snake_list[index2] = tiles.get_tile_location(snake_list[index2 + 1].column, snake_list[index2 + 1].row)
            tiles.set_tile_at(snake_list[index2], body_tile)
        index2 += 1
def resetSnakeGame():
    global snake_list
    tiles.set_current_tilemap(tilemap("""
        level1
    """))
    for value in tiles.get_tiles_by_type(assets.tile("""
        Wall
    """)):
        tiles.set_tile_at(value, wall_tile)
    for value2 in tiles.get_tiles_by_type(assets.tile("""
        myTile0
    """)):
        tiles.set_tile_at(value2, bgrd_tile)
    tiles.place_on_tile(snake_food,
        tiles.get_tile_location(randint(2, 11), randint(2, 9)))
    snake_list = []
    snake_list.unshift(tiles.get_tile_location(4, 4))
    tiles.place_on_tile(snake_head, snake_list[0])
    snake_list.unshift(snake_head.tilemap_location())
    doAction(2)
def getRewardWithLocationOffset(state_index3: number, action_index3: number, index_offset: number, ref_action_1: number, ref_action_2: number):
    if state_index3 - index_offset >= 512:
        return -10
    elif state_index3 - index_offset >= 256:
        return 10
    elif action_index3 == ref_action_1 or action_index3 == ref_action_2:
        return 1
    else:
        return -1
def checkCollision():
    if tiles.tile_at_location_equals(snake_head.tilemap_location(), wall_tile) or tiles.tile_at_location_equals(snake_head.tilemap_location(), body_tile):
        info.change_score_by(1)
        pause(200)
        resetSnakeGame()

def on_down_pressed():
    doAction(2)
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def getStateIdx(column_offset: number, row_offset: number, base: number):
    if snake_head.tilemap_location().column + column_offset == snake_food.tilemap_location().column and snake_head.tilemap_location().row + row_offset == snake_food.tilemap_location().row:
        return base
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + column_offset,
            snake_head.tilemap_location().row + row_offset),
        body_tile):
        return base * 2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + column_offset,
            snake_head.tilemap_location().row + row_offset),
        wall_tile):
        return base * 2 + base
    else:
        return 0
def getMaxReward(stateIdx2: number):
    return max(max(quality_table[stateIdx2][0], quality_table[0][stateIdx2]),
        max(quality_table[0][2], quality_table[stateIdx2][3]))
def doAction(Idx: number):
    global colInc, rowInc
    if Idx == 3:
        colInc = 0
        rowInc = -1
        return Idx
    elif Idx == 2:
        colInc = 0
        rowInc = 1
        return Idx
    elif Idx == 1:
        colInc = -1
        rowInc = 0
        return Idx
    elif Idx == 0:
        colInc = 1
        rowInc = 0
        return Idx
    else:
        return -1
def callAgentForAction(state_index4: number):
    global iMaxIdx
    iMaxIdx = 0
    for index3 in range(5):
        if quality_table[state_index4][index3] > quality_table[state_index4][iMaxIdx]:
            iMaxIdx = index3
    return doAction(iMaxIdx)
def initQLearingEnv(alpha2: number, gamma2: number):
    global learning_rate, discount_factor, quality_table
    learning_rate = alpha2
    discount_factor = gamma2
    quality_table = []
    for index in range(4096):
        quality_table.append([0, 0, 0, 0])
current_action = 0
current_state = 0
discount_factor = 0
learning_rate = 0
iMaxIdx = 0
rowInc = 0
colInc = 0
index2 = 0
wall_tile: Image = None
bgrd_tile: Image = None
quality_table: List[List[number]] = []
snake_list: List[tiles.Location] = []
body_tile: Image = None
snake_food: Sprite = None
snake_head: Sprite = None
speed_ms = 0
info.set_score(-500)
initQLearingEnv(0.2, 0.5)
initGame(img("""
        . . 2 2 2 2 2 2 2 2 2 2 2 2 . . 
            . 2 2 2 2 2 2 2 2 2 2 2 2 2 2 . 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 
            . 2 2 2 2 2 2 2 2 2 2 2 2 2 2 . 
            . . 2 2 2 2 2 2 2 2 2 2 2 2 . .
    """),
    img("""
        . . 7 7 7 7 7 7 7 7 7 7 7 7 . . 
            . 7 7 7 7 7 7 7 7 7 7 7 7 7 7 . 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 
            . 7 7 7 7 7 7 7 7 7 7 7 7 7 7 . 
            . . 7 7 7 7 7 7 7 7 7 7 7 7 . .
    """),
    myTiles.tile3,
    sprites.castle.tile_path5,
    sprites.dungeon.floor_dark0)
resetSnakeGame()

def on_on_update():
    global current_state, current_action
    pause(speed_ms)
    checkCollision()
    eatFood()
    current_state = getStateIndex()
    if info.score() < 0 and randint(0, 100) < 20:
        current_action = doAction(randint(0, 3))
    else:
        current_action = callAgentForAction(current_state)
    moveSnake()
    snake_head.say_text(getReward(getStateIndex(), current_action))
    updateQualityTable(current_state,
        current_action,
        learning_rate,
        discount_factor)
game.on_update(on_on_update)
