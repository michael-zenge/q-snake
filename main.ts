controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(4)
})
function initQTable () {
    lQ = []
    for (let index = 0; index < 1024; index++) {
        lQ.push([
        1,
        0,
        0,
        0,
        0
        ])
    }
}
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(2)
})
function eatFood () {
    if (tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`myTile1`)) {
        tiles.setTileAt(snakeHead.tilemapLocation(), assets.tile`myTile0`)
        while (true) {
            tmpLocation = tiles.getTileLocation(randint(2, 11), randint(2, 9))
            if (!(tiles.tileAtLocationEquals(tmpLocation, assets.tile`myTile`))) {
                tiles.setTileAt(tmpLocation, assets.tile`myTile1`)
                break;
            }
        }
        listSnake.unshift(snakeHead.tilemapLocation())
        info.changeScoreBy(1)
    }
}
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(1)
})
function getState (colOffset: number, rowOffset: number, basis: number) {
    if (tiles.tileAtLocationEquals(tiles.getTileLocation(snakeHead.tilemapLocation().column + colOffset, snakeHead.tilemapLocation().row + rowOffset), assets.tile`myTile1`)) {
        return basis
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snakeHead.tilemapLocation().column + colOffset, snakeHead.tilemapLocation().row + rowOffset), assets.tile`myTile`)) {
        return basis * 2
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snakeHead.tilemapLocation().column + colOffset, snakeHead.tilemapLocation().row + rowOffset), assets.tile`Wall`)) {
        return basis * 2 + basis
    } else {
        return 0
    }
}
function moveSnake () {
    for (let index2 = 0; index2 <= listSnake.length - 1; index2++) {
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
    }
}
function checkCollision () {
    if (tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`Wall`) || tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`myTile`)) {
        game.over(false)
    }
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(3)
})
function getStateIdx () {
    return getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1))))
}
function doAction (Idx: number) {
    if (Idx == 4) {
        colInc = 0
        rowInc = -1
        return true
    } else if (Idx == 3) {
        colInc = 0
        rowInc = 1
        return true
    } else if (Idx == 2) {
        colInc = -1
        rowInc = 0
        return true
    } else if (Idx == 1) {
        colInc = 1
        rowInc = 0
        return true
    } else {
        return true
    }
    return false
}
function doQAction (StateIdx: number) {
    iMaxIdx = 0
    for (let index3 = 0; index3 <= 4; index3++) {
        if (lQ[StateIdx][index3] > iMaxIdx) {
            iMaxIdx = index3
        }
    }
    doAction(iMaxIdx)
}
let iMaxIdx = 0
let rowInc = 0
let colInc = 0
let tmpLocation: tiles.Location = null
let lQ: number[][] = []
let snakeHead: Sprite = null
let listSnake: tiles.Location[] = []
info.setScore(0)
initQTable()
listSnake = []
tiles.setCurrentTilemap(tilemap`level1`)
listSnake.unshift(tiles.getTileLocation(4, 4))
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
tiles.placeOnTile(snakeHead, listSnake[0])
listSnake.unshift(snakeHead.tilemapLocation())
tiles.setTileAt(tiles.getTileLocation(randint(2, 11), randint(2, 9)), assets.tile`myTile1`)
doAction(3)
game.onUpdateInterval(350, function () {
    if (randint(0, 100) < 50) {
        doAction(randint(0, 4))
    } else {
        doQAction(getStateIdx())
    }
    moveSnake()
    snakeHead.sayText(getStateIdx())
    checkCollision()
    eatFood()
})
