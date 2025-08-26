from agents import function_tool

ORDERS = {
    "123": {"status": "Shipped", "eta": "3 days"},
    "456": {"status": "Processing", "eta": "5 days"},
    "789": {"status": "Delivered", "eta": "Yesterday"},
}

def is_order_query(ctx, agent) -> bool:
    """
    Returns True if the user query is about an order.
    Looks for keywords like 'order', 'tracking', or 'status'.
    """
    text = (ctx.context.get("text_input") or "").lower()
    return any(word in text for word in ["order", "tracking", "status"])


# ------------------------------
# Function Tool: Get Order Status
# ------------------------------
@function_tool(
    is_enabled=is_order_query,
    failure_error_function=lambda *args, **kwargs: "Sorry, I couldn't find that order. Please double-check the order ID.",
)
def get_order_status(order_id: str):
    """
    Fetches the status of an order by ID.
    Example IDs: 123, 456, 789.
    """
    order = ORDERS.get(order_id)
    if not order:
        raise ValueError("Order not found")  # triggers error_function
    return {
        "order_id": order_id,
        "status": order["status"],
        "estimated_delivery": order["eta"],
    }
    
    
    
    
