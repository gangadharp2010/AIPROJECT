import re
from database.db_connection import get_connection
from rag.retriever import search_knowledge

def list_destinations():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT name,state,category,cost_per_person_per_night,recommended_nights,best_months "
            "FROM destinations ORDER BY name"
        ).fetchall()
    return [dict(r) for r in rows]

def get_destination(name):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM destinations WHERE lower(name)=lower(?)", (name,)
        ).fetchone()
    return dict(row) if row else None

def estimate_trip(destination, friends=1, nights=2, budget_per_person=None):
    item = get_destination(destination)
    if not item:
        return {"error": f"I don't have {destination} in the sample destination database."}
    friends = max(1, int(friends))
    nights = max(1, int(nights))
    # Estimate includes 10% for food/local transport/activities on top of stay baseline.
    stay = item["cost_per_person_per_night"] * nights
    per_person = round(stay * 1.10)
    total = per_person * friends
    result = {
        "destination": item["name"],
        "friends": friends,
        "nights": nights,
        "estimated_per_person": per_person,
        "estimated_group_total": total,
        "budget_per_person": budget_per_person,
        "within_budget": None if budget_per_person is None else per_person <= budget_per_person,
        "assumption": "Sample stay rate × nights, plus 10% allowance for food/local transport/activities. Intercity travel is not included."
    }
    return result

def compare_budget(budget_per_person, friends, nights):
    results = []
    for item in list_destinations():
        estimate = estimate_trip(item["name"], friends, nights, budget_per_person)
        if estimate.get("within_budget"):
            results.append(estimate)
    results.sort(key=lambda x: x["estimated_per_person"])
    return results

def search_travel_tips(query, top_k=3):
    return search_knowledge(query, top_k=top_k)

def extract_number(pattern, text, default):
    match = re.search(pattern, text, re.I)
    if not match:
        return default
    try:
        return int(match.group(1).replace(",", ""))
    except ValueError:
        return default
