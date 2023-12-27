# Custom lists of evolutions equality check - checks same elements are equal regardless of order
def are_evo_lists_equal(list1, list2):
    if len(list1) != len(list2):
        return False

    return all(item in list2 for item in list1)


# Parse str to set
def to_set(_str: str):
    if _str == '-':  # Empty set
        return set()
    else:
        return set(_str.split(','))


# Get basic rarity (bronze, silver, gold) from ovr rating
def get_rarity(_ovr: int):
    if _ovr >= 75:
        return 'Gold'
    elif _ovr >= 65:
        return 'Silver'
    else:
        return 'Bronze'

