import unittest
from mock import MagicMock, patch
from os.path import dirname
from os.path import abspath
import json
import os
import sys

sys.path.insert(0,
                os.path.join(dirname(dirname(dirname(dirname(abspath(__file__))))),
                             "cmd"))

import b2shareclientCLI as b2shareclientCLI

import logging
test_logger = logging.getLogger('B2shareClientCLITest')  

class argsMock():
    title = "test"
    collectionPath = ""
    communityID = "EUDAT"
    confpath = "/home/irods/B2SAFE-core/conf/b2share_connection.conf"
    metadata = "/localpath/to/metadata"
    record_id = "someID123"
    rec_id = "someID123"
    userName = "userName"
    commID = "someCommunityID123"
    commName = "Aalto"
    draft_id = "someID123"
    draft_to_delete_id = "someID123"
    debug = True
    dryrun = False
    irodsenv = None
    
class B2shareClientCLITest(unittest.TestCase):
    def setUp(self):
        self.configurationMock = MagicMock(confpath = "/home/irods/B2SAFE-core/conf/b2share_connection.conf", 
                                      b2share_host_name = 'https://trng-b2share.eudat.eu/api', 
                                      list_communities_endpoint = '/communities',
                                      access_parameter = '/?access_token=',
                                      access_token = 'JFSUcYzTRpMdVCEyAk3mmtGcfpmH',
                                      irods_home_dir = '',
                                      irods_debug = True,
                                      dryrun = False,
                                      debug = True,
                                      logger = test_logger)
        self.collectionPathMock = "/local/path/to/B2SAFE/collection"
        self.fileTreeMock = {'/JULK_ZONE/home/irods/julia/collection_A/subCollection_C/collection_A1': {'__files__': ['copytest.txt', 'test1.txt']}}
        self.b2shcl = MagicMock()
        pass

    def tearDown(self):
        pass
    
    def testDraft(self):
        with patch('configuration.Configuration.parseConf'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as b2shareclientCLIMock:
                with patch('b2shareclientCLI.collectPIDsForCollection') as b2shareclientCLIMock2:
                    with patch('b2shareclient.B2shareClient.createDraft') as b2shareclientMock:
                        b2shareclientCLIMock.return_value = "tocken_mock"
                        b2shareclientCLIMock2.return_value = [{"key":"BasZone/home/julia/testcollection/collection_A/metatest2.txt", "ePIC_PID":"20.500.11946/619416e2-e0d8-11e7-8ca4-0050569e7581"}]
                        b2shareclientMock.return_value = "ID_mock"
                    
                        record_id = b2shareclientCLI.draft(argsMock)
                        self.assertEqual(record_id, "ID_mock", "testing creating draft ok")
    
    def testGetCommunityIDByName(self):
        mock_get_patcher = patch('b2shareclientCLI.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.json.return_value = json.loads('{"hits": {"hits": [{"created": "Wed, 21 Dec 2016 08:57:40 GMT", "description": "Aalto University", "id": "c4234f93-da96-4d2f-a2c8-fa83d0775212", "name": "Aalto"}]}}')
        mock_get.return_value.status_code = 200
        
        community_id = b2shareclientCLI.getCommunityIDByName(self.configurationMock, "Aalto")
        mock_get_patcher.stop()
        
        self.assertIsNotNone(community_id)
    
    def testGetAllCommunities(self):
        with patch('configuration.Configuration.parseConf'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as CLIMock:
                    with patch('b2shareclient.B2shareClient.getAllCommunities') as clientMock:
                        CLIMock.return_value = "tocken_mock"
                        clientMock.return_value = "communities_list"
                    
                        communities = b2shareclientCLI.getAllCommunities(argsMock)
                        self.assertTrue(bool(communities))
    
    @patch("configuration.Configuration")
    def testAddMetadata(self, config):
        with patch('b2shareclient.B2shareClient.addB2shareMetadata'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as b2shareclientCLIMock:
                with patch('manifest.IRODSUtils.getFile') as file_from_IRODSUtils_Mock:
                    config.irods_home_dir = "/username/home/"
                    config.irods_debug = True
                    config.parseConf.return_value = None
                    
                    b2shareclientCLIMock.return_value = "tocken_mock"
                    file_from_IRODSUtils_Mock.return_value = "## coment \n\n [required] \n\n community \n EUDAT \n\n [optional]\n\n"
                    
                    b2shareclientCLI.addMetadata(argsMock)
                    self.assertTrue(True)
    
    def testPublish(self):
        with patch('configuration.Configuration.parseConf'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as CLIMock:
                    with patch('b2shareclient.B2shareClient.publishRecord'):
                        CLIMock.return_value = "tocken_mock"
                        
                        b2shareclientCLI.publish(argsMock)
                        self.assertTrue(True)
    
    def testGetAccessTokenWithConfigs(self):
        with patch('manifest.IRODSUtils.getMetadata') as getMetadata_mock:
            getMetadata_mock.return_value = ["tocken_mock"]
            
            access_tocken = b2shareclientCLI.getAccessTokenWithConfigs(self.configurationMock, argsMock)
            self.assertEqual(access_tocken, "tocken_mock", "access token is not as expected")
       
    def testGetCommunitySchema(self):
        with patch('configuration.Configuration.parseConf'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as CLI_getTocken_Mock:
                with patch('b2shareclientCLI.getCommunityIDByName') as CLI_getComID_Mock:
                    with patch('b2shareclient.B2shareClient.getCommunitySchema') as clientMock:
                        CLI_getTocken_Mock.return_value = "tocken_mock"
                        CLI_getComID_Mock.return_value = "comID"
                        clientMock.return_value = "community schema"
                        
                        schema = b2shareclientCLI.getCommunitySchema(argsMock)
                        self.assertTrue(bool(schema))
                        
                        argsMock.commID = None
                        schema = b2shareclientCLI.getCommunitySchema(argsMock)
                        self.assertTrue(bool(schema))
                        
                        argsMock.commID = "someCommunityID123"
                        
    def testGetDraftByID(self):
        with patch('configuration.Configuration.parseConf'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as CLI_getTocken_Mock:
                with patch('b2shareclient.B2shareClient.getDraftByID') as clientMock:
                    CLI_getTocken_Mock.return_value = "tocken_mock"
                    clientMock.return_value = "draft"
                    
                    draft = b2shareclientCLI.getDraftByID(argsMock)
                    self.assertTrue(bool(draft))
                    
    def testDeleteDraft(self):
        with patch('configuration.Configuration.parseConf'):
            with patch('b2shareclientCLI.getAccessTokenWithConfigs') as CLI_getTocken_Mock:
                with patch('b2shareclient.B2shareClient.deleteDraft'):
                    CLI_getTocken_Mock.return_value = "tocken_mock"
                    
                    b2shareclientCLI.deleteDraft(argsMock)
                    self.assertTrue(True)
    
    def testCollectPIDsForCollection(self):
        with patch('manifest.IRODSUtils.deepListDir') as listDir_mock:
            with patch('manifest.IRODSUtils.getMetadata') as metadata_mock:
                with patch('b2shareclientCLI.collectFilePathsFromTree') as b2shareclientCLI_mock:
                    listDir_mock.return_value = ('', self.fileTreeMock)
                    metadata_mock.return_value = ["PID_mock"]
                    b2shareclientCLI_mock.return_value = {'/JULK_ZONE/home/irods/julia/collection_A/subCollection_C/EUDAT_manifest_METS.xml': 'EUDAT_manifest_METS.xml',
                                                          '/JULK_ZONE/home/irods/julia/collection_A/b2share_metadata.json': 'b2share_metadata.json'}
                
                    PIDobjectsString = b2shareclientCLI.collectPIDsForCollection(self.collectionPathMock, self.configurationMock)
                    expectedResultStr = '[{"key":"JULK_ZONE/home/irods/julia/collection_A/b2share_metadata.json", "ePIC_PID":"PID_mock"},{"key":"JULK_ZONE/home/irods/julia/collection_A/subCollection_C/EUDAT_manifest_METS.xml", "ePIC_PID":"PID_mock"}]'
                    self.assertEqual(expectedResultStr, PIDobjectsString)
    
    def testCollectFilePathsFromTree(self):
        filePaths = b2shareclientCLI.collectFilePathsFromTree(self.fileTreeMock)
        expectedResult = {'/JULK_ZONE/home/irods/julia/collection_A/subCollection_C/collection_A1'+ os.sep +'copytest.txt': 'copytest.txt', '/JULK_ZONE/home/irods/julia/collection_A/subCollection_C/collection_A1'+ os.sep +'test1.txt': 'test1.txt'}
        self.assertEqual(expectedResult, filePaths)
        
if __name__ == "__main__":
    unittest.main()
