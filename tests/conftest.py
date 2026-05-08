import pytest
from conf_test_db import override_get_db
from app.user.models import User, Role

@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    database = next(override_get_db())
    role = Role(name="admin")
    database.add(role)
    role = Role(name="user")
    database.add(role)
    database.commit()

@pytest.fixture(autouse=True)
def create_dummy_user(tmpdir):
    database = next(override_get_db())
    new_user = User(name='Saduchi', email='sadauchi1267@gmail.com', phone="+79999999999" , password='Sadauchi98764', role_id=1)
    database.add(new_user)
    database.commit()

    yield

    database.query(User).filter(User.email == 'sadauchi1267@gmail.com').delete()
    database.commit()
