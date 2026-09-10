import itertools

class ShapleyValueEngine:
    """
    Shapley Value Cooperative Game Engine.
    Computes unique payoff vector satisfying Efficiency, Symmetry, Dummy Player, and Additivity.
    """
    def __init__(self, players):
        self.players = list(players)

    def compute(self, characteristic_fn):
        n = len(self.players)
        shapley = {p: 0.0 for p in self.players}
        perms = list(itertools.permutations(self.players))

        for p in perms:
            coalition = set()
            for player in p:
                v_before = characteristic_fn(coalition)
                coalition.add(player)
                v_after = characteristic_fn(coalition)
                shapley[player] += (v_after - v_before)

        for player in self.players:
            shapley[player] /= len(perms)
        return shapley
