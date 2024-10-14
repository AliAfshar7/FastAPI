import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    print (res.json().get('message'))
    assert res.json().get('message') == 'hello docker world'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email":"afsh@gmail.com","password":"123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'afsh@gmail.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = int(payload.get("user_id"))
    assert id == test_user['ID']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com','password123', 403),
    ('ali@yahoo.com','wrongpassword', 403),
    ('wrongemail@gmail.com','wrongpassword',403),
    (None,'password123', 422),
    ('ali@yahoo.com', None, 422)   
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={'username':email,'password':password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials'