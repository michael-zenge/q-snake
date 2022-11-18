def on_up_pressed():
    doAction(3)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def initQTable():
    global lQ
    lQ = []
    for index in range(1024):
        lQ.append([0, 0, 0, 0])

def on_a_pressed():
    game.over(True)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def getReward(stateIdx: number, actionIdx: number):
    if stateIdx >= 512:
        return -10
    elif stateIdx >= 256:
        return 10
    else:
        if snakeHead.tilemap_location().column > snakeFood.tilemap_location().column and snakeHead.tilemap_location().row > snakeFood.tilemap_location().row:
            if actionIdx == 3 or actionIdx == 1:
                return 1
        elif snakeHead.tilemap_location().column < snakeFood.tilemap_location().column and snakeHead.tilemap_location().row > snakeFood.tilemap_location().row:
            if actionIdx == 3 or actionIdx == 0:
                return 1
        elif snakeHead.tilemap_location().column < snakeFood.tilemap_location().column and snakeHead.tilemap_location().row < snakeFood.tilemap_location().row:
            if actionIdx == 2 or actionIdx == 0:
                return 1
        elif snakeHead.tilemap_location().column > snakeFood.tilemap_location().column and snakeHead.tilemap_location().row < snakeFood.tilemap_location().row:
            if actionIdx == 2 or actionIdx == 1:
                return 1
        return -1

def on_left_pressed():
    doAction(1)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def eatFood():
    if tiles.tile_at_location_equals(snakeHead.tilemap_location(),
        assets.tile("""
            myTile1
        """)):
        tiles.set_tile_at(snakeHead.tilemap_location(),
            assets.tile("""
                myTile0
            """))
        while True:
            tiles.place_on_tile(snakeFood,
                tiles.get_tile_location(randint(2, 11), randint(2, 9)))
            if not (tiles.tile_at_location_equals(snakeFood.tilemap_location(),
                assets.tile("""
                    myTile
                """))):
                tiles.set_tile_at(snakeFood.tilemap_location(),
                    assets.tile("""
                        myTile1
                    """))
                break
        listSnake.unshift(snakeHead.tilemap_location())
        info.change_score_by(1)

def on_right_pressed():
    doAction(0)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def getState(colOffset: number, rowOffset: number, base: number):
    if tiles.tile_at_location_equals(tiles.get_tile_location(snakeHead.tilemap_location().column + colOffset,
            snakeHead.tilemap_location().row + rowOffset),
        assets.tile("""
            myTile1
        """)):
        return base
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snakeHead.tilemap_location().column + colOffset,
            snakeHead.tilemap_location().row + rowOffset),
        assets.tile("""
            myTile
        """)):
        return base * 2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snakeHead.tilemap_location().column + colOffset,
            snakeHead.tilemap_location().row + rowOffset),
        assets.tile("""
            Wall
        """)):
        return base * 2 + base
    else:
        return 0
def moveSnake():
    global index2
    while index2 <= len(listSnake) - 1:
        if index2 == 0:
            tiles.set_tile_at(listSnake[index2], assets.tile("""
                myTile0
            """))
        if index2 == len(listSnake) - 1:
            listSnake[index2] = tiles.get_tile_location(listSnake[index2].column + colInc,
                listSnake[index2].row + rowInc)
            tiles.place_on_tile(snakeHead, listSnake[index2])
        else:
            listSnake[index2] = tiles.get_tile_location(listSnake[index2 + 1].column, listSnake[index2 + 1].row)
            tiles.set_tile_at(listSnake[index2], assets.tile("""
                myTile
            """))
        index2 += 1
def resetSnake():
    global listSnake
    tiles.set_current_tilemap(tilemap("""
        level1
    """))
    tiles.place_on_tile(snakeFood,
        tiles.get_tile_location(randint(2, 11), randint(2, 9)))
    tiles.set_tile_at(snakeFood.tilemap_location(),
        assets.tile("""
            myTile1
        """))
    listSnake = []
    listSnake.unshift(tiles.get_tile_location(4, 4))
    tiles.place_on_tile(snakeHead, listSnake[0])
    listSnake.unshift(snakeHead.tilemap_location())
    doAction(2)
def checkCollision():
    if tiles.tile_at_location_equals(snakeHead.tilemap_location(), assets.tile("""
        Wall
    """)) or tiles.tile_at_location_equals(snakeHead.tilemap_location(),
        assets.tile("""
            myTile
        """)):
        info.change_score_by(1)
        pause(500)
        resetSnake()

def on_down_pressed():
    doAction(2)
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def getStateIdx():
    return getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1))))
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
def doQAction(StateIdx: number):
    global iMaxIdx
    iMaxIdx = 0
    for index3 in range(5):
        if lQ[StateIdx][index3] > lQ[StateIdx][iMaxIdx]:
            iMaxIdx = index3
    return doAction(iMaxIdx)
def doQUpdate(stateIdx2: number, actionIdx2: number, alpha: number):
    lQ[stateIdx2][actionIdx2] = (1 - alpha) * lQ[stateIdx2][actionIdx2] + alpha * getReward(getStateIdx(), actionIdx2)
    print(lQ[stateIdx2])
currActionIdx = 0
currStateIdx = 0
iMaxIdx = 0
rowInc = 0
colInc = 0
index2 = 0
listSnake: List[tiles.Location] = []
lQ: List[List[number]] = []
snakeHead: Sprite = None
snakeFood: Sprite = None
info.set_score(0)
initQTable()
snakeFood = sprites.create(img("""
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
snakeHead = sprites.create(img("""
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
scene.camera_follow_sprite(snakeHead)
resetSnake()

def on_update_interval():
    global currStateIdx, currActionIdx
    currStateIdx = getStateIdx()
    if randint(0, 100) < 20:
        currActionIdx = doAction(randint(0, 3))
    else:
        currActionIdx = doQAction(currStateIdx)
    checkCollision()
    eatFood()
    moveSnake()
    snakeHead.say_text(getReward(getStateIdx(), currActionIdx))
    doQUpdate(currStateIdx, currActionIdx, 0.2)
game.on_update_interval(350, on_update_interval)
