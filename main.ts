controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(3)
})
controller.B.onEvent(ControllerButtonEvent.Pressed, function () {
    if (speed_ms < 1000) {
        speed_ms = speed_ms + 50
    }
})
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (speed_ms > 50) {
        speed_ms = speed_ms - 50
    }
})
function getReward (state_index: number, action_index: number) {
    if (state_index >= 3072) {
        return getRewardWithLocationOffset(state_index, action_index, 3072, 2, 1)
    } else if (state_index >= 2048) {
        return getRewardWithLocationOffset(state_index, action_index, 2048, 2, 0)
    } else if (state_index >= 1024) {
        return getRewardWithLocationOffset(state_index, action_index, 1024, 3, 0)
    } else {
        return getRewardWithLocationOffset(state_index, action_index, 0, 3, 1)
    }
}
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(1)
})
function eatFood () {
    if (snake_head.overlapsWith(snake_food)) {
        while (snake_head.overlapsWith(snake_food) || tiles.tileAtLocationEquals(snake_food.tilemapLocation(), body_tile)) {
            tiles.placeOnTile(snake_food, tiles.getTileLocation(randint(2, 11), randint(2, 9)))
        }
        snake_list.unshift(snake_head.tilemapLocation())
        info.changeScoreBy(1)
    }
}
function updateQualityTable (state_index2: number, action_index2: number, alpha: number, gamma: number) {
    quality_table[state_index2][action_index2] = (1 - alpha) * quality_table[state_index2][action_index2] + (alpha * getReward(getStateIndex(), action_index2) + alpha * gamma * getMaxReward(action_index2))
    console.log(quality_table[state_index2])
}
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(0)
})
function getStateIndex () {
    if (snake_head.tilemapLocation().column >= snake_food.tilemapLocation().column && snake_head.tilemapLocation().row >= snake_food.tilemapLocation().row) {
        return 0 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    } else if (snake_head.tilemapLocation().column < snake_food.tilemapLocation().column && snake_head.tilemapLocation().row >= snake_food.tilemapLocation().row) {
        return 1024 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    } else if (snake_head.tilemapLocation().column < snake_food.tilemapLocation().column && snake_head.tilemapLocation().row < snake_food.tilemapLocation().row) {
        return 2048 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    } else if (snake_head.tilemapLocation().column >= snake_food.tilemapLocation().column && snake_head.tilemapLocation().row < snake_food.tilemapLocation().row) {
        return 3072 + (getStateIdx(0, 0, 256) + (getStateIdx(-1, 0, 64) + (getStateIdx(0, 1, 16) + (getStateIdx(1, 0, 4) + getStateIdx(0, -1, 1)))))
    }
    return 0
}
function initGame (food_img: Image, head_img: Image, body_img: Image, bgrd_img: Image, wall_img: Image) {
    speed_ms = 350
    snake_food = sprites.create(food_img, SpriteKind.Food)
    snake_head = sprites.create(head_img, SpriteKind.Player)
    scene.cameraFollowSprite(snake_head)
    body_tile = body_img
    bgrd_tile = bgrd_img
    wall_tile = wall_img
}
function moveSnake () {
    index2 = 0
    while (index2 <= snake_list.length - 1) {
        if (index2 == 0) {
            tiles.setTileAt(snake_list[index2], bgrd_tile)
        }
        if (index2 == snake_list.length - 1) {
            snake_list[index2] = tiles.getTileLocation(snake_list[index2].column + colInc, snake_list[index2].row + rowInc)
            tiles.placeOnTile(snake_head, snake_list[index2])
        } else {
            snake_list[index2] = tiles.getTileLocation(snake_list[index2 + 1].column, snake_list[index2 + 1].row)
            tiles.setTileAt(snake_list[index2], body_tile)
        }
        index2 += 1
    }
}
function resetSnakeGame () {
    tiles.setCurrentTilemap(tilemap`level1`)
    for (let value of tiles.getTilesByType(assets.tile`Wall`)) {
        tiles.setTileAt(value, wall_tile)
    }
    for (let value of tiles.getTilesByType(assets.tile`myTile0`)) {
        tiles.setTileAt(value, bgrd_tile)
    }
    tiles.placeOnTile(snake_food, tiles.getTileLocation(randint(2, 11), randint(2, 9)))
    snake_list = []
    snake_list.unshift(tiles.getTileLocation(4, 4))
    tiles.placeOnTile(snake_head, snake_list[0])
    snake_list.unshift(snake_head.tilemapLocation())
    doAction(2)
}
function getRewardWithLocationOffset (state_index3: number, action_index3: number, index_offset: number, ref_action_1: number, ref_action_2: number) {
    if (state_index3 - index_offset >= 512) {
        return -10
    } else if (state_index3 - index_offset >= 256) {
        return 10
    } else if (action_index3 == ref_action_1 || action_index3 == ref_action_2) {
        return 1
    } else {
        return -1
    }
}
function checkCollision () {
    if (tiles.tileAtLocationEquals(snake_head.tilemapLocation(), wall_tile) || tiles.tileAtLocationEquals(snake_head.tilemapLocation(), body_tile)) {
        info.changeScoreBy(1)
        pause(200)
        resetSnakeGame()
    }
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    doAction(2)
})
function getStateIdx (column_offset: number, row_offset: number, base: number) {
    if (snake_head.tilemapLocation().column + column_offset == snake_food.tilemapLocation().column && snake_head.tilemapLocation().row + row_offset == snake_food.tilemapLocation().row) {
        return base
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snake_head.tilemapLocation().column + column_offset, snake_head.tilemapLocation().row + row_offset), body_tile)) {
        return base * 2
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snake_head.tilemapLocation().column + column_offset, snake_head.tilemapLocation().row + row_offset), wall_tile)) {
        return base * 2 + base
    } else {
        return 0
    }
}
function getMaxReward (stateIdx2: number) {
    return Math.max(Math.max(quality_table[stateIdx2][0], quality_table[0][stateIdx2]), Math.max(quality_table[0][2], quality_table[stateIdx2][3]))
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
function callAgentForAction (state_index4: number) {
    iMaxIdx = 0
    for (let index3 = 0; index3 <= 4; index3++) {
        if (quality_table[state_index4][index3] > quality_table[state_index4][iMaxIdx]) {
            iMaxIdx = index3
        }
    }
    return doAction(iMaxIdx)
}
function initQLearingEnv (alpha: number, gamma: number) {
    learning_rate = alpha
    discount_factor = gamma
    quality_table = []
    for (let index = 0; index < 4096; index++) {
        quality_table.push([
        0,
        0,
        0,
        0
        ])
    }
}
let current_action = 0
let current_state = 0
let discount_factor = 0
let learning_rate = 0
let iMaxIdx = 0
let rowInc = 0
let colInc = 0
let index2 = 0
let wall_tile: Image = null
let bgrd_tile: Image = null
let quality_table: number[][] = []
let snake_list: tiles.Location[] = []
let body_tile: Image = null
let snake_food: Sprite = null
let snake_head: Sprite = null
let speed_ms = 0
info.setScore(-500)
initQLearingEnv(0.2, 0.5)
initGame(img`
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
    `, img`
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
    `, myTiles.tile3, sprites.castle.tilePath5, sprites.dungeon.floorDark0)
resetSnakeGame()
game.onUpdate(function () {
    pause(speed_ms)
    checkCollision()
    eatFood()
    current_state = getStateIndex()
    if (info.score() < 0 && randint(0, 100) < 20) {
        current_action = doAction(randint(0, 3))
    } else {
        current_action = callAgentForAction(current_state)
    }
    moveSnake()
    snake_head.sayText(getReward(getStateIndex(), current_action))
    updateQualityTable(current_state, current_action, learning_rate, discount_factor)
})
