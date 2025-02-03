import json
from db import save_order, cancel_order, get_orders
from llm_utils import process_order
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:5173",
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "ok"}

class UserPrompt(BaseModel):
    prompt: str

@app.post("/order")
async def order(user_prompt: UserPrompt):

    output = process_order(user_prompt.prompt)
    
    args = json.loads(output.function_call.arguments)
    match output.function_call.name:
        case "save_order":
            save_order(args)
        case "cancel_order":
            cancel_order(int(args["order_number"]))
        case "non_related_request":
            return {"message": "Invalid function call"}
    orders = get_orders()
    return {"orders": orders}

@app.get("/orders")
async def get_all_orders():
    orders = get_orders()
    return {"orders": orders}
