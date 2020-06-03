
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
gravity = 1500
jump_speed = 600

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
            Rec(0, 300, 400, 40),
            Rec(100, 220, 200, 10),
            Rec(0, 140, 100, 10),
            Rec(300, 140, 100, 10)
        ]
    }
]
death = 2
player_acc = 1800
player_max_speed = 300
friction_de_acc = player_acc * 1.4
sleep_amount = 0.01
friction_stop_threshold = 5
on_ground_threshold = 400
rebound_amount = 0.5
attack_total_time = 0.5

hit_amount = 200
hit_multiplyer = 2
health_reduction = 0.1

final_game_time = 100
