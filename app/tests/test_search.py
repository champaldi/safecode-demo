from app.app import create_app

TEST_API_TOKEN = "test-token-1234567890"


def test_search_finds_user():
    client = create_app().test_client()
    r = client.get("/users/search?q=Dana", headers={"Authorization": f"Bearer {TEST_API_TOKEN}"})
    assert r.get_json()[0]["name"] == "Dana"
