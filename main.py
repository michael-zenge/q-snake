def on_up_pressed():
    apply_action(3)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def on_b_pressed():
    global speed_ms
    if speed_ms < 1000:
        speed_ms = speed_ms + 50
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def get_reward(stateIdx: number, actionIdx: number):
    if stateIdx >= 3072:
        if stateIdx - 3072 >= 512:
            return -10
        elif stateIdx - 3072 >= 256:
            return 10
        elif actionIdx == 2 or actionIdx == 1:
            return 1
        else:
            return -1
    elif stateIdx >= 2048:
        if stateIdx - 2048 >= 512:
            return -10
        elif stateIdx - 2048 >= 256:
            return 10
        elif actionIdx == 2 or actionIdx == 0:
            return 1
        else:
            return -1
    elif stateIdx >= 1024:
        if stateIdx - 1024 >= 512:
            return -10
        elif stateIdx - 1024 >= 256:
            return 10
        elif actionIdx == 3 or actionIdx == 0:
            return 1
        else:
            return -1
    elif stateIdx - 0 >= 512:
        return -10
    elif stateIdx - 0 >= 256:
        return 10
    elif actionIdx == 3 or actionIdx == 1:
        return 1
    else:
        return -1
def do_Q_update(stateIdx22: number, actionIdx2: number, alpha: number, gamma: number):
    Q_table[stateIdx22][actionIdx2] = (1 - alpha) * Q_table[stateIdx22][actionIdx2] + (alpha * get_reward(get_state_idx(), actionIdx2) + alpha * gamma * getMaxReward(actionIdx2))
    print(Q_table[stateIdx22])

def on_a_pressed():
    global speed_ms
    if speed_ms > 50:
        speed_ms = speed_ms - 50
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def move_snake():
    global index2
    index2 = 0
    while index2 <= len(listSnake) - 1:
        if index2 == 0:
            tiles.set_tile_at(listSnake[index2], assets.tile("""
                myTile0
            """))
        if index2 == len(listSnake) - 1:
            listSnake[index2] = tiles.get_tile_location(listSnake[index2].column + colInc,
                listSnake[index2].row + rowInc)
            tiles.place_on_tile(snake_head, listSnake[index2])
        else:
            listSnake[index2] = tiles.get_tile_location(listSnake[index2 + 1].column, listSnake[index2 + 1].row)
            tiles.set_tile_at(listSnake[index2], assets.tile("""
                myTile
            """))
        index2 += 1
def reset_snake():
    global listSnake
    tiles.set_current_tilemap(tilemap("""
        level1
    """))
    tiles.place_on_tile(snake_food,
        tiles.get_tile_location(randint(2, 11), randint(2, 9)))
    tiles.set_tile_at(snake_food.tilemap_location(),
        assets.tile("""
            myTile1
        """))
    listSnake = []
    listSnake.unshift(tiles.get_tile_location(4, 4))
    tiles.place_on_tile(snake_head, listSnake[0])
    listSnake.unshift(snake_head.tilemap_location())
    apply_action(2)

def on_left_pressed():
    apply_action(1)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def apply_Q_action(StateIdx: number):
    global iMaxIdx
    iMaxIdx = 0
    for index3 in range(5):
        if Q_table[StateIdx][index3] > Q_table[StateIdx][iMaxIdx]:
            iMaxIdx = index3
    return apply_action(iMaxIdx)

def on_right_pressed():
    apply_action(0)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def getState(colOffset: number, rowOffset: number, base: number):
    if tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + colOffset,
            snake_head.tilemap_location().row + rowOffset),
        assets.tile("""
            myTile1
        """)):
        return base
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + colOffset,
            snake_head.tilemap_location().row + rowOffset),
        assets.tile("""
            myTile
        """)):
        return base * 2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snake_head.tilemap_location().column + colOffset,
            snake_head.tilemap_location().row + rowOffset),
        assets.tile("""
            Wall
        """)):
        return base * 2 + base
    else:
        return 0
def initialize_Q_table():
    global Q_table
    Q_table = []
    for index in range(4096):
        Q_table.append([0, 0, 0, 0])

def on_down_pressed():
    apply_action(2)
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def getMaxReward(stateIdx2: number):
    return max(max(Q_table[stateIdx2][0], Q_table[0][stateIdx2]),
        max(Q_table[0][2], Q_table[stateIdx2][3]))
def get_state_idx():
    if snake_head.tilemap_location().column >= snake_food.tilemap_location().column and snake_head.tilemap_location().row >= snake_food.tilemap_location().row:
        return 0 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    elif snake_head.tilemap_location().column < snake_food.tilemap_location().column and snake_head.tilemap_location().row >= snake_food.tilemap_location().row:
        return 1024 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    elif snake_head.tilemap_location().column < snake_food.tilemap_location().column and snake_head.tilemap_location().row < snake_food.tilemap_location().row:
        return 2048 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    elif snake_head.tilemap_location().column >= snake_food.tilemap_location().column and snake_head.tilemap_location().row < snake_food.tilemap_location().row:
        return 3072 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    return 0
def set_global_variables():
    global speed_ms, learning_rate, discount_factor, snake_food, snake_head
    speed_ms = 350
    learning_rate = 0.2
    discount_factor = 0.5
    snake_food = sprites.create(img("""
            . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . f . f . . . . . . . 
                    . . . . . . . f . . . . . . . . 
                    . . . . . . f . f . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . .
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
def apply_action(Idx: number):
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
def eat_food():
    if tiles.tile_at_location_equals(snake_head.tilemap_location(),
        assets.tile("""
            myTile1
        """)):
        while True:
            tiles.place_on_tile(snake_food,
                tiles.get_tile_location(randint(2, 11), randint(2, 9)))
            if not (tiles.tile_at_location_equals(snake_food.tilemap_location(),
                assets.tile("""
                    myTile1
                """))) and not (tiles.tile_at_location_equals(snake_food.tilemap_location(),
                assets.tile("""
                    myTile
                """))):
                tiles.set_tile_at(snake_food.tilemap_location(),
                    assets.tile("""
                        myTile1
                    """))
                break
        tiles.set_tile_at(snake_head.tilemap_location(),
            assets.tile("""
                myTile0
            """))
        listSnake.unshift(snake_head.tilemap_location())
        info.change_score_by(1)
def check_collision():
    if tiles.tile_at_location_equals(snake_head.tilemap_location(), assets.tile("""
        Wall
    """)) or tiles.tile_at_location_equals(snake_head.tilemap_location(),
        assets.tile("""
            myTile
        """)):
        info.change_score_by(1)
        pause(200)
        reset_snake()
current_action = 0
current_state = 0
discount_factor = 0
learning_rate = 0
iMaxIdx = 0
snake_food: Sprite = None
snake_head: Sprite = None
rowInc = 0
colInc = 0
listSnake: List[tiles.Location] = []
index2 = 0
Q_table: List[List[number]] = []
speed_ms = 0
info.set_score(0)
set_global_variables()
initialize_Q_table()
reset_snake()

def on_on_update():
    global current_state, current_action
    pause(speed_ms)
    current_state = get_state_idx()
    if randint(0, 100) < 20:
        current_action = apply_action(randint(0, 3))
    else:
        current_action = apply_Q_action(current_state)
    check_collision()
    eat_food()
    move_snake()
    snake_head.say_text(get_reward(get_state_idx(), current_action))
    do_Q_update(current_state,
        current_action,
        learning_rate,
        discount_factor)
game.on_update(on_on_update)
