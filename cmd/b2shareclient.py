#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import jsonpatch
import requests
import os
import numpy


class B2shareClient():

    def __init__(self, conf):
        self.configuration = conf

    # Creates a new record, in the draft state in B2SHARE
    # for the collection with a given title,
    # a list of PIDs of the files in the collection
    # for the specified community
    # and with the default values for open_access to be true
    # and no community specific data
    def createDraft(self, community_id, filePIDsString):
        record_id = None
        self.configuration.logger.debug("title: " +
                                        self.configuration.title +
                                        ", community: " +
                                        str(community_id))
        acces_part = self.configuration.access_parameter + \
            "=" + self.configuration.access_token
        create_draft_url = self.configuration.b2share_host_name + \
            self.configuration.records_endpoint + acces_part
        data = '{"titles":[{"title":"' + \
            self.configuration.title + '"}], ' + \
            '"community":"' + community_id + '", ' + \
            '"external_pids":' + filePIDsString + ', ' + \
            '"open_access":true, "community_specific": {}}'
        headers = {"Content-Type": "application/json"}
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: " +
                                           "the method would send: " +
                                           "POST Request with URL: " +
                                           create_draft_url +
                                           "\n headers: " + str(headers) +
                                           "\n data: " + data)
        else:
            try:
                response = requests.post(url=create_draft_url,
                                         headers=headers,
                                         data=data)
                self.configuration.logger.debug(
                    "status code: " + str(response.status_code))
                if ((str(response.status_code) == "200") |
                        (str(response.status_code) == "201")):
                    record_id = response.json()['id']
                    self.configuration.logger.info(
                        "Record created with id: " + record_id)
                else:
                    self.configuration.logger.error("NO record created." +
                                                    "Response: " +
                                                    str(response.json()))
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
        return record_id

    # Patch the draft with extra metadata
    # metadata_file:
    # JSON object from the metadata file = community schema
    # filled by user with data
    def addB2shareMetadata(self, metadata_file):
        acces_part = self.configuration.access_parameter + "=" + \
            self.configuration.access_token
        patch_url = "" + self.configuration.b2share_host_name + \
                    self.configuration.records_endpoint + \
                    self.configuration.record_id + \
                    "/draft" + acces_part
        patch_destination = {}
        with metadata_file.open('r+') as json_file:
            data = json.load(json_file)
            required_options = data["metadata"]["required"]
            optional_options = data["metadata"]["optional"]
            options = required_options + optional_options
            patch_source = {}
            draft_metadata = self.getDraftMetadata()
            for option in options:
                option_value = option["value"]
                if option_value is None or option_value == "":
                    self.configuration.logger.info("Ignored the line " +
                                                option_name +
                                                " with value " +
                                                option_value)
                    continue
                option_name = option["option_name"]
                patch_destination[option_name] = option_value
                if draft_metadata:
                    if option_name in draft_metadata.keys():
                        patch_source[option_name] = draft_metadata[option_name]
                    else:
                        patch_source[option_name] = ''
            if not patch_destination:
                return
            patch = jsonpatch.JsonPatch.from_diff(patch_source, patch_destination)
            headers = {"Content-Type": "application/json-patch+json"}

            if self.configuration.dryrun:
                self.configuration.logger.info("DRYRUN: the method would send: " +
                                                " PATCH Request with URL: " +
                                                patch_url +
                                                "\n headers: " + str(headers) +
                                                "\n data: " + str(patch))
                print("DRYRUN: the method would send: " +
                                                " PATCH Request with URL: " +
                                                patch_url +
                                                "\n headers: " + str(headers) +
                                                "\n data: " + str(patch))
            else:
                try:
                    response = requests.patch(url=patch_url, headers=headers,
                                              data=str(patch))
                    if str(response.status_code) == "200":
                        self.configuration.logger.info(
                            "Adding metadata to the draft " +
                            self.configuration.record_id +
                            " SUCCESSFUL.")
                    else:
                        self.configuration.logger.error(
                            "Adding metadata to the draft " +
                            self.configuration.record_id +
                            " FAILED. Response: " + str(response.json()))
                except requests.exceptions.RequestException as e:
                    self.configuration.logger.error(e)

    def getDraftMetadata(self):
        record_id = self.configuration.record_id
        acces_part = self.configuration.access_parameter + \
            "=" + self.configuration.access_token
        get_draft_metadata = self.configuration.b2share_host_name +\
            self.configuration.records_endpoint + record_id \
            + "/draft" + acces_part
        if self.configuration.dryrun:
            self.configuration.logger.info(
                "DRYRUN: the method would send: GET Request with URL: " +
                get_draft_metadata)
            print("DRYRUN: the method would send: GET Request with URL: " +
                  get_draft_metadata)
        else:
            try:
                response = requests.get(url=get_draft_metadata)
                self.configuration.logger.debug(
                    "Get Draft md status code: " + str(response.status_code))
                if str(response.status_code) == "200":
                    return response.json()["metadata"]
                else:
                    self.configuration.logger.error(
                        "Request for draft metadata failed. URL: " +
                        get_draft_metadata)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
            return None

    # compare every md option between metadata_file and draft_metadata
    def compareMD(self, metadata_file):
        draft_metadata = self.getDraftMetadata()
        with metadata_file.open('r+') as json_file:
            data = json.load(json_file)
            required_options = data["metadata"]["required"]
            optional_options = data["metadata"]["optional"]
            options = required_options + optional_options
            for option in options:
                md_name = option["option_name"]
                md_value = option["value"]
                if md_value !='':
                    if md_name in draft_metadata.keys():
                        draft_value = draft_metadata[md_name]
                        if md_value != draft_value:
                            self.configuration.logger.info("Meta data in collection and draft are NOT equal")
                            return False
                    else:
                        self.configuration.logger.info("Meta data in collection and draft are NOT equal")
                        return False
        self.configuration.logger.info("Meta data in collection and draft are equal")
        return True

    def publishRecord(self):
        record_id = self.configuration.record_id
        acces_part = self.configuration.access_parameter + \
            "=" + self.configuration.access_token
        publish_record_url = self.configuration.b2share_host_name +\
            self.configuration.records_endpoint + record_id +\
            "/draft" + acces_part
        patch = \
            '[{"op":"add", "path":"/publication_state", "value":"submitted"}]'
        headers = {"Content-Type": "application/json-patch+json"}
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send:" +
                                           " PATCH Request with URL: " +
                                           publish_record_url +
                                           "\n headers: " + str(headers) +
                                           "\n data: " + str(patch))
        else:
            try:
                response = requests.patch(url=publish_record_url,
                                          headers=headers,
                                          data=patch)
                return response
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
                return None

    # TODO add the function Get iRODS metadata
    def getB2safeMetadata(self):
        """Get system metadata"""
        return None

    def getCommunitySchema(self, community_id):
        community_endpoint = self.configuration.list_communities_endpoint
        get_schema_endpoint = self.configuration.get_community_schema_endpoint
        acces_part = self.configuration.access_parameter + \
            "=" + self.configuration.access_token
        get_community_schema_url = self.configuration.b2share_host_name +\
            community_endpoint + \
            community_id + \
            get_schema_endpoint + acces_part
        community_schema = None
        if self.configuration.dryrun:
            self.configuration.logger.info(
                "DRYRUN: the method would send: GET Request with URL: " +
                get_community_schema_url)
        else:
            try:
                # Add 'verify=False',
                # if B2SHARE server has no proper certificate
                response = requests.get(url=get_community_schema_url)
                self.configuration.logger.debug(response.text)
                if str(response.status_code) == "200":
                    community_schema = response.text
                else:
                    self.configuration.logger.error(
                        "Request for community schema failed. Response: " +
                        str(response.json()))
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
        return community_schema

    def getDraftByID(self):
        draft_id = self.configuration.record_id
        acces_part = self.configuration.access_parameter + \
                     "=" + self.configuration.access_token
        get_draft_url = self.configuration.b2share_host_name + \
            self.configuration.records_endpoint + draft_id + \
            "/draft" + acces_part
        draft = None
        if self.configuration.dryrun:
            print(get_draft_url)
            self.configuration.logger.info(
                "DRYRUN: the method would send: GET Request with URL: " +
                get_draft_url)
        else:
            try:
                response = requests.get(url=get_draft_url)
                if str(response.status_code) == "200":
                    self.configuration.logger.info(
                        "Request for a draft with id " + draft_id +
                        " SUCCESSFUL.")
                    draft = response.text
                else:
                    self.configuration.logger.error(
                        "Request for a draft with id " + draft_id +
                        " FAILED. Response: " + str(response.json()))
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
        return draft

    def deleteDraft(self):
        draft_id = self.configuration.record_id
        acces_part = self.configuration.access_parameter + \
            "=" + self.configuration.access_token
        delete_draft_url = self.configuration.b2share_host_name + \
            self.configuration.records_endpoint + \
            draft_id + "/draft" + acces_part
        headers = {"Content-Type": "application/json"}
        if self.configuration.dryrun:
            self.configuration.logger.info(
                "DRYRUN: the method would send: DELETE Request with URL: " +
                delete_draft_url)
        else:
            try:
                response = requests.delete(
                    url=delete_draft_url, headers=headers)
                if str(response.status_code) == "204":
                    self.configuration.logger.info(
                        "Draft with id " + draft_id + " DELETED.")
                else:
                    self.configuration.logger.error(
                        "Deleting draft with id " + draft_id +
                        " FAILED. Response: " + str(response.json()))
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
                self.configuration.logger.error(
                    "Deleting draft with id " + draft_id +
                    " FAILED. Response: " + str(response.json()))

    def getAllCommunities(self):
        host = self.configuration.b2share_host_name
        endpoint = self.configuration.list_communities_endpoint
        acces_part = self.configuration.access_parameter + \
            "=" + self.configuration.access_token
        list_communities_url = host + endpoint + acces_part
        communities = {}
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send:" +
                                           " GET Request with URL: " +
                                           list_communities_url)
        else:
            try:
                response = requests.get(url=list_communities_url)
                if str(response.status_code) == "200":
                    communities_list = response.json()["hits"]["hits"]
                    for community_object in communities_list:
                        name = community_object["name"]
                        community_id = community_object["id"]
                        communities[name] = community_id
                else:
                    self.configuration.logger.error(response.text)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
        return communities
