import json
import time
import base64
import six

import requests
import sys

from os.path import dirname
from os.path import join

from c8 import C8Client
from c8.exceptions import CollectionListError
from c8.exceptions import FabricListError


from constants import FABRIC1
from constants import GUEST_PASSWORD, GUEST_MAIL
from constants import GUEST_TENANT
from constants import MAX_SLEEP_TIME
from constants import MIN_SLEEP_TIME
from constants import RETRY_NUMTRIES
from constants import RETRY_WAITSECS
from constants import ROOT_USER
from constants import SYSTEM_DB
from constants import PORT
from constants import PROTOCOL


def get_api_url(dc):
    return dc["tags"]["api"]


def get_dc_names(dclist):
    dc_names = []
    for dc in dclist:
        dc_names.append(dc["name"])
    return dc_names


def get_document(fabric, collection_name):
    query = "FOR doc IN %s RETURN doc" % collection_name
    resp = fabric.c8ql.execute(query)
    return resp.batch()


def get_fabric(region, tenant_email, password, fabric_name):
    tenn_obj = get_tenant(region, tenant_email, password)
    return tenn_obj.useFabric(fabric_name)


def get_jwt_token(region, tenant_email, password):
    url = "https://%s/_open/auth" % region
    payload = {"password": password, "email": tenant_email}
    response = requests.post(url, json=payload)
    if response.status_code not in range(200, 210):
        print("URL: %s\nPayload: %s\nMethod: POST" % (url, payload))
        raise RuntimeError("getting token failed with status_code: %s",
                           response.status_code)
    json_data = json.loads(response.text)
    token = json_data["jwt"]
    return token


def get_regions(dclist, which_region):
    regions = []
    for dc in dclist:
        regions.append(get_api_url(dc))
    regions.sort()
    region1, region2, region3 = regions[0], regions[1], regions[2]
    if which_region == "region1":
        return region1
    if which_region == "region2":
        return region2
    if which_region == "region3":
        return region3
    if which_region == "all":
        return [region1, region2, region3]


def get_tenant(region, email, password):
    client = C8Client(host=region, protocol=str(PROTOCOL), port=PORT)
    return client.tenant(email, password)


def load_json_schema(filename):
    relative_path = join("schemas", filename)
    absolute_path = join(dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())


def verify_collection_replicated(dclist, collection_name, tenant_name,
                                 fabric_name, password,
                                 is_creating=True):
    for dc in dclist:
        result = None
        region = get_api_url(dc)
        tenant = get_tenant(region, tenant_name, password)
        fabric = tenant.useFabric(fabric_name)
        for i in range(RETRY_NUMTRIES):
            try:
                result = fabric.has_collection(collection_name)
                if result and is_creating:
                    break
                if not result and not is_creating:
                    break
            except CollectionListError as e:
                print(e.message)
            time.sleep(RETRY_WAITSECS)
        if is_creating:
            message = "Collection not replicated in region %s" % region
        else:
            message = "Collection found in region %s" % region
        assert result is is_creating, message


def verify_document_replicated(dclist, collection_name, document_key,
                               tenant_name, fabric_name, username, password):
    for dc in dclist:
        region = get_api_url(dc)
        tenant = get_tenant(region, tenant_name, password)
        fabric = tenant.useFabric(fabric_name)
        result = None
        for i in range(RETRY_NUMTRIES):
            collection = fabric.collection(collection_name)
            result = collection.get(document_key)
            if result:
                break
            time.sleep(RETRY_WAITSECS)
        message = "Document with key '%s' not found" % document_key
        assert result is not None, message


def verify_fabric_replicated(dclist, fabric_name, is_creating=True,
                             tenant=GUEST_MAIL, password=GUEST_PASSWORD):
    for dc in dclist:
        region = get_api_url(dc)
        fabric = get_fabric(region, tenant, password, SYSTEM_DB)
        for i in range(RETRY_NUMTRIES):
            try:
                result = fabric.has_fabric(fabric_name)
                if result and is_creating:
                    break
                if not result and not is_creating:
                    break
            except FabricListError as e:
                print(e.message)
            time.sleep(RETRY_WAITSECS)
        if is_creating:
            message = "Fabric not replicated in region " + region
        else:
            message = "Fabric found in region " + region
        assert result is is_creating, message



def verify_primary_region(dclist, fabric_name, primary_region, is_none=False):
    for dc in dclist:
        peer_region = get_api_url(dc)
        for i in range(RETRY_NUMTRIES):
            fabric = get_fabric(peer_region, GUEST_MAIL,  GUEST_PASSWORD,
                                fabric_name)
            fabric_details = fabric.properties()
            spot_dc = fabric_details["options"]["spotDc"]
            if spot_dc:
                break
            if not spot_dc and is_none:
                break
            time.sleep(RETRY_WAITSECS)
        assert spot_dc == primary_region