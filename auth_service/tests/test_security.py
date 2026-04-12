from app.core.security import hash_password, verify_password, create_access_token, decode_token

def test_hash_password_returns_different_string():
    password = "mysecret123"
    hashed = hash_password(password)
    assert hashed != password
    assert hashed.startswith("$2b$")

def test_verify_password_correct():
    password = "mysecret123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    password = "mysecret123"
    wrong_password = "wrongpass"
    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) is False

def test_create_access_token_contains_required_fields():
    user_id = 42
    role = "admin"
    token = create_access_token(user_id, role)
    payload = decode_token(token)
    
    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["role"] == role
    assert "iat" in payload
    assert "exp" in payload

def test_create_access_token_default_role():
    user_id = 100
    token = create_access_token(user_id)
    payload = decode_token(token)
    
    assert payload["role"] == "user"
