controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(4)
})
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
    for (let index = 0; index <= listSnake.length - 1; index++) {
        if (index == 0) {
            tiles.setTileAt(listSnake[index], assets.tile`myTile0`)
        }
        if (index == listSnake.length - 1) {
            listSnake[index] = tiles.getTileLocation(listSnake[index].column + colInc, listSnake[index].row + rowInc)
            tiles.placeOnTile(snakeHead, listSnake[index])
        } else {
            listSnake[index] = tiles.getTileLocation(listSnake[index + 1].column, listSnake[index + 1].row)
            tiles.setTileAt(listSnake[index], assets.tile`myTile`)
        }
    }
}
function checkCollision () {
    if (tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`Wall`) || tiles.tileAtLocationEquals(snakeHead.tilemapLocation(), assets.tile`myTile`)) {
        game.over(false)
    }
}
function doQLearningStep () {
    if (randint(0, 100) < 50) {
        doAction(randint(0, 4))
    } else {
    	
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
let tmpLocation: tiles.Location = null
let colInc = 0
let rowInc = 0
let snakeHead: Sprite = null
let listSnake: tiles.Location[] = []
info.setScore(0)
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
rowInc = 1
colInc = 0
game.onUpdateInterval(350, function () {
    checkCollision()
    eatFood()
    moveSnake()
    snakeHead.sayText(getStateIdx())
    doQLearningStep()
})
