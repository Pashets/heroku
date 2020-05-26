import random

from app import db
from models import User
from string import ascii_uppercase


def test_create():
    """A simple test function, which test create"""

    random_email = ''.join(random.choice(ascii_uppercase) for i in range(10)) + '@gmail.com'
    user_dont_exist = User.query.filter(User.email == random_email).first()
    assert user_dont_exist is None
    new_user = User(email=random_email, password=random_email)
    db.session.add(new_user)
    db.session.commit()
    user_exist = User.query.filter(User.email == random_email).first()
    assert user_exist == new_user
    User.query.filter(User.email == random_email).delete()
    user_dont_exist = User.query.filter(User.email == random_email).first()
    assert user_dont_exist is None


def test_read():
    """A simple test function, which test read"""

    random_email = ''.join(random.choice(ascii_uppercase) for i in range(10)) + '@gmail.com'
    new_user = User(email=random_email, password=random_email)
    db.session.add(new_user)
    db.session.commit()
    user_exist = User.query.filter(User.email == random_email).first()
    assert user_exist == new_user
    User.query.filter(User.email == random_email).delete()
    user_dont_exist = User.query.filter(User.email == random_email).first()
    assert user_dont_exist is None


def test_update():
    """A simple test function, which test update"""

    random_email = ''.join(random.choice(ascii_uppercase) for i in range(10)) + '@gmail.com'
    random_email_2 = ''.join(random.choice(ascii_uppercase) for i in range(10)) + '@gmail.com'
    user = User(email=random_email, password=random_email)
    db.session.add(user)
    db.session.commit()
    user_exist = User.query.filter(User.email == random_email).first()
    assert user_exist == user
    user_update = User.query.filter(User.email == random_email).first()
    user_update.email = random_email_2
    db.session.add(user_update)
    db.session.commit()
    user_check = User.query.filter(User.email == random_email_2).first()
    assert user_check == user_update
    User.query.filter(User.email == random_email_2).delete()
    user_dont_exist = User.query.filter(User.email == random_email_2).first()
    assert user_dont_exist is None


def test_delete():
    """A simple test function, which test delete"""

    random_email = ''.join(random.choice(ascii_uppercase) for i in range(10)) + '@gmail.com'
    user_dont_exist = User.query.filter(User.email == random_email).first()
    assert user_dont_exist is None
    new_user = User(email=random_email, password=random_email)
    db.session.add(new_user)
    db.session.commit()
    user_exist = User.query.filter(User.email == random_email).first()
    assert user_exist == new_user
    User.query.filter(User.email == random_email).delete()
    user_dont_exist = User.query.filter(User.email == random_email).first()
    assert user_dont_exist is None
