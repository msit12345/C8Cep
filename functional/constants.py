import yaml
import os

DEMO_TENANT = "demo"
DEMO_PASSWORD = "demo"
GUEST_TENANT = "guest"
GUEST_PASSWORD = "guest"
SUPER_TENANT = "_mm"
SUPER_PASSWORD = "Macrometa123!@#"
SYSTEM_DB = "_system"
ROOT_USER = "root"

SUPER_MAIL = "mm@macrometa.io"
GUEST_MAIL = "guest@macrometa.io"
DEMO_MAIL = "demo@macrometa.io"

FABRIC1 = "fabric1"
SEEDDATA_KEY = "test"
SPOT_COLLECTION_NAME = "spotCollection"
TEST_COLLECTION = "employees"
TESTGRAPH = "transactions"
USER1 = "smokeuser1@macrometa.io"
USER1_PASS = "user1"
USER2 = "smokeuser2@macrometa.io"
USER2_PASS = "user2"
TENANT1 = "smoketenant1@macrometa.io"
TENANT1_PASS = "tenant1"
TENANT2 = "smoketenant2@macrometa.io"
TENANT2_PASS = "tenant2"
QUERY_NAME = "smoketestquery"

MIN_SLEEP_TIME = 5
MAX_SLEEP_TIME = 10
RETRY_NUMTRIES = 15
RETRY_WAITSECS = 6

WORKFLOW_FILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "functional_workflows.yaml"))
with open(WORKFLOW_FILE_PATH, 'r') as f:
    doc = yaml.load(f)
    PORT = doc["port"]
    PROTOCOL = doc["protocol"]
