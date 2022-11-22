controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    apply_action(3)
})
controller.B.onEvent(ControllerButtonEvent.Pressed, function () {
    if (speed_ms < 1000) {
        speed_ms = speed_ms + 50
    }
})
function get_reward (stateIdx: number, actionIdx: number) {
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
function do_Q_update (stateIdx22: number, actionIdx2: number, alpha: number, gamma: number) {
    Q_table[stateIdx22][actionIdx2] = (1 - alpha) * Q_table[stateIdx22][actionIdx2] + (alpha * get_reward(get_state_idx(), actionIdx2) + alpha * gamma * getMaxReward(actionIdx2))
    console.log(Q_table[stateIdx22])
}
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (speed_ms > 50) {
        speed_ms = speed_ms - 50
    }
})
function move_snake () {
    index2 = 0
    while (index2 <= listSnake.length - 1) {
        if (index2 == 0) {
            tiles.setTileAt(listSnake[index2], assets.tile`myTile0`)
        }
        if (index2 == listSnake.length - 1) {
            listSnake[index2] = tiles.getTileLocation(listSnake[index2].column + colInc, listSnake[index2].row + rowInc)
            tiles.placeOnTile(snake_head, listSnake[index2])
        } else {
            listSnake[index2] = tiles.getTileLocation(listSnake[index2 + 1].column, listSnake[index2 + 1].row)
            tiles.setTileAt(listSnake[index2], assets.tile`myTile`)
        }
        index2 += 1
    }
}
function reset_snake () {
    tiles.setCurrentTilemap(tilemap`level1`)
    tiles.placeOnTile(snake_food, tiles.getTileLocation(randint(2, 11), randint(2, 9)))
    tiles.setTileAt(snake_food.tilemapLocation(), assets.tile`myTile1`)
    listSnake = []
    listSnake.unshift(tiles.getTileLocation(4, 4))
    tiles.placeOnTile(snake_head, listSnake[0])
    listSnake.unshift(snake_head.tilemapLocation())
    apply_action(2)
}
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    apply_action(1)
})
function apply_Q_action (StateIdx: number) {
    iMaxIdx = 0
    for (let index3 = 0; index3 <= 4; index3++) {
        if (Q_table[StateIdx][index3] > Q_table[StateIdx][iMaxIdx]) {
            iMaxIdx = index3
        }
    }
    return apply_action(iMaxIdx)
}
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    apply_action(0)
})
function getState (colOffset: number, rowOffset: number, base: number) {
    if (tiles.tileAtLocationEquals(tiles.getTileLocation(snake_head.tilemapLocation().column + colOffset, snake_head.tilemapLocation().row + rowOffset), assets.tile`myTile1`)) {
        return base
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snake_head.tilemapLocation().column + colOffset, snake_head.tilemapLocation().row + rowOffset), assets.tile`myTile`)) {
        return base * 2
    } else if (tiles.tileAtLocationEquals(tiles.getTileLocation(snake_head.tilemapLocation().column + colOffset, snake_head.tilemapLocation().row + rowOffset), assets.tile`Wall`)) {
        return base * 2 + base
    } else {
        return 0
    }
}
function initialize_Q_table () {
    Q_table = []
    for (let index = 0; index < 4096; index++) {
        Q_table.push([
        0,
        0,
        0,
        0
        ])
    }
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    apply_action(2)
})
function getMaxReward (stateIdx2: number) {
    return Math.max(Math.max(Q_table[stateIdx2][0], Q_table[0][stateIdx2]), Math.max(Q_table[0][2], Q_table[stateIdx2][3]))
}
function get_state_idx () {
    if (snake_head.tilemapLocation().column >= snake_food.tilemapLocation().column && snake_head.tilemapLocation().row >= snake_food.tilemapLocation().row) {
        return 0 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    } else if (snake_head.tilemapLocation().column < snake_food.tilemapLocation().column && snake_head.tilemapLocation().row >= snake_food.tilemapLocation().row) {
        return 1024 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    } else if (snake_head.tilemapLocation().column < snake_food.tilemapLocation().column && snake_head.tilemapLocation().row < snake_food.tilemapLocation().row) {
        return 2048 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    } else if (snake_head.tilemapLocation().column >= snake_food.tilemapLocation().column && snake_head.tilemapLocation().row < snake_food.tilemapLocation().row) {
        return 3072 + (getState(0, 0, 256) + (getState(-1, 0, 64) + (getState(0, 1, 16) + (getState(1, 0, 4) + getState(0, -1, 1)))))
    }
    return 0
}
function set_global_variables () {
    action_list = [
    "right",
    "left",
    "down",
    "up"
    ]
    speed_ms = 350
    learning_rate = 0.2
    discount_factor = 0.5
}
function apply_action (Idx: number) {
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
function eat_food () {
    if (tiles.tileAtLocationEquals(snake_head.tilemapLocation(), assets.tile`myTile1`)) {
        while (true) {
            tiles.placeOnTile(snake_food, tiles.getTileLocation(randint(2, 11), randint(2, 9)))
            if (!(tiles.tileAtLocationEquals(snake_food.tilemapLocation(), assets.tile`myTile1`)) && !(tiles.tileAtLocationEquals(snake_food.tilemapLocation(), assets.tile`myTile`))) {
                tiles.setTileAt(snake_food.tilemapLocation(), assets.tile`myTile1`)
                break;
            }
        }
        tiles.setTileAt(snake_head.tilemapLocation(), assets.tile`myTile0`)
        listSnake.unshift(snake_head.tilemapLocation())
        info.changeScoreBy(1)
    }
}
function check_collision () {
    if (tiles.tileAtLocationEquals(snake_head.tilemapLocation(), assets.tile`Wall`) || tiles.tileAtLocationEquals(snake_head.tilemapLocation(), assets.tile`myTile`)) {
        info.changeScoreBy(1)
        pause(200)
        reset_snake()
    }
}
let current_action = 0
let current_state = 0
let discount_factor = 0
let learning_rate = 0
let action_list: string[] = []
let iMaxIdx = 0
let rowInc = 0
let colInc = 0
let listSnake: tiles.Location[] = []
let index2 = 0
let Q_table: number[][] = []
let speed_ms = 0
let snake_head: Sprite = null
let snake_food: Sprite = null
info.setScore(0)
set_global_variables()
initialize_Q_table()
snake_food = sprites.create(img`
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
snake_head = sprites.create(img`
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
scene.cameraFollowSprite(snake_head)
reset_snake()
game.onUpdate(function () {
    pause(speed_ms)
    current_state = get_state_idx()
    if (randint(0, 100) < 20) {
        current_action = apply_action(randint(0, 3))
    } else {
        current_action = apply_Q_action(current_state)
    }
    check_collision()
    eat_food()
    move_snake()
    snake_head.sayText(get_reward(get_state_idx(), current_action))
    do_Q_update(current_state, current_action, learning_rate, discount_factor)
})
