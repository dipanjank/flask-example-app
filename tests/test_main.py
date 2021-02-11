import json

import pytest

from main import app, db, Group, User


@pytest.fixture()
def clear_db():
    db.session.query(User).delete()
    db.session.query(Group).delete()
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
    json_in = {
        'name': 'A',
    }

    with app.test_client() as client:
        rv = client.post('/addgroup', json=json_in)
        result_data = json.loads(rv.get_data(as_text=True))
        group_id = result_data['group_id']
        assert db.session.query(Group).count() == 1

        user_in = {'name': "user-A", 'group_id': group_id, 'email': 'user-A@acme.com'}
        client.post('/adduser', json=user_in)
        assert db.session.query(User).count() == 1
