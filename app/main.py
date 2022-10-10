import asyncio
from typing import Dict, Optional, Union

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


class Account(BaseModel):
    name: str
    description: Optional[str] = None
    balance: float
    active: bool = True

app = FastAPI(
    title = "AccountAPI",
    version = "1.0.0",
    description = "Simple API for managing system accounts.",
    openapi_url="/api/v1/openapi.json"
)

accounts = dict()

async def get_account(account_id: int) -> Optional[Account]:
    if account_id in accounts:
        return accounts[account_id]
    else:
        return None

async def add_account(account_id: int, account: Account) -> Optional[Account]:
    if account_id in accounts:
        return None
    else:
        accounts[account_id] = account.dict()
        return accounts[account_id]

async def update_account(account_id: int, account: Account) -> Optional[Account]:
    if account_id in accounts:
        accounts[account_id] = account.dict()
        return accounts[account_id]
    else:
        return None

async def delete_account(account_id: int) -> Optional[bool]:
    if account_id in accounts:
        del accounts[account_id]
        return True
    else:
        return False


@app.get("/healthz", status_code=200)
async def get_health(request: Request) -> Union[Optional[Dict], HTTPException]:
    return {"status": True}

@app.get("/accounts/{account_id}", status_code=200)
async def get(account_id: int):
    res = await get_account(account_id)
    if res is None:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found!")
    else:
        return res

@app.post("/accounts/{account_id}", status_code=201)
async def create(account_id: int, account: Account):
    res = await add_account(account_id, account)
    if res is None:
        raise HTTPException(status_code=409, detail=f"Account with ID {account_id} already exists!")
    else:
        return res

@app.put("/accounts/{account_id}", status_code=200)
async def update(account_id: int, account: Account):
    res = await update_account(account_id, account)
    if res is None:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found!")
    else:
        return res

@app.delete("/accounts/{account_id}", status_code=200)
async def remove(account_id: int):
    res = await delete_account(account_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found!")
    else:
        return {"message": "Successful"}