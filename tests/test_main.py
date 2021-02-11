from main import app
from main import db, User
import pytest


@pytest.fixture()
def clear_db():
    db.session.query(User).delete()
    yield


@pytest.mark.usefixtures("clear_db")
def test_index():
    app.config['TESTING'] = True
    with app.test_client() as client:
        result = client.get('/')
        assert result.get_json() == {'status': 'ok'}


@pytest.mark.usefixtures("clear_db")
def test_add_user():
    app.config['TESTING'] = True
    json_in = [
        {
            'name': 'A',
            'email': 'A@acme.org',
        },
        {
            'name': 'B',
            'email': 'B@acme.org',
        },
    ]

    with app.test_client() as client:
        client.post('/adduser', json=json_in)
        assert db.session.query(User).count() == 2
