from fastmcp import FastMCP
from fastmcp.tools.tool import ToolResult
from fastmcp.exceptions import ToolError

import requests
import os
import json

mcp = FastMCP(name="FoodTracker")


@mcp.tool
def list_items(page: int = 1, limit: int = 10) -> ToolResult:
    """List items in the database with pagination
    Args:
        page: int = 1,
        limit: int = 10,
    """
    try:
        url = f"{os.getenv('BACKEND_URL', 'backend:8000')}/api/v1/tracker/list_items"
        params = {"page": page, "limit": limit}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ToolError(f"Failed to list items: {response.text}")
        return ToolResult(
            content=json.dumps(response.json()),
            structured_content=response.json(),
        )
    except Exception as e:
        raise ToolError(f"Failed to list items: {str(e)}")


@mcp.tool
def insert_item(
    order_type: str,
    description: str,
    category: str,
    restaurant: str,
    price: int,
    purchased_at: str,
) -> ToolResult:
    """Insert an item into the database
    Args:
        order_type: str = "Grabfood, Gofood, Shopeefood, Offline"
        description: str = "items details"
        category: str = "Food, Beverage, Snack"
        restaurant: str = "Name of the store/restaurant"
        price: int = "Price of the item"
        purchased_at: str = "Date and time when the item is purchased if the receipt includes it. If not use the current time"
    """
    try:
        url = f"{os.getenv('BACKEND_URL', 'backend:8000')}/api/v1/tracker/insert_item"
        response = requests.post(
            url,
            json={
                "name": order_type,
                "description": description,
                "category": category,
                "restaurant": restaurant,
                "price": price,
                "purchased_at": purchased_at,
            },
        )
        if response.status_code != 200:
            raise ToolError(f"Failed to insert item: {response.text}")
        return ToolResult(
            content=json.dumps(response.json()),
            structured_content=response.json(),
        )
    except Exception as e:
        raise ToolError(f"Failed to insert item: {str(e)}")


@mcp.tool
def execute_select_query(sql_query: str) -> ToolResult:
    """Execute a select query on the database
    Args:
        sql_query: str
    """
    try:
        url = f"{os.getenv('BACKEND_URL', 'backend:8000')}/api/v1/tracker/execute_select_query"
        response = requests.post(url, params={"sql_statement": sql_query})
        if response.status_code != 200:
            raise ToolError(f"Failed to execute select query: {response.text}")
        return ToolResult(
            content=json.dumps(response.json()),
            structured_content=response.json(),
        )
    except Exception as e:
        raise ToolError(f"Failed to execute select query: {str(e)}")


@mcp.tool
def get_schema() -> ToolResult:
    """Get the schema of the database"""
    url = f"{os.getenv('BACKEND_URL', 'backend:8000')}/api/v1/tracker/schema"
    response = requests.get(url)
    return ToolResult(
        content=json.dumps(response.json()),
        structured_content=response.json(),
    )


@mcp.resource("data://schema")
def get_schema_resource() -> dict:
    """Get the schema of the database"""
    url = f"{os.getenv('BACKEND_URL', 'backend:8000')}/api/v1/tracker/schema"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
