def create_user(client, email, password, role="viewer", token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.post(
        "/users/",
        json={"email": email, "password": password, "role": role},
        headers=headers,
    )
def login(client, email, password):
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response

def test_bootstrap_first_user_public_then_locked(client):
    first = create_user(client, "admin@example.com", "Password123", "admin")
    assert first.status_code == 201
    second_without_token = create_user(
        client, "analyst@example.com", "Password123", "analyst")
    assert second_without_token.status_code == 403

def test_admin_can_create_user_after_login(client):
    create_user(client, "admin@example.com", "Password123", "admin")
    login_response = login(client, "admin@example.com", "Password123")
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    created = create_user(client, "viewer@example.com","Password123", "viewer", token)
    assert created.status_code == 201
    assert created.json()["role"] == "viewer"

def test_user_validation_role_and_password(client):
    bad_role = client.post(
        "/users/",json={"email": "x@example.com","password": "Password123", "role": "owner"},)
    assert bad_role.status_code == 422
    short_password = client.post("/users/",json={"email": "y@example.com", "password": "short", "role": "viewer"},)
    assert short_password.status_code == 422
