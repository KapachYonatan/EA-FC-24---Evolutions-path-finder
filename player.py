from utils import are_evo_lists_equal

MAX_STAT = 99
MAX_STARS = 5


class Player:
    def __init__(self, name: str, _pac: int, _sho: int, _pas: int, _dri: int, _def: int, _phy: int, _ovr: int,
                 skills: int, wf: int, positions: set, playstyle_plus: str, playstyles: set, att_wr: str, def_wr: str,
                 rarity: str, evolutions: list):
        self.name = name
        self._pac = _pac
        self._sho = _sho
        self._pas = _pas
        self._dri = _dri
        self._def = _def
        self._phy = _phy
        self._ovr = _ovr
        self.skills = skills
        self.wf = wf
        self.positions = positions
        self.playstyle_plus = playstyle_plus
        self.playstyles = playstyles
        self.att_wr = att_wr
        self.def_wr = def_wr
        self.rarity = rarity
        self.evolutions = evolutions

    def __str__(self):
        return (f"Player: {self.name}  OVR: {self._ovr}\n"
                f"Pac: {self._pac}  Dri: {self._dri}\n"
                f"Sho: {self._sho}  Def: {self._def}\n"
                f"Pas: {self._pas}  Phy: {self._phy}\n"
                f"Skills: {self.skills} Weak foot: {self.wf}\n"
                f"Playstyle+ : {self.playstyle_plus}\n"
                f"Playstyles: {self.playstyles}\n"
                f"Positions: {self.positions}\n"
                f"Attacking/Defensive Work rate: {self.att_wr}/{self.def_wr}\n"
                f"Rarity: {self.rarity}\n"
                f"Evolutions: {self.evolutions}\n")

    # Overload hash for "set" purpose
    def __hash__(self):
        return hash(self.name)

    # Overload equals for "set" purpose
    def __eq__(self, other):
        # First check the name of the player and then the evolution list
        return (isinstance(other, Player) and self.name == other.name
                and are_evo_lists_equal(self.evolutions, other.evolutions) and self._pac == other._pac
                and self._sho == other._sho and self._pas == other._pas and self._dri == other._dri
                and self._def == other._def and self._phy == other._phy and self.skills == other.skills
                and self.wf == other.wf and self.playstyles == other.playstyles and self.positions == other.positions
                and self.playstyle_plus == other.playstyle_plus and self.att_wr == other.att_wr
                and self.def_wr == other.def_wr)

    # Adds player stat (ovr, pac, sho, pas, dri, def, phy)
    def add_stat(self, stat_name: str, val: int):
        curr_value = getattr(self, stat_name)
        if curr_value + val >= MAX_STAT:
            setattr(self, stat_name, MAX_STAT)
        else:
            setattr(self, stat_name, curr_value + val)

    # Adds player star value (skills, wf)
    def add_star(self, star_name: str, val: int):
        curr_value = getattr(self, star_name)
        if curr_value + val >= MAX_STARS:
            setattr(self, star_name, MAX_STARS)
        else:
            setattr(self, star_name, curr_value + val)

    # Add positions to set
    def add_positions(self, positions: set):
        self.positions.update(positions)

    # Add playstyles to set
    def add_playstyles(self, new_playstyles: set):
        self.playstyles.update(new_playstyles)

    # Update playstyle plus only if current is None
    def add_playstyle_plus(self, name: str):
        if self.playstyle_plus == "None":
            self.playstyle_plus = name

    # Update work rate - can be "att" or "def" work rate
    def add_wr(self, wr_name: str, val: str):
        if "att" in wr_name:
            self.att_wr = val
        else:
            self.def_wr = val

    # Append evolution to list
    def add_evo(self, done_evo):
        self.evolutions.append(done_evo)

    # Update rarity
    def add_rarity(self, rarity: str):
        self.rarity = rarity

    # Returns a list of the available evolutions for the current player out of evo_list
    def get_avail_evos(self, evo_list: list):
        avail_evos = list()

        for evolution in evo_list:  # Iterate over current evolutions in the game
            if evolution.is_evo_able(self):
                avail_evos.append(evolution)

        return avail_evos

    # Gets conditions and returns T/F if the player match them
    def eval_cond(self, name='', min_pac=0, min_sho=0, min_pas=0, min_dri=0, min_def=0, min_phy=0, min_ovr=0,
                  min_skills=0, min_wf=0, wanted_positions=None, playstyle_plus='', wanted_playstyles=None, att_wr='',
                  def_wr='', wanted_evos=None):
        if name != '':
            if name not in self.name:
                return False

        if wanted_evos is not None:
            if set(wanted_evos).isdisjoint(set(self.evolutions)):  # No desired evolution in path
                return False

        if (self._ovr < min_ovr or self._pac < min_pac or self._sho < min_sho or self._pas < min_pas  # Stat check
                or self._dri < min_dri or self._def < min_def or self._phy < min_phy or self.skills < min_skills
                or self.wf < min_wf):
            return False

        if wanted_positions is not None:
            if wanted_positions.isdisjoint(self.positions):  # No desired position for this player
                return False

        if wanted_playstyles is not None:
            if wanted_playstyles.isdisjoint(self.playstyles):  # No desired playstyle for this player
                return False

        if playstyle_plus != '':
            if playstyle_plus != self.playstyle_plus:
                return False

        if att_wr != '':
            if att_wr != self.att_wr:
                return False

        if def_wr != '':
            if def_wr != self.def_wr:
                return False

        return True

    # Recursive algorithm to find all evo paths for a player under a condition - updates evolved players caught in set
    def update_evo_paths(self, player_set: set, evo_list: list,  **kwargs):
        avail_evos = self.get_avail_evos(evo_list)
        if not avail_evos:  # Checks if available evolutions list of the player is empty - path end
            if self.evolutions and self.eval_cond(**kwargs):  # Evolved player and conditions met for him
                player_set.add(self)  # Add the evolved player to set
            return

        for avail_evo in avail_evos:  # Iterate over available evolutions for the player
            evo_player = avail_evo.evolve(self)
            evo_player.update_evo_paths(player_set, evo_list, **kwargs)  # Recursively expand the evolution path
