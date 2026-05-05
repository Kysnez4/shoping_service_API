import pytest

from app.user.models import User


@pytest.fixture(autouse=True)
def create_dummy_user(tmpdir):
    from conf_test_db import override_get_db
    database = next(override_get_db())
    new_user = User(name='Saduchi', email='sadauchi1267@gmail.com', password='Sadauchi98764')
    database.add(new_user)
    database.commit()

    yield

    database.query(User).filter(User.email == 'sadauchi1267@gmail.com').delete()
    database.commit()
