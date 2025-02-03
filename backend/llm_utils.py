import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY')
)

functions_schema = [
    {
        "name": "save_order",
        "description": "get restaurant order from user. DO NOT ask additional questions only return the burger, fries, and drink count if not found return 0",
        "parameters": {
            "type": "object",
            "properties": {
                "burger": {"type": "string", "description": "the burger count"},
                "drink": {"type": "string", "description": "the drink count"},
                "fries": {"type": "string", "description": "the fries count"},
        },
        "required": ["burger", "fries", "drink"]
        }
    },
    {
        "name": "cancel_order",
        "description": "cancel restaurant order. DO NOT ask additional questions only return the order number to be cancelled",
        "parameters": {
            "type": "object",
            "properties": {
                "order_number": {"type": "string", "description": "order number to be cancelled"},
        },
        "required": ["order_number"]
        }
    },
    {
        "name": "non_related_request",
        "description": "any request that is not related to ordering or cancelling an order",
        "parameters": {}
    }
]


def process_order(user_prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {"role": "user", "content": user_prompt}
        ],
        functions=functions_schema,
        function_call="auto"
    )

    output = completion.choices[0].message
    return output

