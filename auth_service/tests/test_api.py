import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.api.deps import get_db

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL_TEST, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "role" in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post("/auth/register", json={"email": "duplicate@example.com", "password": "pass"})
    response = await client.post("/auth/register", json={"email": "duplicate@example.com", "password": "pass"})
    assert response.status_code == 409
    assert "User already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={"email": "login@example.com", "password": "secret"})
    response = await client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={"email": "wrongpass@example.com", "password": "correct"})
    response = await client.post(
        "/auth/login",
        data={"username": "wrongpass@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_user_not_exists(client):
    response = await client.post(
        "/auth/login",
        data={"username": "nonexistent@example.com", "password": "anything"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_me_success(client):
    await client.post("/auth/register", json={"email": "me@example.com", "password": "pass"})
    login_resp = await client.post("/auth/login", data={"username": "me@example.com", "password": "pass"})
    token = login_resp.json()["access_token"]
    
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"

@pytest.mark.asyncio
async def test_me_no_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_me_invalid_token(client):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
