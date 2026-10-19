from mcp.server.fastmcp import FastMCP
import httpx
import os
import uvicorn

mcp = FastMCP("ntfy")

NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "yueyue-Claude")

@mcp.tool()
async def send_message(message: str, title: str = "") -> str:
    """Send a notification to phone"""
    async with httpx.AsyncClient() as client:
        payload = {"topic": NTFY_TOPIC, "message": message}
        if title:
            payload["title"] = title
        r = await client.post("https://ntfy.sh", json=payload)
        return f"Sent: {r.status_code}"

app = mcp.sse_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
