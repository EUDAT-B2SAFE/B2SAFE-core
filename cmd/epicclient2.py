#!/usr/bin/env python
#
# epicclient.py
#
# * use 4 spaces!!! not tabs
# * set tabstop=4
# * set expandtab
# * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
# * use pylint
#

"""EUDAT EPIC client API. Supports reading, querying, creating, modifying and
deleting handle records.
"""
from b2handle.handleclient import EUDATHandleClient
from b2handle.clientcredentials import PIDClientCredentials
from b2handle.handleexceptions import *
import uuid
import argparse
import sys
import json

###############################################################################
# EPIC Client Command Line Interface #
###############################################################################

def search(args):
    """perform search action"""

    # load credentials
    credentials = PIDClientCredentials.load_from_JSON(args.credpath)

    # retrieve and set extra values
    extra_config = {}

    # setup connection to handle server
    client = EUDATHandleClient.instantiate_with_credentials(
        credentials,
        **extra_config)

    kvpairs = dict([(args.key, str(''.join(args.value)))])

    try:
        # search for handle
        result = client.search_handle(**kvpairs)
    except ReverseLookupException:
        result = '{error}'

    json_result = str(json.dumps(result))

    if json_result == '[]':
        json_result = 'empty'
    elif json_result == '{error}':
        json_result = 'error'

    sys.stdout.write(json_result)


def read(args):
    """perform read action"""

    # load credentials
    credentials = PIDClientCredentials.load_from_JSON(args.credpath)

    # retrieve and set extra values
    extra_config = {}

    # setup connection to handle server
    client = EUDATHandleClient.instantiate_with_credentials(
        credentials,
        **extra_config)

    # set default return value
    json_result = "None"

    if args.key is None:
        try:
            # retrieve whole handle
            result = client.retrieve_handle_record_json(args.handle)
        except HandleSyntaxError:
            json_result = 'error'

        if result is not None:
           json_result = json.dumps(result["values"])
    else:
        try:
            # retrieve single value from a handle
            result = client.get_value_from_handle(args.handle, args.key)
        except HandleSyntaxError:
            json_result = 'error'

        if result is not None:
            json_result = json.dumps(result)
            # remove starting and finishing quotes.
            json_result = json_result.lstrip('"')
            json_result = json_result.rstrip('"')

    sys.stdout.write(json_result)


def create(args):
    """perform create action"""

    # load credentials
    credentials = PIDClientCredentials.load_from_JSON(args.credpath)

    # retrieve and set extra values
    extra_config = {}

    # create a handle to put. Concate the prefix with a new generated suffix
    prefix = str(credentials.get_prefix())
    uid = uuid.uuid1()
    suffix = str(uid)
    handle = prefix+"/"+suffix

    # setup connection to handle server
    client = EUDATHandleClient.instantiate_with_credentials(
        credentials,
        **extra_config)

    # pre-process the input parameters for the handle api
    extype = {}
    if args.extratype is not None:
        exlist = args.extratype.split(';')
        for item in exlist:
            key = item.split('=')[0]
            extype[key] = item.split('=')[1]
    if args.loc10320 is not None:
        l10320 = args.loc10320.split(';')
    else:
        l10320 = None

    result = ''

    try:
        # create the new handle
        result = client.register_handle(
            handle,
            location=args.location,
            checksum=args.checksum,
            additional_URLs=l10320,
            overwrite=False,
            **extype)
    except HandleAlreadyExistsException:
        result = 'False'
    except HandleAuthenticationError:
        result = 'error'
    except HandleSyntaxError:
        result = 'error'

    sys.stdout.write(result)


def modify(args):
    """perform modify action"""

    # load credentials
    credentials = PIDClientCredentials.load_from_JSON(args.credpath)

    # retrieve and set extra values
    extra_config = {}

    # setup connection to handle server
    client = EUDATHandleClient.instantiate_with_credentials(
        credentials,
        **extra_config)

    kvpairs = dict([(args.key, args.value)])

    result = 'True'

    try:
        # modify key/value pairs
        client.modify_handle_value(
            args.handle,
            ttl=None,
            add_if_not_exist=True,
            **kvpairs)
    except HandleAuthenticationError:
        result = 'error'
    except HandleNotFoundException:
        result = 'False'
    except HandleSyntaxError:
        result = 'error'

    sys.stdout.write(result)


