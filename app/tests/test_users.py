from app.app import create_app


def test_list_users():
    r = create_app().test_client().get("/users")
    assert [u["name"] for u in r.get_json()] == ["Aigerim", "Dana"]


def test_missing_user_is_404():
    assert create_app().test_client().get("/users/99").status_code == 404
