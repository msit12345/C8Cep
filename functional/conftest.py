import random

from pytest import fixture

from constants import DEMO_PASSWORD
from constants import DEMO_TENANT
from constants import FABRIC1
from constants import GUEST_PASSWORD
from constants import GUEST_TENANT
from constants import ROOT_USER
from constants import SUPER_PASSWORD, SUPER_MAIL
from constants import SUPER_TENANT
from constants import SYSTEM_DB
from constants import TENANT1, TENANT2
from constants import TENANT1_PASS, TENANT2_PASS
from constants import USER1
from constants import USER1_PASS
from constants import GUEST_MAIL, DEMO_MAIL, SUPER_MAIL
from helpers import get_fabric
from helpers import get_tenant


def pytest_addoption(parser):
    parser.addoption("--region", action="store",
                     help="region name where you want to run the tests")


@fixture(scope="module")
def region(request):
    return request.config.getoption("--region")


@fixture(scope="module")
def root_tenant(region):
    yield get_tenant(region, SUPER_MAIL, SUPER_PASSWORD)


@fixture(scope="module")
def root_fabric(root_tenant):
    yield root_tenant.useFabric(SYSTEM_DB)


@fixture(scope="module")
def sys_tenant(region):
    yield get_tenant(region, GUEST_MAIL, GUEST_PASSWORD)


@fixture(scope="module")
def sys_fabric(sys_tenant):
    yield sys_tenant.useFabric(SYSTEM_DB)


@fixture(scope="module")
def guest_fabric(region):
    tennant = get_tenant(region, GUEST_MAIL, GUEST_PASSWORD)
    yield tennant.useFabric(FABRIC1)


@fixture(scope="module")
def demo_tenant(region):
    yield get_tenant(region, DEMO_MAIL, DEMO_PASSWORD)


@fixture(scope="module")
def demo_fabric(demo_tenant):
    yield demo_tenant.useFabric(SYSTEM_DB)


###
@fixture(scope="module")
def demo_fabric_with_db(region):
    yield get_fabric(region, DEMO_MAIL, DEMO_PASSWORD, FABRIC1)


@fixture(scope="module")
def guest_fabric_with_demo(region):
    yield get_fabric(region, DEMO_MAIL, DEMO_PASSWORD, FABRIC1)


@fixture(scope="module")
def user_fabric(region):
    yield get_fabric(region, USER1, USER1_PASS, FABRIC1)


@fixture(scope="module")
def tenant1_fabric(tenant1_tenant):
    yield tenant1_tenant.useFabric(SYSTEM_DB)


@fixture(scope="module")
def tenant1_tenant(region):
    yield get_tenant(region, TENANT1,  TENANT1_PASS)


@fixture(scope="module")
def tenant2_tenant(region):
    yield get_tenant(region, TENANT2,  TENANT2_PASS)


@fixture(scope="module")
def stream_data(region):
    region_name = region.split(".", 1)[0]
    global_random = str(random.randint(1, 1000))
    local_random = str(random.randint(1, 1000))
    global_stream = "{0}_global_stream_{1}".format(region_name, global_random)
    local_stream = "{0}_local_stream_{1}".format(region_name, local_random)
    return {"global_stream": global_stream, "local_stream": local_stream}


@fixture(scope="module")
def sys_dclist(sys_fabric):
    yield sys_fabric.dclist(detail=True)


@fixture(scope="module")
def spot_data():
    return {"new_record": {"name": "john", "count": 0, "_key": "spot"},
            "updated_record": {"name": "john", "count": 1, "_key": "spot"}}


@fixture(scope="module")
def tenant_data():
    return {"_key": "test", "name": "test"}
