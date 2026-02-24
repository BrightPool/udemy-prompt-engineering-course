# Tool Schema Pattern (No Manual JSON Typing)

Use Pydantic models to generate tool parameter schemas automatically.

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ToolArgsBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SearchOrdersArgs(ToolArgsBase):
    customer_email: str | None = Field(..., description="Customer email address.")
    order_id: int | None = Field(..., description="Specific order ID.")
    status: Literal["pending", "shipped", "delivered", "refunded"] | None = Field(
        ...,
        description="Order status filter.",
    )


def function_tool(name: str, description: str, args_model: type[BaseModel]) -> dict:
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": args_model.model_json_schema(),
        "strict": True,
    }
```

Then build your tools with:

```python
tools = [
    function_tool("search_orders", "Search for customer orders.", SearchOrdersArgs),
]
```

This keeps schemas valid and easy to maintain while matching OpenAI's strict tool-calling flow.
