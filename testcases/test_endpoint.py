from pytest import fixture
from bson.objectid import ObjectId
import requests
import time
import json

from helpers.mongo_helper import db

URL = 'http://0.0.0.0:11000'


@fixture(scope='module')
def add_entry(request):
    """
    Adds entry to the DB.

    Args:

    Returns(str): entry id.

    """
    test_cmd = 'pwd'
    data = {"cmd": '"{}"'.format(test_cmd)}
    endpoint = "{}/new_task".format(URL)
    response = requests.post(endpoint, json=data)
    time.sleep(1)
    assert response.status_code == 200, 'Failed to add'\
                                        ' new entry: {}'.format(response.text)
    _id = json.loads(response.text)['id']

    def delete_entry():
        """
        Deletes generated entry.
        """
        db.collection.delete_one({"_id": ObjectId(_id)})

    request.addfinalizer(delete_entry)
    return _id


def test_add_entry(add_entry):
    """
    Setup:
        - Adds test entry.

    Test steps:
        - Verify the entry is present on the collection.

    Teardown:
        - Delete the test entry

    """
    _id = add_entry

    endpoint = '{}/get_output/{}'.format(URL, _id)
    response =  requests.get(endpoint)
    output = json.loads(response.text)['output']
    assert output, 'Entry is not present on the collection'
    assert "/usr/src/mongo_app" in output, 'Output is not the'\
                                           ' expected one: {}'.format(output)
