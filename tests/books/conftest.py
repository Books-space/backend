import random

import pytest


@pytest.fixture
def number():
    return random.randint(0, 10)


@pytest.fixture
def name():
    return random.choice(['Vladimir', 'Alex'])


@pytest.fixture()
def books_creator():
    uid = random.randint(0, 10)
    print(f"insert into books (uid) ({uid})")
    yield uid
    print(f"delete from books where uid={uid}")


@pytest.fixture()
def db():
    engine = ...
    yield engine
    engine.close()

