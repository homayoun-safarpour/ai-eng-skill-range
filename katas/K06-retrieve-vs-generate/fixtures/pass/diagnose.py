def diagnose(retrieved_ids, relevant_ids, answer_has_hallucination):
    retrieved = set(retrieved_ids)
    if not set(relevant_ids).issubset(retrieved):
        return "retrieval"
    if answer_has_hallucination:
        return "generation"
    return "ok"
