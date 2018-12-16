#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import unittest
from mock import MagicMock, patch
import json
import sys

import logging
test_logger = logging.getLogger('B2shareClientTest')  

sys.path.append("../../cmd") 
from b2shareclientworker import B2shareClient

class B2shareClientTest(unittest.TestCase):
    def setUp(self):
        # mock configuration
        # TODO: change "confpath" to variable from call of the test or in the test suite
        self.configurationMock = MagicMock(confpath = "/home/irods/B2SAFE-core/conf/b2safe_b2share.conf", 
                                      b2share_host_name = 'https://trng-b2share.eudat.eu/api', 
                                      list_communities_endpoint = '/communities',
                                      access_parameter = '/?access_token=',
                                      access_token = 'JFSUcYzTRpMdVCEyAk3mmtGcfpmH',
                                      dryrun = False,
                                      debug = True,
                                      logger = test_logger)
        self.b2shcl = B2shareClient(self.configurationMock)
        self.draft_id_mock = "734c8cf3bb4f42cca0e9c4c3cf3cc86b"
        self.community_id_mock = "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095"
        self.filePIDsString_mock = '[{"ePIC_PID": "http://hdl.handle.net/20.500.11946/5db21a88-e0d8-11e7-9eab-0050569e7581","key": "copytest.txt"},{"ePIC_PID": "http://hdl.handle.net/20.500.11946/619416e2-e0d8-11e7-8ca4-0050569e7581","key": "metatest2.txt"}]'
        self.metadata_file_mock = ''
        # TODO: change to variable from call of the test or in the test suite
        filled_md_file_path = '/home/irods/B2SAFE-core/conf/b2share_metadata.json'
        with open(filled_md_file_path, 'r') as metadata_file:
            self.metadata_file_mock = metadata_file.read()
        self.title_mock = "TestDraftTitle"
        pass
    
    def tearDown(self):
        logging.shutdown()
        pass
    
    
    def testGetAllCommunities(self):
        mock_get_patcher = patch('b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.json.return_value = json.loads('{"hits": {"hits": [{"created": "Wed, 21 Dec 2016 08:57:40 GMT", "description": "Aalto University", "id": "c4234f93-da96-4d2f-a2c8-fa83d0775212", "name": "Aalto"}]}}')
        mock_get.return_value.status_code = 200
        
        b2shcl = B2shareClient(self.configurationMock)
        communities = b2shcl.getAllCommunities()
        
        mock_get_patcher.stop()
        
        self.assertTrue(bool(communities))
        
    def testDeleteDraft(self):
        mock_get_patcher = patch('b2shareclient.requests.delete')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 204
        
        b2shcl = B2shareClient(self.configurationMock)
        b2shcl.deleteDraft(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(True)
        
    def testGetDraftByID(self):
        mock_get_patcher = patch('b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "response text mock"
        
        b2shcl = B2shareClient(self.configurationMock)
        draft = b2shcl.getDraftByID(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(bool(draft))
        
    def testgGetCommunitySchema(self):
        mock_get_patcher = patch('b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "response text mock"
        
        b2shcl = B2shareClient(self.configurationMock)
        community_schema = b2shcl.getCommunitySchema(self.community_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(bool(community_schema))
      
    def testPublishRecord(self):
        mock_get_patcher = patch('b2shareclient.requests.patch')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "response text mock"
        
        b2shcl = B2shareClient(self.configurationMock)
        b2shcl.publishRecord(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(True)
        
    def testGetDraftMetadata(self):
        mock_get_patcher = patch('b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads('{"metadata":{"$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema", "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095", "community_specific": {}, "external_pids": [{"ePIC_PID": "http://hdl.handle.net/20.500.11946/5db21a88-e0d8-11e7-9eab-0050569e7581","key": "copytest.txt"},{"ePIC_PID": "http://hdl.handle.net/20.500.11946/60fb7360-e0d8-11e7-a910-0050569e7581","key": "test3.txt"}],"open_access": true,"owners": [148],"publication_state": "draft","titles": [{"title": "testCollectionDraft1"}]}}')
        mock_get.return_value.text = "response text mock"
        
        b2shcl = B2shareClient(self.configurationMock)
        draft_metadata = b2shcl.getDraftMetadata(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(bool(draft_metadata))
        
    def testAddB2shareMetadata(self):
        mock_patch_patcher = patch('b2shareclient.requests.patch')
        mock_patch = mock_patch_patcher.start()
        mock_patch.return_value.status_code = 200
        
        self.b2shcl.addB2shareMetadata(self.draft_id_mock, self.metadata_file_mock)
        
        mock_patch_patcher.stop()
        self.assertTrue(bool(True))
        
    def testCreateDraft(self):
        mock_post_patcher = patch('b2shareclient.requests.post')
        mock_post = mock_post_patcher.start()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = json.loads('{"id":"734c8cf3bb4f42cca0e9c4c3cf3cc86b"}')
        
        b2shcl = B2shareClient(self.configurationMock)
        record_id = b2shcl.createDraft(self.community_id_mock, self.title_mock, self.filePIDsString_mock)
        
        mock_post_patcher.stop()
        self.assertTrue(bool(record_id))
        
#### test failure status_code
    def testGetAllCommunities_failed(self):
        mock_get_patcher = patch('scripts.tests.cmd.b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.json.return_value = json.loads('{}')
        mock_get.return_value.status_code = 400
        
        b2shcl = B2shareClient(self.configurationMock)
        communities = b2shcl.getAllCommunities()
        
        mock_get_patcher.stop()
        
        self.assertFalse(bool(communities))
       
    def testDeleteDraft_failed(self):
        mock_get_patcher = patch('scripts.tests.cmd.b2shareclient.requests.delete')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 400
        
        b2shcl = B2shareClient(self.configurationMock)
        b2shcl.deleteDraft(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(True)
    
    def testGetDraftByID_failed(self):
        mock_get_patcher = patch('scripts.tests.cmd.b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = None
        
        b2shcl = B2shareClient(self.configurationMock)
        draft = b2shcl.getDraftByID(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertFalse(bool(draft))
    
    def testgGetCommunitySchema_failed(self):
        mock_get_patcher = patch('scripts.tests.cmd.b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = None
        
        b2shcl = B2shareClient(self.configurationMock)
        community_schema = b2shcl.getCommunitySchema(self.community_id_mock)
        
        mock_get_patcher.stop()
        self.assertFalse(bool(community_schema))
    
    def testPublishRecord_failed(self):
        mock_get_patcher = patch('scripts.tests.cmd.b2shareclient.requests.patch')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = None
        
        b2shcl = B2shareClient(self.configurationMock)
        b2shcl.publishRecord(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertTrue(True)
    
    def testGetDraftMetadata_failed(self):
        mock_get_patcher = patch('scripts.tests.cmd.b2shareclient.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = json.loads('{}')
        mock_get.return_value.text = None
        
        b2shcl = B2shareClient(self.configurationMock)
        draft_metadata = b2shcl.getDraftMetadata(self.draft_id_mock)
        
        mock_get_patcher.stop()
        self.assertFalse(bool(draft_metadata))
        
    def testAddB2shareMetadata_failed(self):
        mock_patch_patcher = patch('scripts.tests.cmd.b2shareclient.requests.patch')
        mock_patch = mock_patch_patcher.start()
        mock_patch.return_value.status_code = 400
        
        self.b2shcl.addB2shareMetadata(self.draft_id_mock, self.metadata_file_mock)
        
        mock_patch_patcher.stop()
        self.assertTrue(bool(True))
        
    def testCreateDraft_failed(self):
        mock_post_patcher = patch('scripts.tests.cmd.b2shareclient.requests.post')
        mock_post = mock_post_patcher.start()
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = json.loads('{}')
        
        b2shcl = B2shareClient(self.configurationMock)
        record_id = b2shcl.createDraft(self.community_id_mock, self.title_mock, self.filePIDsString_mock)
        
        mock_post_patcher.stop()
        self.assertFalse(bool(record_id))

if __name__ == '__main__':
    unittest.main()