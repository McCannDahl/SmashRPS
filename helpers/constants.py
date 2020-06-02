
from helpers.rec import Rec

colors = [
    [0,0,0],
    [255,0,0],
    [255,127,0],
    [225,225,0],
    [0,255,0],
    [0,0,255],
    [75,0,130],
    [148,0,211]
]
gravity = 1600
jump_speed = 500

maps = [
    {
        'w': 400,
        'h': 300,
        'walls': [
            Rec(0, 0, 400, 40)
        ]
    },
    {
        'w': 400,
        'h': 300,
        'walls': [
            Rec(0, 300, 400, 40)
        ]
    }
]
death = 2
player_acc = 100
player_max_speed = 100
friction = 0.2
sleep_amount = 0.01
friction_stop_threshold = 50
on_ground_threshold = 300
rebound_amount = 0.6
