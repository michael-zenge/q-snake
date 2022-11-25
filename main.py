def on_up_pressed():
    doAction(3)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def getState2(column_offset: number, row_offset: number, base: number):
    if snake_head.tilemap_location().column + column_offset == snake_food.tilemap_location().column and snake_head.tilemap_location().row + row_offset == snake_food.tilemap_location().row:
        return base
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + column_offset,
            snake_head.tilemap_location().row + row_offset),
        assets.tile("""
            myTile
        """)):
        return base * 2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + column_offset,
            snake_head.tilemap_location().row + row_offset),
        assets.tile("""
            Wall
        """)):
        return base * 2 + base
    else:
        return 0

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

def initQualityTable():
    global quality_table
    quality_table = []
    for index in range(4096):
        quality_table.append([0, 0, 0, 0])
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

def setGlobalVariables():
    global speed_ms, learning_rate, discount_factor, snake_food, snake_head
    speed_ms = 350
    learning_rate = 1
    discount_factor = 0.5
    snake_food = sprites.create(img("""
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
        SpriteKind.food)
    snake_head = sprites.create(img("""
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
        SpriteKind.player)
    scene.camera_follow_sprite(snake_head)
def eatFood():
    if snake_head.overlaps_with(snake_food):
        while snake_head.overlaps_with(snake_food) or tiles.tile_at_location_equals(snake_food.tilemap_location(),
            assets.tile("""
                myTile
            """)):
            tiles.place_on_tile(snake_food,
                tiles.get_tile_location(randint(2, 11), randint(2, 9)))
        snake_list.unshift(snake_head.tilemap_location())
        info.change_score_by(1)

def on_right_pressed():
    doAction(0)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def update_quality_table(state_index2: number, action_index2: number, alpha: number, gamma: number):
    quality_table[state_index2][action_index2] = (1 - alpha) * quality_table[state_index2][action_index2] + (alpha * getReward(getStateIndex(), action_index2) + alpha * gamma * getMaxReward(action_index2))
    print(quality_table[state_index2])
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
def moveSnake():
    global index2
    index2 = 0
    while index2 <= len(snake_list) - 1:
        if index2 == 0:
            tiles.set_tile_at(snake_list[index2], assets.tile("""
                myTile0
            """))
        if index2 == len(snake_list) - 1:
            snake_list[index2] = tiles.get_tile_location(snake_list[index2].column + colInc,
                snake_list[index2].row + rowInc)
            tiles.place_on_tile(snake_head, snake_list[index2])
        else:
            snake_list[index2] = tiles.get_tile_location(snake_list[index2 + 1].column, snake_list[index2 + 1].row)
            tiles.set_tile_at(snake_list[index2], assets.tile("""
                myTile
            """))
        index2 += 1
def resetSnake():
    global snake_list
    tiles.set_current_tilemap(tilemap("""
        level1
    """))
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
    if tiles.tile_at_location_equals(snake_head.tilemap_location(), assets.tile("""
        Wall
    """)) or tiles.tile_at_location_equals(snake_head.tilemap_location(),
        assets.tile("""
            myTile
        """)):
        info.change_score_by(1)
        pause(200)
        resetSnake()

def on_down_pressed():
    doAction(2)
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def getStateIdx(column_offset2: number, row_offset2: number, base2: number):
    if snake_head.tilemap_location().column + column_offset2 == snake_food.tilemap_location().column and snake_head.tilemap_location().row + row_offset2 == snake_food.tilemap_location().row:
        return base2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + column_offset2,
            snake_head.tilemap_location().row + row_offset2),
        assets.tile("""
            myTile
        """)):
        return base2 * 2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + column_offset2,
            snake_head.tilemap_location().row + row_offset2),
        assets.tile("""
            Wall
        """)):
        return base2 * 2 + base2
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
current_action = 0
current_state = 0
iMaxIdx = 0
rowInc = 0
colInc = 0
index2 = 0
snake_list: List[tiles.Location] = []
discount_factor = 0
learning_rate = 0
quality_table: List[List[number]] = []
speed_ms = 0
snake_food: Sprite = None
snake_head: Sprite = None
info.set_score(0)
setGlobalVariables()
initQualityTable()
resetSnake()

def on_on_update():
    global current_state, current_action
    pause(speed_ms)
    current_state = getStateIndex()
    if randint(0, 100) < 20:
        current_action = doAction(randint(0, 3))
    else:
        current_action = callAgentForAction(current_state)
    checkCollision()
    eatFood()
    moveSnake()
    snake_head.say_text(getReward(getStateIndex(), current_action))
    update_quality_table(current_state,
        current_action,
        learning_rate,
        discount_factor)
game.on_update(on_on_update)
