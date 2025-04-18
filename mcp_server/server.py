from mcp.server import FastMCP
from service.order_dataset_service import get_all_orders as service_get_all_orders

mcp = FastMCP("Thanh server")

@mcp.tool()
def get_all_orders(limit: int = 5, page: int  = 1):
    """Get some orders from the database base on limit and page"""
    results = service_get_all_orders(limit=limit, page=page)
    return results

