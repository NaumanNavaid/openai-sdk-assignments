HOTELS = {
    "hotel sannata": {
        "name": "Hotel Sannata",
        "owner": "Mr. Ratan Lal",
        "total_rooms": 200,
        "private_rooms": 20
    },
    "hotel one": {
        "name": "Hotel One",
        "owner": "Mr. Nauman Navaid",
        "total_rooms": 150,
        "private_rooms": 10
    },
    "hotel grand": {
        "name": "Hotel Grand",
        "owner": "Ms. Ayesha Khan",
        "total_rooms": 300,
        "private_rooms": 30
    }
}
from agents import RunContextWrapper

def dynamic_instruction(ctx: RunContextWrapper, agent):
    """
    Looks at the raw user input, finds a hotel name if mentioned,
    and returns tailored instructions.
    """
    query = (ctx.context.get("user_input") or "").lower()

    for hotel_key, hotel in HOTELS.items():
        if hotel_key in query:
            return (
                f"You are a helpful hotel customer care assistant for {hotel['name']}.\n"
                f"- Hotel total rooms: {hotel['total_rooms']}.\n"
                f"- Hotel Owner: {hotel['owner']}.\n"
                f"- {hotel['private_rooms']} rooms are not available for the public, "
                f"they are reserved for special guests."
            )

    # Default fallback
    return (
        "You are a helpful hotel customer care assistant. "
        "The user did not mention a hotel. Ask politely which hotel "
        "they are inquiring about (Hotel Sannata, Hotel One, or Hotel Grand)."
    )