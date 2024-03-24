from unittest.mock import patch
from fastapi.testclient import TestClient
from types import SimpleNamespace
from ..main import app
client = TestClient(app)


@patch('blog.service.create_user')
@patch('blog.service.get_user_by_email')
def test_create_user(mock_get_user_by_email, mock_create_user):
    mock_get_user_by_email.return_value = None
    mock_create_user.return_value = {
        "id": 1, "name": "test", "location": "test", "email": "user@example.com"}

    response = client.post(
        "/users/", json={"name": "test", "location": "test", "email": "user@example.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {'name': 'test',
                               'email': 'user@example.com', 'id': 1}


@patch('blog.service.get_user_by_email')
@patch('blog.auth.verify_password')
@patch('blog.auth.create_access_token')
def test_login_for_access_token(mock_create_access_token, mock_verify_password, mock_get_user_by_email):
    # Using SimpleNamespace for attribute access
    mock_user = SimpleNamespace(
        id=1, email="user@example.com", hashed_password="hashed")
    mock_get_user_by_email.return_value = mock_user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "test_token"

    response = client.post(
        "/token", data={"username": "user@example.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "test_token", "token_type": "bearer"}


@patch('blog.auth.get_current_user')
@patch('blog.auth.verify_token')
@patch('blog.service.get_blog_posts_by_user')
@patch('blog.auth.verify_token')
def test_read_blog_posts_for_user(mock_create_access_token, mock_get_blog_posts_by_user, mock_verify_token, mock_get_current_user):
    # Setting up the mock to return a predetermined access token
    mock_create_access_token.return_value = "test_token"
    mock_verify_token.return_value = 1
    mock_get_current_user.return_value = 1
    mock_get_blog_posts_by_user.return_value = [
        {"id": 1, "title": "Test Post", "content": "Content"}]

    # Including the Authorization header with the mocked token in the request
    headers = {"Authorization": f"Bearer test_token"}
    response = client.get("/users/1/blog_posts/", headers=headers)

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Test Post", "content": "Content"}]


@patch('blog.auth.get_current_user')
@patch('blog.service.get_blog_posts_by_user')
def test_non_auth_read_blog_posts_for_user(mock_get_blog_posts_by_user, mock_get_current_user):
    mock_get_current_user.return_value = 1
    mock_get_blog_posts_by_user.return_value = [
        {"id": 1, "title": "Test Post", "content": "Content"}]

    response = client.get("/users/1/blog_posts/")
    assert response.status_code == 401
