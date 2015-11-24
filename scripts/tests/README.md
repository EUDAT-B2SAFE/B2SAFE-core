## Testing Guidelines for EPIC Client

The suite of unit and integration test cases for the EPIC Client uses the standard testing framework, i.e. `unittest`, aka “PyUnit”, the Python version of JUnit.

* Unit tests use `unittest.mock` to mock EPIC REST API calls.
* Integrations tests require a valid credentials file (otherwise test suite will be skipped):
  * filename: `epic_credentials` (see [example](resources/epic_credentials_example))
  * location: under `resources` directory 

### Requirements

Dependencies for Python 2.7 are listed in `requirements.txt`. Earlier versions of Python have also been tested (e.g. see `requirements26.txt` for Python 2.6). In order to install required modules, use your distribution's package manager or `pip` (recommended) as follows:

    pip install -r requirements.txt

### Usage

    python testB2SafeCmd.py -test epic

### Test coverage

Assuming `coverage` module is installed:

    python -m coverage run testB2SafeCmd.py -test epic && python -m coverage xml

This will run all EPIC Client unit & integration tests and create an xml-formatted coverage report suitable for Jenkins/SonarQube

### Known Issues

* Tests in `testB2SafeCmd.epicclitest.EpicClientCLITestCase` fail with `AttributeError: assert_called_once`: The current workaround is to use `mock` version 1.0.1 (see `requirements.txt`).
