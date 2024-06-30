import random

class Player:
    def __init__(self, name, attack_level=99, defense_level=99):
        self.name = name
        self.hp = 99
        self.shark_count = 6
        self.karambwan_count = 2
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.strategy = None

    def reset(self):
        self.hp = 99
        self.shark_count = 6
        self.karambwan_count = 2

    def attack(self, opponent):
        max_hit = 44 + (42 * ((99 - self.hp) // 98))
        if self.hit_success(opponent):
            hit = random.randint(0, int(max_hit))
            opponent.hp -= hit

    def hit_success(self, opponent):
        attack_roll = self.attack_level * (self.attack_level + 64)
        defense_roll = opponent.defense_level * (opponent.defense_level + 64)
        hit_chance = attack_roll / (attack_roll + defense_roll)
        return random.random() < hit_chance

    def eat_shark(self):
        if self.shark_count > 0:
            self.hp += 20
            if self.hp > 99:
                self.hp = 99
            self.shark_count -= 1

    def eat_shark_and_karambwan(self):
        if self.shark_count > 0 and self.karambwan_count > 0:
            self.hp += 38
            if self.hp > 99:
                self.hp = 99
            self.shark_count -= 1
            self.karambwan_count -= 1

    def choose_action(self, opponent):
        return self.strategy(self, opponent)
    
def strategy1(player, opponent):
    if player.hp < 45 and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    else:
        player.attack(opponent)

def strategy2(player, opponent):
    player.attack(opponent)

def strategy3(player, opponent):
    if player.shark_count == 0 and player.karambwan_count == 0:
        player.attack(opponent)
    else:
        choice = random.choice(['attack', 'shark', 'shark_and_karambwan'])
        if choice == 'attack':
            player.attack(opponent)
        elif choice == 'shark' and player.shark_count > 0:
            player.eat_shark()
        elif choice == 'shark_and_karambwan' and player.shark_count > 0 and player.karambwan_count > 0:
            player.eat_shark_and_karambwan()
        else:
            player.attack(opponent)

def strategy4(player, opponent):
    if player.hp < 40 and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    elif player.hp < 60 and player.shark_count > 0:
        player.eat_shark()
    else:
        player.attack(opponent)

def strategy5(player, opponent):
    if opponent.hp < player.hp:
        player.attack(opponent)
    elif player.hp < 40 and player.shark_count > 0 and player.karambwan_count > 0:
        player.eat_shark_and_karambwan()
    else:
        player.attack(opponent)

def strategy6(player, opponent):
    opponent_max_hit = 44 + (42 * ((99 - opponent.hp) // 98))
    if opponent_max_hit < player.hp:
        player.attack(opponent)
    else:
        if player.hp + 38 <= 99 and player.shark_count > 0 and player.karambwan_count > 0:
            player.eat_shark_and_karambwan()
        elif player.shark_count > 0:
            player.eat_shark()
        else:
            player.attack(opponent)

def simulate_game(strategy1, strategy2):
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    player1.strategy = strategy1
    player2.strategy = strategy2
    
    players = [player1, player2]
    random.shuffle(players)
    
    while player1.hp > 0 and player2.hp > 0:
        current_player = players[0]
        opponent = players[1]
        current_player.choose_action(opponent)
        
        if opponent.hp <= 0:
            return current_player.name
        
        players.reverse()

def run_simulations():
    strategies = [strategy1, strategy2, strategy3, strategy4, strategy5, strategy6]
    strategy_names = ["2-tick", "yolo", "???", "Safer", "Opponent hp", "actual safer"]
    results = {name: {name: 0 for name in strategy_names} for name in strategy_names}
    
    for i, strat1 in enumerate(strategies):
        for j, strat2 in enumerate(strategies):
            if i != j:
                wins = 0
                for _ in range(10000):
                    winner = simulate_game(strat1, strat2)
                    if winner == "Player 1":
                        wins += 1
                results[strategy_names[i]][strategy_names[j]] = wins
                results[strategy_names[j]][strategy_names[i]] = 10000 - wins

    return results

results = run_simulations()
for strategy, outcomes in results.items():
    print(f"{strategy} results:")
    for opponent_strategy, wins in outcomes.items():
        print(f"  Against {opponent_strategy}: {wins} wins")
