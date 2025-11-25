import asyncio

async def send_message(ctx, text: str):
    print(f"[TASK] Notify: {text}")

    await asyncio.sleep(0.1)
    return {"status": "ok"}