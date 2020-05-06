# sheet2api-python

Google/Excel Sheets API Python Client. For use with https://sheet.com/

[![Build Status](https://travis-ci.org/ODwyerSoftware/sheet2api-python.svg?branch=master)](https://travis-ci.org/ODwyerSoftware/sheet2api-python)

[![PyPI version](https://badge.fury.io/py/sheet2api.svg)](https://pypi.org/project/sheet2api/)

## Installation

```bash
pip install sheet2api
```

## Usage Examples

Before starting you should head over to [https://sheet2api.com/](https://sheet2api.com/documentation/) and link up your Google Sheets or Excel Online account and create your first Spreadsheet API.

Next, create an instance of the client and pass in the API URL to your API.

```python
from sheet2api import SheetAPIClient

client = SheetAPIClient(api_url='https://sheet2api.com/v1/FgI6zV8qT222/my-api/')
# If your API has authentication enabled
client = SheetAPIClient(
    api_url='https://sheet2api.com/v1/FgI6zV8qT222/my-api/',
    username='api_username_here',
    password='api_password_here',
)
```

### Get all rows

Returns all rows within the **first** Sheet of your Spreadsheet.

```python
client.get_rows()

# Returns a list of dicts
[{
	'name': 'Bob',
	'age': 22
}, {
	'name': 'Richard',
	'age': 19
}, {
	'name': 'Bob Jones',
	'age': 99
}]
```

To return rows from a specific Sheet.


```python
client.get_rows(sheet='Sheet1')
```

### Get all rows matching a query

Returns all rows matching a query.

```python
client.get_rows(query={'name': 'Bob'})
```


### Create a new row

```python
client.create_row(sheet='Sheet1', row={'name': 'Jane','age': 18,})
```

### Update all rows which match a query

This will update the entire row for the matches, if you fail to specificy all column values in the replacement `row`, those cells will be filled with an empty value.

```python
client.update_rows(
    sheet='Sheet1,
    query={'name': 'Philip'},
    row={
        'name': 'Phil',
        'age': 99999
    },
)
```

Partially update rows matching a query.

This will only update the columns which you provide replacement values for in the `row` dict parameter. All other columns will be left unchanged.

```python
client.update_rows(
    sheet='Sheet1,
    query={'name': 'Philip'},
    row={
        'age': 99999
    },
)
```


### Delete all rows matching a query

```python
client.delete_rows(sheet='Sheet1', query={'name': 'Satan'})
```
