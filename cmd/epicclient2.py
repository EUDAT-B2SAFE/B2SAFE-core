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

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

    result = search_execution(client, args.key, args.value)

    sys.stdout.write(result)


def read(args):
    """perform read action"""

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

    if args.key is None:
        result =  read_execution(client, args.handle)
    else:
        result =  read_execution(client, args.handle, args.key)

    sys.stdout.write(result)


def create(args):
    """perform create action"""

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    # create a handle to put. Concate the prefix with a new generated suffix
    prefix = str(credentials.get_prefix())
    uid = uuid.uuid1()
    suffix = str(uid)
    handle = prefix+"/"+suffix

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

    overwrite=False
    result = create_execution(client, handle, args.location, overwrite, args.checksum, args.loc10320, args.extratype)

    sys.stdout.write(result)


def modify(args):
    """perform modify action"""

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

    result = modify_execution(client, args.handle, args.key, args.value)

    sys.stdout.write(result)


def delete(args):
    """perform delete action"""

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

    if args.key is None:
        result =  delete_execution(client, args.handle)
    else:
        result =  delete_execution(client, args.handle, args.key)

    sys.stdout.write(result)


def relation(args):
    """perform the relation action"""

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

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


def bulk(args):
    """perform the bulk actions"""

    try:
        # open input file
        bulk_input_file = open(args.input, "r") 
    except:
        sys.stdout.write('error opening: '+args.input)
        return

    try:
        # open result file
        bulk_result_file = open(args.result, "w") 
    except:
        sys.stdout.write('error opening: '+args.result)
        return

    try:
        # load credentials
        credentials = PIDClientCredentials.load_from_JSON(args.credpath)
    except CredentialsFormatError:
        sys.stdout.write('error')
        return
    except HandleSyntaxError:
        sys.stdout.write('error')
        return

    # retrieve and set extra values
    extra_config = {}

    try:
        # setup connection to handle server
        client = EUDATHandleClient.instantiate_with_credentials(
            credentials,
            **extra_config)
    except HandleNotFoundException:
        sys.stdout.write('error')
        return

    for line in bulk_input_file:
        bulk_array = line.split()

        if bulk_array[0] == 'SEARCH':
            # search key value  # search handle which matches criteria

            search_key = bulk_array[1] 
            search_value = bulk_array[2]
            result = search_execution(client, search_key, search_value)
            bulk_result_file.write('search handle key: '+search_key+' value: '+search_value+' result: '+result+'\n')

        if bulk_array[0] == 'READ':
            # READ handle       # read whole handle
            # READ handle key   # read key/value pair from handle

            read_handle = bulk_array[1] 
            if len(bulk_array) >= 3:
                read_key = bulk_array[2]
                result = read_execution(client, read_handle, read_key)
                bulk_result_file.write('read handle: '+read_handle+' key: '+read_key+' result: '+result+'\n')
            else: 
                result = read_execution(client, read_handle)
                bulk_result_file.write('read handle: '+read_handle+' result: '+result+'\n')

        if bulk_array[0] == 'CREATE':
            # CREATE prefix/uuid URL                       # create handle, use uuid for suffix
            # CREATE prefix/suffix URL                     # create handle, use suffix for handle, no check before if handle exists
            # CREATE prefix/uuid URL CHECKSUM              # create handle, use uuid for suffix, add checksum
            # CREATE prefix/uuid URL CHECKSUM 10320/LOC    # create handle, use uuid for suffix, add checksum, add 10320/LOC
            # CREATE prefix/uuid URL CHECKSUM 10320/LOC EXTRATYPE # create handle, use uuid for suffix, add checksum, add 10320/LOC, add extratypes

            overwrite=False
            checksum = None
            loc10320 = None
            extratype = None

            # create a handle to put. 
            prefix = str(credentials.get_prefix())
            create_prefix = bulk_array[1].split("/")[0]
            create_suffix = bulk_array[1].split("/")[1] 
            if create_suffix == 'uuid':
                uid = uuid.uuid1()
                suffix = str(uid)
                handle = prefix+"/"+suffix
            else:
                handle = prefix+"/"+create_suffix
                overwrite=True

            if len(bulk_array) == 3:
                result = create_execution(client, handle, bulk_array[2], overwrite)
            else:
                if len(bulk_array) >= 4 and bulk_array[3].lower() != 'none':
                    checksum = bulk_array[3]
                if len(bulk_array) >= 5 and bulk_array[4].lower() != 'none':
                    loc10320 = bulk_array[4]
                if len(bulk_array) >= 6 and bulk_array[5].lower() != 'none':
                    extratype = bulk_array[5]
                result = create_execution(client, handle, bulk_array[2], overwrite, checksum, loc10320, extratype)

            bulk_result_file.write('create handle: '+bulk_array[1]+' result: '+result+'\n')

        if bulk_array[0] == 'DELETE':
            # DELETE handle       # delete whole handle
            # DELETE handle key   # delete key/value pair from handle

            delete_handle = bulk_array[1] 
            if len(bulk_array) >= 3:
                delete_key = bulk_array[2]
                result = delete_execution(client, delete_handle, delete_key)
                bulk_result_file.write('delete handle: '+delete_handle+' key: '+delete_key+' result: '+result+'\n')
            else: 
                result = delete_execution(client, delete_handle)
                bulk_result_file.write('delete handle: '+delete_handle+' result: '+result+'\n')

        if bulk_array[0] == 'MODIFY':
            # MODIFY handle key value  # modify key/value pair in handle

            if len(bulk_array) == 4:
                modify_handle = bulk_array[1] 
                modify_key = bulk_array[2]
                modify_value = bulk_array[3]
                result = modify_execution(client, modify_handle, modify_key, modify_value)
                bulk_result_file.write('modify handle: '+modify_handle+' key: '+modify_key+' value: '+modify_value+' result: '+result+'\n')

        if bulk_array[0] == 'REPLACE':
            # REPLACE handle key data1 data2  # replace data1 with data2 in value part of key/value pair in handle

            if len(bulk_array) == 5:
                replace_handle = bulk_array[1] 
                replace_key = bulk_array[2]
                replace_data1 = bulk_array[3]
                replace_data2 = bulk_array[4]
                result = read_execution(client, replace_handle, replace_key)
                if result != "None" and result != 'error':
                    new_value = result.replace(replace_data1, replace_data2)
                    if result != new_value:
                        result = modify_execution(client, replace_handle, replace_key, new_value)
                    else:
                        result = "None"

                bulk_result_file.write('replace handle: '+replace_handle+' key: '+replace_key+' data1: '+replace_data1+' data2: '+replace_data2+' result: '+result+'\n')

    bulk_input_file.close()
    bulk_result_file.close()

