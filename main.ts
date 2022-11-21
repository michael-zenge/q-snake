controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(3)
})
function initQTable () {
    lQ = []
    for (let index = 0; index < 4096; index++) {
        lQ.push([
        0,
        0,
        0,
        0
        ])
    }
}
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    game.over(true)
})
function getReward (stateIdx: number, actionIdx: number) {
    if (stateIdx >= 3072) {
        if (stateIdx - 3072 >= 512) {
            return -10
        } else if (stateIdx - 3072 >= 256) {
            return 10
        } else if (actionIdx == 2 || actionIdx == 1) {
            return 1
        } else {
            return -1
        }
    } else if (stateIdx >= 2048) {
        if (stateIdx - 2048 >= 512) {
            return -10
        } else if (stateIdx - 2048 >= 256) {
            return 10
        } else if (actionIdx == 2 || actionIdx == 0) {
            return 1
        } else {
            return -1
        }
    } else if (stateIdx >= 1024) {
        if (stateIdx - 1024 >= 512) {
            return -10
        } else if (stateIdx - 1024 >= 256) {
            return 10
        } else if (actionIdx == 3 || actionIdx == 0) {
            return 1
        } else {
            return -1
        }
    } else if (stateIdx - 0 >= 512) {
        return -10
    } else if (stateIdx - 0 >= 256) {
        return 10
    } else if (actionIdx == 3 || actionIdx == 1) {
        return 1
    } else {
        return -1
    }
}
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(1)
})
function eatFood () {
    if (tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`myTile1`)) {
        tiles.setTileAt(snakeHead.tilemapLocation(), assets.tile`myTile0`)
        while (true) {
            tiles.placeOnTile(snakeFood, tiles.getTileLocation(randint(2, 11), randint(2, 9)))
            if (!(tiles.tileAtLocationEquals(snakeFood.tilemapLocation(), assets.tile`myTile`))) {
                tiles.setTileAt(snakeFood.tilemapLocation(), assets.tile`myTile1`)
                break;
            }
        }
        listSnake.unshift(snakeHead.tilemapLocation())
        info.changeScoreBy(1)
    }
}
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(0)
})
function getState (colOffset: number, rowOffset: number, base: number) {
    if (tiles.tileAtLocationEquals(tiles.getTileLocation(snakeHead.tilemapLocation().column + colOffset, snakeHead.tilemapLocation().row + rowOffset), assets.tile`myTile1`)) {
        return base
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snakeHead.tilemapLocation().column + colOffset, snakeHead.tilemapLocation().row + rowOffset), assets.tile`myTile`)) {
        return base * 2
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snakeHead.tilemapLocation().column + colOffset, snakeHead.tilemapLocation().row + rowOffset), assets.tile`Wall`)) {
        return base * 2 + base
    } else {
        return 0
    }
}
function moveSnake () {
    index2 = 0
    while (index2 <= listSnake.length - 1) {
        if (index2 == 0) {
            tiles.setTileAt(listSnake[index2], assets.tile`myTile0`)
        }
        if (index2 == listSnake.length - 1) {
            listSnake[index2] = tiles.getTileLocation(listSnake[index2].column + colInc, listSnake[index2].row + rowInc)
            tiles.placeOnTile(snakeHead, listSnake[index2])
        } else {
            listSnake[index2] = tiles.getTileLocation(listSnake[index2 + 1].column, listSnake[index2 + 1].row)
            tiles.setTileAt(listSnake[index2], assets.tile`myTile`)
        }
        index2 += 1
    }
}
function resetSnake () {
    tiles.setCurrentTilemap(tilemap`level1`)
    tiles.placeOnTile(snakeFood, tiles.getTileLocation(randint(2, 11), randint(2, 9)))
    tiles.setTileAt(snakeFood.tilemapLocation(), assets.tile`myTile1`)
    listSnake = []
    listSnake.unshift(tiles.getTileLocation(4, 4))
    tiles.placeOnTile(snakeHead, listSnake[0])
    listSnake.unshift(snakeHead.tilemapLocation())
    doAction(2)
}
function checkCollision () {
    if (tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`Wall`) || tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`myTile`)) {
        info.changeScoreBy(1)
        pause(100)
        resetSnake()
    }
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(2)
})
function getStateIdx () {
    if (snakeHead.tilemapLocation().column >= snakeFood.tilemapLocation().column && snakeHead.tilemapLocation().row >= snakeFood.tilemapLocation().row) {
        return 0 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    } else if (snakeHead.tilemapLocation().column < snakeFood.tilemapLocation().column && snakeHead.tilemapLocation().row >= snakeFood.tilemapLocation().row) {
        return 1024 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    } else if (snakeHead.tilemapLocation().column < snakeFood.tilemapLocation().column && snakeHead.tilemapLocation().row < snakeFood.tilemapLocation().row) {
        return 2048 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    } else if (snakeHead.tilemapLocation().column >= snakeFood.tilemapLocation().column && snakeHead.tilemapLocation().row < snakeFood.tilemapLocation().row) {
        return 3072 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    }
    return 0
}
function doAction (Idx: number) {
    if (Idx == 3) {
        colInc = 0
        rowInc = -1
        return Idx
    } else if (Idx == 2) {
        colInc = 0
        rowInc = 1
        return Idx
    } else if (Idx == 1) {
        colInc = -1
        rowInc = 0
        return Idx
    } else if (Idx == 0) {
        colInc = 1
        rowInc = 0
        return Idx
    } else {
        return -1
    }
}
function doQAction (StateIdx: number) {
    iMaxIdx = 0
    for (let index3 = 0; index3 <= 4; index3++) {
        if (lQ[StateIdx][index3] > lQ[StateIdx][iMaxIdx]) {
            iMaxIdx = index3
        }
    }
    return doAction(iMaxIdx)
}
function doQUpdate (stateIdx2: number, actionIdx2: number, alpha: number) {
    lQ[stateIdx2][actionIdx2] = (1 - alpha) * lQ[stateIdx2][actionIdx2] + alpha * getReward(getStateIdx(), actionIdx2)
    console.log(lQ[stateIdx2])
}
let currActionIdx = 0
let currStateIdx = 0
let iMaxIdx = 0
let rowInc = 0
let colInc = 0
let index2 = 0
let listSnake: tiles.Location[] = []
let lQ: number[][] = []
let snakeHead: Sprite = null
let snakeFood: Sprite = null
info.setScore(0)
initQTable()
snakeFood = sprites.create(img`
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
    `, SpriteKind.Food)
snakeHead = sprites.create(img`
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
    `, SpriteKind.Player)
scene.cameraFollowSprite(snakeHead)
resetSnake()
game.onUpdateInterval(350, function () {
    currStateIdx = getStateIdx()
    if (randint(0, 100) < 20) {
        currActionIdx = doAction(randint(0, 3))
    } else {
        currActionIdx = doQAction(currStateIdx)
    }
    checkCollision()
    eatFood()
    moveSnake()
    snakeHead.sayText(getReward(getStateIdx(), currActionIdx))
    doQUpdate(currStateIdx, currActionIdx, 0.2)
})
