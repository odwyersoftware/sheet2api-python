import uuid
import pytest

from sheet2api import Sheet2APIClient

URL = (
    'https://sheet2api.com/v1/FgI6zV8qT121/'
    'testing-sheet-simple_python_client_read_write/'
)
URL_AUTH = (
    'https://sheet2api.com/v1/FgI6zV8qT121/'
    'testing-sheet-simple_python_client_read_auth/'
)


@pytest.fixture
def client():
    return Sheet2APIClient(api_url=URL)


@pytest.fixture
def client_with_auth():
    return Sheet2APIClient(
        api_url=URL_AUTH, username='mruser', password='mrpassword'
    )


class TestReadRows:
    @pytest.mark.parametrize('client_fixture', ['client', 'client_with_auth'])
    def test_returns_all_rows_in_spreadsheet(self, client_fixture, request):
        client = request.getfixturevalue(client_fixture)

        rows = client.read_rows()

        assert rows == [{
            'name': 'Bob',
            'age': 22
        }, {
            'name': 'Richard',
            'age': 19
        }, {
            'name': 'Bob Jones',
            'age': 99
        }]

    def test_returns_all_rows_for_a_specific_sheet(self, client):
        rows = client.read_rows(sheet='Address')

        assert rows == [{
            'name': 'Bob',
            'address': 'Bob Street'
        }, {
            'name': 'Richard',
            'address': 'Richard Street'
        }]

    def test_returns_filtered_rows_when_query_is_passed(self, client):
        rows = client.read_rows(query={'name': 'Bob'})

        assert rows == [{'name': 'Bob', 'age': 22}]


class TestCreateRow:
    @pytest.mark.parametrize('sheet', [None, 'Age'])
    def test_creates_a_new_row(self, client, request, sheet):
        name = str(uuid.uuid4())
        row = {
            'name': name,
            'age': 18,
        }

        def fin():
            client.delete_rows(sheet=sheet, query={'name': name})

        request.addfinalizer(fin)

        added_row = client.create_row(sheet=sheet, row=row)

        assert added_row == row
        assert client.read_rows(sheet=sheet) == [row] + [{
            'name': 'Bob',
            'age': 22
        }, {
            'name': 'Richard',
            'age': 19
        }, {
            'name': 'Bob Jones',
            'age': 99
        }]


class TestUpdateRows:
    @pytest.mark.parametrize('sheet', [None, 'Age'])
    def test_update_rows(self, client, sheet, request):
        name = str(uuid.uuid4())
        row = {
            'name': name,
            'age': 18,
        }

        def fin():
            client.delete_rows(sheet=sheet, query={'name': name})

        request.addfinalizer(fin)
        client.create_row(sheet=sheet, row=row)

        updates_made = client.update_rows(
            sheet=sheet,
            query={'name': name},
            row={
                'name': name,
                'age': 99999
            },
        )

        assert updates_made == [{'name': name, 'age': 99999}]
        assert client.read_rows(sheet=sheet) == [{
            'name': name,
            'age': 99999
        }, {
            'name': 'Bob',
            'age': 22
        }, {
            'name': 'Richard',
            'age': 19
        }, {
            'name': 'Bob Jones',
            'age': 99
        }]

    def test_update_rows_partially(self, client, request):
        sheet = None
        name = str(uuid.uuid4())
        row = {
            'name': name,
            'age': 18,
        }

        def fin():
            client.delete_rows(sheet=sheet, query={'name': name})

        request.addfinalizer(fin)
        client.create_row(sheet=sheet, row=row)

        updates_made = client.update_rows(
            sheet=sheet,
            query={'name': name},
            row={
                'name': name,
            },
            partial_update=True,
        )

        assert updates_made == [{'name': name}]
        assert client.read_rows(sheet=sheet) == [{
            'name': name,
            'age': 18
        }, {
            'name': 'Bob',
            'age': 22
        }, {
            'name': 'Richard',
            'age': 19
        }, {
            'name': 'Bob Jones',
            'age': 99
        }]
