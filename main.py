def on_up_pressed():
    doAction(4)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def initQTable():
    global lQ
    lQ = []
    for index in range(1024):
        lQ.append([1, 0, 0, 0, 0])

def on_left_pressed():
    doAction(2)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def eatFood():
    global tmpLocation
    if tiles.tile_at_location_equals(snakeHead.tilemap_location(),
        assets.tile("""
            myTile1
        """)):
        tiles.set_tile_at(snakeHead.tilemap_location(),
            assets.tile("""
                myTile0
            """))
        while True:
            tmpLocation = tiles.get_tile_location(randint(2, 11), randint(2, 9))
            if not (tiles.tile_at_location_equals(tmpLocation, assets.tile("""
                myTile
            """))):
                tiles.set_tile_at(tmpLocation, assets.tile("""
                    myTile1
                """))
                break
        listSnake.unshift(snakeHead.tilemap_location())
        info.change_score_by(1)

def on_right_pressed():
    doAction(1)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def getState(colOffset: number, rowOffset: number, basis: number):
    if tiles.tile_at_location_equals(tiles.get_tile_location(snakeHead.tilemap_location().column + colOffset,
            snakeHead.tilemap_location().row + rowOffset),
        assets.tile("""
            myTile1
        """)):
        return basis
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snakeHead.tilemap_location().column + colOffset,
            snakeHead.tilemap_location().row + rowOffset),
        assets.tile("""
            myTile
        """)):
        return basis * 2
    elif tiles.tile_at_location_equals(tiles.get_tile_location(snakeHead.tilemap_location().column + colOffset,
            snakeHead.tilemap_location().row + rowOffset),
        assets.tile("""
            Wall
        """)):
        return basis * 2 + basis
    else:
        return 0
def moveSnake():
    index2 = 0
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
def checkCollision():
    if tiles.tile_at_location_equals(snakeHead.tilemap_location(), assets.tile("""
        Wall
    """)) or tiles.tile_at_location_equals(snakeHead.tilemap_location(),
        assets.tile("""
            myTile
        """)):
        game.over(False)

def on_down_pressed():
    doAction(3)
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def getStateIdx():
    return getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1))))
def doAction(Idx: number):
    global colInc, rowInc
    if Idx == 4:
        colInc = 0
        rowInc = -1
        return True
    elif Idx == 3:
        colInc = 0
        rowInc = 1
        return True
    elif Idx == 2:
        colInc = -1
        rowInc = 0
        return True
    elif Idx == 1:
        colInc = 1
        rowInc = 0
        return True
    else:
        return True
    return False
def doQAction(StateIdx: number):
    global iMaxIdx
    iMaxIdx = 0
    for index3 in range(5):
        if lQ[StateIdx][index3] > iMaxIdx:
            iMaxIdx = index3
    doAction(iMaxIdx)
iMaxIdx = 0
rowInc = 0
colInc = 0
tmpLocation: tiles.Location = None
lQ: List[List[number]] = []
snakeHead: Sprite = None
listSnake: List[tiles.Location] = []
info.set_score(0)
initQTable()
listSnake = []
tiles.set_current_tilemap(tilemap("""
    level1
"""))
listSnake.unshift(tiles.get_tile_location(4, 4))
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
tiles.place_on_tile(snakeHead, listSnake[0])
listSnake.unshift(snakeHead.tilemap_location())
tiles.set_tile_at(tiles.get_tile_location(randint(2, 11), randint(2, 9)),
    assets.tile("""
        myTile1
    """))
doAction(3)

def on_update_interval():
    if False and randint(0, 100) < 50:
        doAction(randint(0, 4))
    else:
        doQAction(getStateIdx())
    moveSnake()
    snakeHead.say_text(getStateIdx())
    checkCollision()
    eatFood()
game.on_update_interval(350, on_update_interval)