###############################################################################
# EPIC Client sub functions
###############################################################################

def search_execution(client, search_key=None, search_value=None):
    """Execute the search action """

    # set default return value
    result = None
    json_result = "None"

    if search_key is not None and search_value is not None:
        try:
            kvpairs = dict([(search_key, str(''.join(search_value)))])
            # search for handle
            result = client.search_handle(**kvpairs)
        except ReverseLookupException:
            result = '{error}'

        json_result = str(json.dumps(result))

        if json_result == '[]':
            json_result = 'empty'
        elif json_result == '{error}':
            json_result = 'error'

    return(json_result)


def read_execution(client, read_handle, read_key=None):
    """Execute the read action """

    # set default return value
    result = None
    json_result = "None"

    if read_key is None:
        try:
            # retrieve whole handle
            result = client.retrieve_handle_record_json(read_handle)
        except HandleSyntaxError:
            json_result = 'error'

        if result is not None:
            json_result = json.dumps(result["values"])
    else:
        try:
            # retrieve single value from a handle
            result = client.get_value_from_handle(read_handle, read_key)
        except HandleNotFoundException:
            json_result = 'None'
        except HandleSyntaxError:
            json_result = 'error'

        if result is not None:
            json_result = json.dumps(result)
            # remove starting and finishing quotes.
            json_result = json_result.lstrip('"')
            json_result = json_result.rstrip('"')

    return(json_result)

def create_execution(client, create_handle, create_location, create_overwrite=False, create_checksum=None, create_loc10320=None, create_extratype=None ):
    """Execute the create action """

    # pre-process the input parameters for the handle api
    extype = {}
    if create_extratype is not None:
        exlist = create_extratype.split(';')
        for item in exlist:
            key = item.split('=')[0]
            value = item.split('=')[1]
            extype[key] = value
    if create_loc10320 is not None:
        l10320 = create_loc10320.split(';')
    else:
        l10320 = None

    # replace "EUDAT/FIO=pid" with "EUDAT/FIO=handle"
    key = 'EUDAT/FIO'
    if key in extype:
        if extype[key].lower() == 'pid':
            extype[key] = create_handle

    # replace "EUDAT/ROR=pid" with "EUDAT/ROR=handle"
    key = 'EUDAT/ROR'
    if key in extype:
        if extype[key].lower() == 'pid':
            extype[key] = create_handle

    result = ''

    try:
        # create the new handle
        result = client.register_handle(
            create_handle,
            location=create_location,
            checksum=create_checksum,
            additional_URLs=l10320,
            overwrite=create_overwrite,
            **extype)
    except HandleAlreadyExistsException:
        result = 'False'
    except HandleAuthenticationError:
        result = 'error'
    except HandleSyntaxError:
        result = 'error'
    except GenericHandleError as ex:
        result = 'error'
    return(result)

def delete_execution(client, delete_handle, delete_key=None):
    """Execute the delete action """

    result = 'True'

    if delete_key is None:
        # delete whole handle
        try:
            client.delete_handle(delete_handle)
        except HandleAuthenticationError:
            result = 'error'
        except HandleNotFoundException:
            result = 'False'
        except HandleSyntaxError:
            result = 'error'
    else:
        # delete value
        try:
            client.delete_handle_value(delete_handle, delete_key)
        except HandleAuthenticationError:
            result = 'error'
        except HandleNotFoundException:
            result = 'False'
        except HandleSyntaxError:
            result = 'error'

    return(result)

def modify_execution(client, modify_handle, modify_key, modify_value):
    """Execute the modify action """

    kvpairs = dict([(modify_key, modify_value)])

    result = 'True'

    try:
        # modify key/value pairs
        client.modify_handle_value(
            modify_handle,
            ttl=None,
            add_if_not_exist=True,
            **kvpairs)
    except HandleAuthenticationError:
        result = 'error'
    except HandleNotFoundException:
        result = 'False'
    except HandleSyntaxError:
        result = 'error'

    return(result)


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
    
    PARSER_BULK = SUBPARSERS.add_parser('bulk',
                                        help='perform bulk actions using '
                                             'an input and result file ')
    PARSER_BULK.add_argument("--input", required=True, help="input file for bulk actions")
    PARSER_BULK.add_argument("--result", required=True, help="output file for bulk actions")
    PARSER_BULK.set_defaults(func=bulk)

    _ARGS = PARSER.parse_args()
    _ARGS.func(_ARGS)
