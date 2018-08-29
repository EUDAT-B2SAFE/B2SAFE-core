## Testing Guidelines for EPIC Client, EPIC client 2, log, auth, iRODS, b2SAFE

The suite can test following parts:
* epicclient.py unit and integration test
* epicclient2.py integration test
* log
* auth
* iRODS integration test on live installation
* b2safe integration test on live installation

The suite of unit and integration test cases for all parts uses the standard testing framework, i.e. `unittest`, aka “PyUnit”, the Python version of JUnit.

* Unit tests use `unittest.mock` to mock EPIC REST API calls.
* EPIC Integration tests require a valid credentials file (otherwise test suite will be skipped):
  * filename: `epic_credentials` (see [example](resources/epic_credentials_example))
  * location: under `resources` directory 
* EPIC2 Integration tests require a valid credentials file (otherwise test suite will be skipped):
  * filename: `epic2_credentials`
  * location: under `resources` directory 
* iRODS Integration tests require a `~/.irods/irods_environment.json` with at least:
```
    irods_default_hash_scheme
    irods_default_resource
    irods_home
    irods_user_name
    irods_zone_name
```
* b2safe Integration test require a `~/.irods/irods_environment.json` with at least:
```
    irods_default_hash_scheme
    irods_default_resource
    irods_home
    irods_user_name
    irods_zone_name
```

### Requirements

Dependencies for Python 2.7 are listed in `requirements.txt`. Earlier versions of Python have also been tested (e.g. see `requirements26.txt` for Python 2.6). In order to install required modules, use your distribution's package manager or `pip` (recommended) as follows:

    pip install -r requirements.txt

### Usage

    python testB2SafeCmd.py --help
    python testB2SafeCmd.py -test epic
    python testB2SafeCmd.py -test epic2
    python testB2SafeCmd.py -test irods
    python testB2SafeCmd.py -test b2safe

### Test coverage

Assuming `coverage` module is installed:

    python -m coverage run testB2SafeCmd.py -test epic && python -m coverage xml

This will run all unit & integration tests and create an xml-formatted coverage report suitable for Jenkins/SonarQube

### Known Issues

* Tests in `testB2SafeCmd.epicclitest.EpicClientCLITestCase` fail with `AttributeError: assert_called_once`: The current workaround is to use `mock` version 1.0.1 (see `requirements.txt`).
