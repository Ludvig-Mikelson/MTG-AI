import Engine as en
import Classes as cs


player1 = en.player1
player2 = en.player2

state = cs.GameState(player_AP=player1,player_NAP=player2,stack=[])

for _ in range(1,100):
    en.main_action(state)