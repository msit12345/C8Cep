import base64
import time
import json
from conftest import get_fabric
from helpers import get_regions
from helpers import get_fabric
from helpers import verify_collection_replicated
from constants import GUEST_MAIL, GUEST_PASSWORD
from constants import SYSTEM_DB, TEST_COLLECTION


def test_create_collection(sys_fabric):
    employees = sys_fabric.create_collection(TEST_COLLECTION)
    assert employees.name == TEST_COLLECTION


def test_create_hashindex(sys_fabric):
    employees = sys_fabric.collection(TEST_COLLECTION)
    hash_index = employees.add_hash_index(fields=['email', '_key'],
                                          unique=True)
    expected_fields = {"fields": ["email", "_key"]}
    assert hash_index["fields"] == expected_fields["fields"]


def test_create_geoindex(sys_fabric):
    employees = sys_fabric.collection(TEST_COLLECTION)
    geo_index = employees.add_geo_index(fields=['name', '_key'], ordered=None)
    expected_fields = {"fields": ["name", "_key"]}
    assert geo_index["fields"] == expected_fields["fields"]


def test_insert_data_in_collection(sys_fabric):
    data = [
        {"userId": 1200001, "firstName": "Raleigh", "lastName": "McGilvra"},
        {"userId": 1200002, "firstName": "Marty", "lastName": "Mueller"},
        {"userId": 1200003, "firstName": "Kelby", "lastName": "Mattholie"}
        ]
    if sys_fabric.has_collection(TEST_COLLECTION):
        inputcoll = sys_fabric.collection(TEST_COLLECTION)
        inputcoll.insert_many(data)
        assert inputcoll.count() is 3


def test_get_index(sys_fabric):
    index2 = sys_fabric.collection(TEST_COLLECTION)
    index3 = index2.indexes()
    assert len(index3) is 3


def test_delete_index(sys_fabric):
    employees = sys_fabric.collection(TEST_COLLECTION)
    size = len(employees.indexes())
    while size > 1:
        i = size-1
        size -= 1
        index = employees.indexes()[i]
        print(index)
        employees.delete_index(index['id'])
    assert len(employees.indexes()) is 1


def test_delete_collections(sys_fabric):
    result = sys_fabric.delete_collection(TEST_COLLECTION)
    assert result is True