def delete(args):
    """perform delete action"""

    # load credentials
    credentials = PIDClientCredentials.load_from_JSON(args.credpath)

    # retrieve and set extra values
    extra_config = {}

    # setup connection to handle server
    client = EUDATHandleClient.instantiate_with_credentials(
        credentials,
        **extra_config)

    result = 'True'

    if args.key is None:
        # delete whole handle
	try:
            client.delete_handle(args.handle)
        except HandleAuthenticationError:
            result = 'error'
        except HandleNotFoundException:
            result = 'False'
        except HandleSyntaxError:
            result = 'error'
    else:
        # delete value
        try:
            client.delete_handle_value(args.handle, args.key)
        except HandleAuthenticationError:
            result = 'error'
        except HandleNotFoundException:
            result = 'False'
        except HandleSyntaxError:
            result = 'error'

    sys.stdout.write(result)


def relation(args):
    """perform the relation action"""

    # load credentials
    credentials = PIDClientCredentials.load_from_JSON(args.credpath)

    # retrieve and set extra values
    extra_config = {}

    # setup connection to handle server
    client = EUDATHandleClient.instantiate_with_credentials(
        credentials,
        **extra_config)

    result = 'None'

    # add relation to 10320/LOC
    try:
        client.add_additional_URL(args.ppid, args.cpid)
    except HandleAuthenticationError:
        result = 'error'
    except HandleNotFoundException:
        result = 'False'
    except HandleSyntaxError:
        result = 'error'

    sys.stdout.write(result)


###############################################################################
# EPIC Client main body #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='EUDAT EPIC client API. '
                                                 'Supports reading, querying,'
                                                 ' creating, modifying and '
                                                 'deleting handle records.')
    PARSER.add_argument("credstore", choices=['os', 'irods'], default="NULL",
                        help="the used credential storage "
                             "(os=filespace, irods=iRODS storage)")
    PARSER.add_argument("credpath", default="NULL",
                        help="path to the credentials")

    SUBPARSERS = PARSER.add_subparsers(title='Actions',
                                       description='Handle record management'
                                                   'actions',
                                       help='additional help')

    PARSER_CREATE = SUBPARSERS.add_parser('create',
                                          help='creating handle records')
    PARSER_CREATE.add_argument("location", help="location to store in "
                                                "the new handle record")
    PARSER_CREATE.add_argument("--checksum", help="checksum to store in "
                                                  "the new handle record")
    PARSER_CREATE.add_argument("--extratype", help="Extension create fields \
                               EUDAT/ROR and EUDAT/PPID \
                               in format: \"EUDAT/ROR=xyz;EUDAT/PPID=abc\"")
    PARSER_CREATE.add_argument("--loc10320", help="Extension field 10320/LOC \
                               in format: \"location1;location2;location3\"")
    PARSER_CREATE.set_defaults(func=create)

    PARSER_MODIFY = SUBPARSERS.add_parser('modify',
                                          help='modifying handle records')
    PARSER_MODIFY.add_argument("handle", help="the handle value")
    PARSER_MODIFY.add_argument("key", help="the key of the field to change "
                                           "in the pid record")
    PARSER_MODIFY.add_argument("value", help="the new value to store "
                                             "in the pid record identified "
                                             "with the supplied key")
    PARSER_MODIFY.set_defaults(func=modify)

    PARSER_DELETE = SUBPARSERS.add_parser('delete',
                                          help='Deleting handle records or '
                                               'handle field')
    PARSER_DELETE.add_argument("handle",
                               help="the handle value of the digital object "
                                    "instance to delete")
    PARSER_DELETE.add_argument("--key",
                               help="the key-field of handle, field == '' in "
                                    "case delete complete handle ")
    PARSER_DELETE.set_defaults(func=delete)

    PARSER_READ = SUBPARSERS.add_parser('read', help='Read handle record')
    PARSER_READ.add_argument("handle", help="the handle value")
    PARSER_READ.add_argument("--key", help="only read this key instead of "
                                           "the full handle record")
    PARSER_READ.set_defaults(func=read)

    PARSER_SEARCH = SUBPARSERS.add_parser('search',
                                          help='Search for handle records')
    PARSER_SEARCH.add_argument("key", choices=['URL', 'CHECKSUM'],
                               help="the key to search")
    PARSER_SEARCH.add_argument("value", nargs='+', help="the value to search")
    PARSER_SEARCH.set_defaults(func=search)

    PARSER_RELATION = SUBPARSERS.add_parser('relation',
                                            help='Add a (parent,child) '
                                                 'relationship between '
                                                 'the specified handle '
                                                 'records')
    PARSER_RELATION.add_argument("ppid", help="parent handle value")
    PARSER_RELATION.add_argument("cpid", help="child handle value")
    PARSER_RELATION.set_defaults(func=relation)

    _ARGS = PARSER.parse_args()
    _ARGS.func(_ARGS)
