import pytest
@pytest.mark.asyncio
async def test_insights(client):
    await client.post("/api/reviews", json={"product": "app", "text": "Great UX but expensive pricing", "rating": 4})
    r = await client.get("/api/insights", params={"product": "app"})
    assert r.status_code == 200
    assert r.json()["count"] >= 1
