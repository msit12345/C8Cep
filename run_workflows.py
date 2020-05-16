import os
import sys
import yaml

from texttable import Texttable

inputs = yaml.load(open("functional_workflows.yaml"), Loader=yaml.FullLoader)
federation_url = inputs["federation"]["url"]

if federation_url == "default.dev.aws.macrometa.io":
    print("Not executing the script as default url has been provided")
    sys.exit(0)
else:
    print("running tests against the federation = %s" % federation_url)

statuscode = 0
workflowresults = Texttable()
summary = Texttable()
failed = 0
passed = 0

if inputs["diagnostics"]["enable"]:
    print("component: diagnostics tests executing")
    os.chdir("diagnostics")
    # os.system("sudo pip3 install -r requirements.txt")
    exitcode = os.system("python diagnostics.py -host %s -t diagnostics" %
                         federation_url)
    statuscode = exitcode or statuscode
    if exitcode != 0:
        workflowresults.add_rows([["Workflow", "Result"],
                                  ["diagnostics", "fail"]])
        failed = failed + 1
    else:
        workflowresults.add_rows([["Workflow", "Result"],
                                  ["diagnostics", "pass"]])
        passed = passed + 1
    os.chdir("../")

if inputs["functional"]["enable"]:
    print("Installing pyc8")
    os.system("sudo pip3 install -U pyc8==0.15.4 -q")
    os.chdir("functional")
    test_markers = inputs["functional"]["test-suite"]
    test_suites = []
    if test_markers is not None and "," in test_markers:
        test_suites = test_markers.split(",")
        test_suites = [x.replace(" ", "") for x in test_suites]
    else:
        test_suites = test_markers
    markers = None
    if test_suites is not None:
        if type(test_suites) is list and len(test_suites) > 1:
            markers = '"-m {}"'.format(" or ".join(test_suites))
        else:
            markers = '"-m {}"'.format(test_suites)
    if markers is not None:
        cmd = "py.test -sv --disable-pytest-warnings {}\
                --region={}".format(markers, federation_url)
    else:
        cmd = "py.test -sv --disable-pytest-warnings\
                --region={}".format(federation_url)
    exitcode = os.system(cmd)
    statuscode = exitcode or statuscode
    if exitcode != 0:
        workflowresults.add_rows([["Workflow", "Result"],
                                  ["functional", "fail"]])
        failed = failed + 1
    else:
        workflowresults.add_rows([["Workflow", "Result"],
                                  ["functional", "pass"]])
        passed = passed + 1
    os.chdir("../")

print("\nSUMMARY")
print(workflowresults.draw())
summary.add_rows([["executed", "passed", "failed"],
                  [passed + failed, passed, failed]])
print(summary.draw())

sys.exit(1 if statuscode else 0)
