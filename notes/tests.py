from django.test import TestCase
from django.test import Client

from tudutul.models import Note, User, Table
from notes.views import get_all_notes_for_user, NoteView


class TestNotes(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['userLogin'] = 'TestUser'
        session.save()

        self.user1 = User(
            login='TestUser',
            email='test@user.com',
            password='pass'
        )
        self.user1.save()

        self.table1 = Table(
            name='TestTable',
            is_shared=False,
            owner='TestUser'
        )
        self.table1.save()

        self.note1 = Note(
            name='TestNote',
            creator='TestUser',
            content='TestContent',
            completion_date='2021-12-21',
            priority=5,
            owning_table_id=self.table1.id
        )
        self.note1.save()

    def test_note_created(self):
        self.assertEqual(self.note1.name, 'TestNote')

    def test_get_all_notes_helper_returns_user_created_notes(self):
        expected = [self.note1.id]
        tested = [el['id'] for el in get_all_notes_for_user(self.user1.login)]
        self.assertListEqual(expected, tested)

    def test_get_all_notes_helper_returns_from_users_tables(self):
        note2 = Note.objects.create(
            name='TestTableNote',
            creator='TestTableUser',
            content='TestContent',
            completion_date='2021-12-21',
            priority=5,
            owning_table_id=self.table1.id
        )

        expected = [self.note1.id, note2.id]
        tested = [el['id'] for el in get_all_notes_for_user(self.user1.login)]
        self.assertListEqual(expected, tested)

    def test_get_all_notes_helper_returns_from_shared_tables(self):
        table2 = Table.objects.create(
            name='TestSharedTable',
            is_shared=True,
            owner='TestSharedUser'
        )
        note2 = Note.objects.create(
            name='TestSharedNote',
            creator='TestSharedUser',
            content='TestContent',
            completion_date='2021-12-21',
            priority=5,
            owning_table_id=table2.id
        )
        table2.shared_with.add(self.user1)

        expected = [self.note1.id, note2.id]
        tested = [el['id'] for el in get_all_notes_for_user(self.user1.login)]
        self.assertListEqual(expected, tested)

    def test_get_request_returns_all_notes(self):
        table2 = Table.objects.create(
            name='TestSharedTable',
            is_shared=True,
            owner='TestSharedUser'
        )
        note2 = Note.objects.create(
            name='TestSharedNote',
            creator='TestSharedUser',
            content='TestContent',
            completion_date='2021-12-21',
            priority=5,
            owning_table_id=table2.id
        )
        table2.shared_with.add(self.user1)

        note3 = Note.objects.create(
            name='TestTableNote',
            creator='TestTableUser',
            content='TestContent',
            completion_date='2021-12-21',
            priority=5,
            owning_table_id=self.table1.id
        )

        response = self.client.get('/note/')
        expected = [self.note1.id, note2.id, note3.id]
        tested = [el['id'] for el in response.data['ans']]
        self.assertListEqual(expected, tested)

    def test_get_request_returns_only_from_specified_date(self):
        note2 = Note.objects.create(
            name='TestNote',
            creator='TestUser',
            content='TestContent',
            completion_date='2021-12-23 16:30',
            priority=5
        )

        response = self.client.get('/note/', {'completion_date': '2021-12-23'})
        expected = [note2.id]
        tested = [el['id'] for el in response.data['ans']]
        self.assertListEqual(expected, tested)

    def test_get_request_returns_only_from_specified_table(self):
        table2 = Table.objects.create(
            name='TestTable',
            is_shared=True,
            owner='TestUser'
        )
        note2 = Note.objects.create(
            name='TestSharedNote',
            creator='TestUser',
            content='TestContent',
            completion_date='2021-12-21',
            priority=5,
            owning_table_id=table2.id
        )

        response = self.client.get('/note/', {'table_id': table2.id})
        expected = [note2.id]
        tested = [el['id'] for el in response.data['ans']]
        self.assertListEqual(expected, tested)
