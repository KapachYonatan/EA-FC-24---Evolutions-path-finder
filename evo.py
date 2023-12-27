from copy import deepcopy


class Evo:
    def __init__(self, name, price, req, upg):
        self.name = name
        self.price = price
        self.req = req
        self.upg = upg

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # Overload hash for "set" purpose
    def __hash__(self):
        return hash(self.name)

    # Checking equality by name only
    def __eq__(self, other):
        return isinstance(other, Evo) and self.name == other.name

    # Gets a player object and checks requirements for evolution
    def is_evo_able(self, _player):
        for done_evo in getattr(_player, "evolutions"):  # Iterate over already done evolutions of the player
            if self.name == getattr(done_evo, "name"):  # Evo has been used
                return False

        for key in self.req:
            req_val = self.req[key]

            if key == "playstyle_plus" and getattr(_player, key) != "None":  # Check playstyle plus violation
                return False

            if key == "max_playstyles" and req_val < len(getattr(_player, "playstyles")):  # Too many playstyles
                return False

            if key == "positions":  # Check if position fits
                hit = False
                for pos in req_val:
                    if pos in getattr(_player, key):  # Position fits
                        hit = True
                        break
                if not hit:
                    return False

            if key == "rarity":  # Check if desired rarity
                if req_val != getattr(_player, "rarity"):
                    return False

            if key == "no_positions":  # Position not allowed
                for no_pos in req_val:
                    if no_pos in getattr(_player, "positions"):
                        return False

            if "min" in key:  # Req is min rating
                p_val = getattr(_player, key.removeprefix("min"))  # Get the relevant player stat value
                if p_val < req_val:
                    return False

            if "max" in key and "playstyles" not in key:  # Req is max stat
                p_val = getattr(_player, key.removeprefix("max"))  # Get the relevant player stat value
                if p_val > req_val:
                    return False

        return True

    # Perform an evolution on a player object - returns a new evolved player. No requirements check
    def evolve(self, old_player):
        evo_player = deepcopy(old_player)  # No memory shared

        for key in self.upg:
            upg_val = self.upg[key]

            if key.startswith("_"):  # Stat
                evo_player.add_stat(key, upg_val)
            elif key == "positions":
                evo_player.add_positions(upg_val)
            elif key == "playstyles":
                evo_player.add_playstyles(upg_val)
            elif key == "playstyle_plus":
                evo_player.add_playstyle_plus(upg_val)
            elif key == "rarity":
                evo_player.add_rarity(upg_val)
            elif "wr" in key:  # Work rate
                evo_player.add_wr(key, upg_val)
            else:  # Only left choice - skills/wf
                evo_player.add_star(key, upg_val)

        evo_player.add_evo(self)  # Update evolutions done of the new evolved player

        return evo_player


'''
current evolutions in game
'''

peps_legacy_req = {'max_pac': 90, 'max_dri': 86, 'max_phy': 81, 'positions': {'LB'}, 'max_playstyles': 8,
                   'playstyle_plus': 'None'}
peps_legacy_upg = {'wf': 2, 'skills': 1, 'playstyles': {'TIKI TAKA', 'INCISIVE PASS'}, '_ovr': 5, '_pac': 1, '_sho': 4,
                   '_pas': 8, '_dri': 5, '_def': 2, '_phy': 2, 'rarity': 'Winter Wildcards Evo'}
peps_legacy_evo = Evo("Pep's Legacy", 75000, peps_legacy_req, peps_legacy_upg)

grow_spurt_req = {'max_ovr': 75, 'max_pac': 76, 'max_dri': 80, 'max_phy': 80, 'max_playstyles': 7,
                  'playstyle_plus': 'None'}
grow_spurt_upg = {'playstyles': {'TECHNICAL', 'INCISIVE PASS'}, '_ovr': 13, '_pac': 10, '_sho': 10, '_pas': 12,
                  '_dri': 11, '_def': 11, '_phy': 9, 'playstyle_plus': 'DEAD BALL', 'rarity': 'Winter Wildcards Evo'}
grow_spurt_evo = Evo("Growth Spurt", 0, grow_spurt_req, grow_spurt_upg)

pitch_req = {'max_ovr': 85, 'max_pac': 84, 'max_pas': 81, 'max_dri': 85, 'max_phy': 82, 'positions': {'CDM'},
             'playstyle_plus': 'None'}
pitch_upg = {'wf': 1, 'playstyle_plus': 'INTERCEPT', '_ovr': 3, '_pac': 3, '_pas': 4, '_dri': 3, '_def': 4, '_phy': 4,
             'rarity': 'Evolutions III'}
pitch_one_evo = Evo('Pitch Commander 1', 150000, pitch_req, pitch_upg)
pitch_two_evo = Evo('Pitch Commander 2', 150000, pitch_req, pitch_upg)

treq_req = {'max_pac': 90, 'max_sho': 86, 'max_pas': 78, 'max_dri': 84, 'positions': {'ST'}, 'max_playstyles': 8,
            'playstyle_plus': 'None'}
treq_upg = {'playstyles': {'PINGED PASS'}, 'playstyle_plus': 'TIKI TAKA', '_ovr': 3, '_pac': 2, '_pas': 11, '_dri': 3,
            '_phy': 3, 'rarity': 'Evolutions III'}
treq_evo = Evo('Trequartista Time', 75000, treq_req, treq_upg)

mid_dyn_req = {'max_ovr': 85, 'max_pac': 89, 'max_dri': 86, 'max_phy': 85, 'positions': {'LM'}, 'no_positions': {'CM'},
               'max_playstyles': 8}
mid_dyn_upg = {'playstyles': {'PRESS PROVEN', 'WHIPPED PASS'}, '_ovr': 3, '_pac': 3, '_sho': 4, '_pas': 4, '_dri': 3,
               '_def': 2, '_phy': 2, 'rarity': 'Evolutions II'}
mid_dyn_evo = Evo('Midfield Dynasty', 0, mid_dyn_req, mid_dyn_upg)

dri_sen_req = {'max_ovr': 84, 'max_pac': 84, 'min_sho': 71, 'max_dri': 83, 'max_phy': 84, 'max_playstyles': 9}
dri_sen_upg = {'playstyles': {'PRESS PROVEN'}, '_ovr': 2, '_pac': 2, '_sho': 2, '_pas': 2, '_dri': 4,
               '_def': 2, '_phy': 2, 'rarity': 'Evolutions II'}
dri_sen_evo = Evo('Dribbling Sensation', 0, dri_sen_req, dri_sen_upg)

budding_req = {'max_ovr': 77, 'max_pac': 91, 'max_sho': 80, 'max_dri': 83, 'max_phy': 69, 'no_positions': {'CF'},
               'max_playstyles': 8}
budding_upg = {'playstyles': {'ACROBATIC', 'QUICK STEP'}, '_ovr': 8, '_pac': 3, '_sho': 10, '_pas': 11, '_dri': 8,
               '_def': 5, '_phy': 9, 'rarity': 'Evolutions II'}
budding_one_evo = Evo('Budding Starlet 1', 0, budding_req, budding_upg)
budding_two_evo = Evo('Budding Starlet 2', 0, budding_req, budding_upg)

curr_evos = [budding_one_evo, budding_two_evo, treq_evo, pitch_one_evo, pitch_two_evo,
             dri_sen_evo, mid_dyn_evo, peps_legacy_evo, grow_spurt_evo]

'''
evolutions section end
'''



