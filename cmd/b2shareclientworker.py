#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import json
import jsonpatch
import requests

class B2shareClient():

    def __init__(self, conf):
        self.configuration = conf
    
    # Creates a new record, in the draft state in B2SHARE for the collection with
    # a given title,
    # a list of PIDs of the files in the collection
    # for the specified community
    # and with the default values for open_access to be true and no community specific data
    def createDraft(self, community_id, title, filePIDsString):
        record_id = None
        if community_id and filePIDsString:
            self.configuration.logger.debug("title: " + str(title) + \
                                            ", token: " + self.configuration.access_token \
                                            + ", community: " + str(community_id))
            acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
            create_draft_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + acces_part
            data = '{"titles":[{"title":"' + title + '"}], ' + \
                   '"community":"' + community_id + '", ' + \
				   '"external_pids":' + filePIDsString + ', ' + \
                   '"open_access":true, "community_specific": {}}'
            headers = {"Content-Type":"application/json"}
            if self.configuration.dryrun:
                self.configuration.logger.info("DRYRUN: the method would send: POST Request with URL: " + create_draft_url \
                                                            + "\n headers: "+ str(headers) \
                                                            + "\n data: " + data)
            else:
                try:
                    #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                    response = requests.post(url=create_draft_url, headers=headers, data=data, verify=False)
                    self.configuration.logger.debug("status code: " + str(response.status_code))
                    if (str(response.status_code) == "200") | (str(response.status_code) == "201"): 
                        record_id = response.json()['id']
                        self.configuration.logger.info("Record created with id: " + record_id)
                    else:
                        self.configuration.logger.error("NO record created: " + str(response.json()))
                except requests.exceptions.RequestException as e:
                    self.configuration.logger.error(e)
        return record_id

    # Patch the draft with extra metadata
    # metadata_file: JSON object from the metadata file = community schema filled by user with data
    def addB2shareMetadata(self, record_id, metadata_file):
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        patch_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                    + "/draft" + acces_part
        
        metadata_lines = metadata_file.split('\n\n')
        patch_source = {}
        patch_destination = {}
        
        #ignore first line as it is a comment
        for line in metadata_lines[1:]:
            option_value_line = line.split('\n')
            if not self.isLineContainingValue(option_value_line):
                continue
            option_name = option_value_line[0]
            if option_name == 'community' or option_name == '' or option_name == 'titles':
                self.configuration.logger.info("Ignore the line " + option_name + \
                                               " with value " + option_value_line[1])
                continue
            draft_metadata = self.getDraftMetadata(record_id)
            if draft_metadata:
                if option_name in draft_metadata.keys():
                    # add or replace the existing values in the draft record
                    # replace: patch_source[option_name] = draft_metadata[option_name]
                    # add: 
                    patch_source[option_name] = ''
            option_value = option_value_line[1]
            if self.isArray(option_value): 
                option_value = self.patchArrayFrom(option_value)
            elif self.isObject(option_value): 
                option_value = self.toJsonObject(option_value)
            elif self.isBoolean(option_value):
                option_value = self.valueToBoolean(option_value)   
            else:
                # value is a string
                option_value = option_value
            patch_destination[option_name] = option_value
        
        patch = jsonpatch.make_patch(patch_source, patch_destination)
        headers = {"Content-Type": "application/json-patch+json"}
        
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: PATCH Request with URL: " + patch_url \
                                                            + "\n headers: "+ str(headers) \
                                                            + "\n data: " + str(patch))
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.patch(url=patch_url, headers=headers, data=str(patch), verify=False)
                if str(response.status_code) == "200":
                    self.configuration.logger.info("Adding metadata to the draft " + record_id + " SUCCESSFUL.")
                else:
                    self.configuration.logger.error("Adding metadata to the draft " + record_id + " FAILED. " + \
                                                "\n response: " + response.text)
            except requests.exceptions.RequestException as e:
                    self.configuration.logger.error(e)
    
    def patchArrayFrom(self, option_value):
        option_value = option_value.replace('[','').replace(']','')
        if self.isObjectsArray(option_value):
            array_of_objects = self.objectsArrayFrom(option_value)
            return array_of_objects
        else:
            strings_array = self.strigsArrayFrom(option_value)
            return strings_array
    
    def strigsArrayFrom(self, option_value):
        strings_array = []
        for string_value in option_value.split(','):
            strings_array.append(string_value.strip())
        return strings_array
    
    def objectsArrayFrom(self, value):
        values_array = []
        if '},' in value:
            #many objects in array
            delimiter = '}'
            arr = value.split(delimiter)
            values_array.append(arr[0]+'}')
            for elem in value.split(delimiter)[1:]:
                values_array.append(elem[1:].strip()+'}')
        else:
            #one element in array
            values_array.append(value)
        array_of_objects = []
        for array_element in values_array:
            if '{' in array_element:
                array_of_objects.append(self.toJsonObject(array_element))
        return array_of_objects
    
    def toJsonObject(self, value):
        v = json.loads(value)
        return v
    
    def getDraftMetadata(self, record_id):
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        get_draft_metadata = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                    + "/draft" + acces_part
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: GET Request with URL: " + get_draft_metadata)
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.get(url=get_draft_metadata, verify=False)
                self.configuration.logger.debug("status code: " + str(response.status_code))
                if str(response.status_code) == "200":
                    return response.json()["metadata"]
                else:
                    self.configuration.logger.error("Request for draft metadata failed. URL: "+get_draft_metadata + \
                                                    "\n response: " + response.text)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
            return None
    
    def publishRecord(self, record_id):
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        publish_record_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + record_id \
                             + "/draft" + acces_part
        patch = '[{"op":"add", "path":"/publication_state", "value":"submitted"}]'
        headers = {"Content-Type": "application/json-patch+json"}
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: PATCH Request with URL: " + publish_record_url \
                                                            + "\n headers: "+ str(headers) \
                                                            + "\n data: " + str(patch))
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.patch(url=publish_record_url, headers=headers, data=patch, verify=False)
                if str(response.status_code) == "200":
                    self.configuration.logger.info("Publishing SUCCESSFUL. " + str(response.text))
                else:
                    self.configuration.logger.error("Publishing FAILED. " + \
                                                    "\n response: " + response.text)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
                self.configuration.logger.error("Publishing FAILED. ")
        
    
    def valueToBoolean(self, option_value):
        if option_value.lower() == "true":
            return True
        if option_value.lower() == "false":
            return False
    
    def isBoolean(self, option_value):
        return ((option_value.lower() == "true") | (option_value.lower() == "false"))
    
    def isObject(self, option_value):
        return option_value.startswith('{')
    
    def isObjectsArray(self, option_value):
        return option_value.startswith('{')
    
    def isArray(self, option_value):
        return option_value.startswith('[')
    
    def isLineContainingValue(self, line_content):
        return len(line_content) == 2
    
    #TODO add the function Get iRODS metadata
    def getB2safeMetadata(self):
        """Get system metadata"""
        return None
    
    def getCommunitySchema(self, community_id):
        community_endpoint = self.configuration.list_communities_endpoint
        get_schema_endpoint = self.configuration.get_community_schema_endpoint
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token        
        get_community_schema_url = self.configuration.b2share_host_name + community_endpoint\
                                   + community_id + get_schema_endpoint + acces_part
        community_schema = None
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: GET Request with URL: " + get_community_schema_url)
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.get(url=get_community_schema_url, verify=False)
                self.configuration.logger.debug(response.text)
                if str(response.status_code) == "200":
                    community_schema = response.text
                else:
                    self.configuration.logger.error("Request for community schema failed. " + \
                                                    "\n response: " + response.text)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
        return community_schema
    
    def getDraftByID(self, draft_id):
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        get_draft_url = self.configuration.b2share_host_name + 'records/' + draft_id + "/draft" + acces_part
        draft = None
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: GET Request with URL: " + get_draft_url)
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.get(url=get_draft_url,  verify=False)
                if str(response.status_code) == "200":
                    self.configuration.logger.info("Request for a draft with id " + draft_id + " SUCCESSFUL.")
                    draft = response.text
                else:
                    self.configuration.logger.error("Request for a draft with id " + draft_id + " FAILED. " + \
                                                    "\n response: " + response.text)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
        return draft
    
    def deleteDraft(self, draft_id):
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        delete_draft_url = self.configuration.b2share_host_name + self.configuration.records_endpoint + \
                            draft_id + "/draft" + acces_part
        headers = {"Content-Type": "application/json"}
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: DELETE Request with URL: " + delete_draft_url)
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.delete(url=delete_draft_url, headers=headers, verify=False)
                if str(response.status_code) == "204":
                    self.configuration.logger.info("Draft with id " + draft_id + " DELETED.")
                else:
                    self.configuration.logger.error("Deleting draft with id " + draft_id + " FAILED. " + \
                                                    "\n response: " + response.text)
            except requests.exceptions.RequestException as e:
                self.configuration.logger.error(e)
                self.configuration.logger.error("Deleting draft with id " + draft_id + " FAILED. ")
    
    def getAllCommunities(self):       
        host = self.configuration.b2share_host_name
        endpoint = self.configuration.list_communities_endpoint
        acces_part = self.configuration.access_parameter + "=" + self.configuration.access_token
        list_communities_url = host + endpoint + acces_part
        communities = {}
        if self.configuration.dryrun:
            self.configuration.logger.info("DRYRUN: the method would send: GET Request with URL: " + list_communities_url)
        else:
            try:
                #TODO: delete 'verify=False', if B2SHARE server has proper certificate
                response = requests.get(url=list_communities_url, verify=False)
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
    