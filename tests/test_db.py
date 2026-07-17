# test_db.py

import unittest
import os
os.environ['TESTING'] = 'true'

from peewee import *

from app import TimelinePost, mydb

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()
        mydb.bind(MODELS, bind_refs=False, bind_backrefs=False)

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        # Get timeline posts and assert that they are correct.
        posts = list(TimelinePost.select().order_by(TimelinePost.created_at.desc()))
        assert len(posts) == 2

        retrieved_first = TimelinePost.get(TimelinePost.id == 1)
        assert retrieved_first.name == 'John Doe'
        assert retrieved_first.email == 'john@example.com'
        assert retrieved_first.content == 'Hello world, I\'m John!'

        retrieved_second = TimelinePost.get(TimelinePost.id == 2)
        assert retrieved_second.name == 'Jane Doe'
        assert retrieved_second.email == 'jane@example.com'
        assert retrieved_second.content == 'Hello world, I\'m Jane!'
