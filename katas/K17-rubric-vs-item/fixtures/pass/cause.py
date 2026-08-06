def cause(item_ambiguous, rubric_vague):
    if item_ambiguous and rubric_vague:
        return "both"
    if item_ambiguous:
        return "item"
    if rubric_vague:
        return "rubric"
    return "neither"
