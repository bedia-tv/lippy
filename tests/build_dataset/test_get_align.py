import unittest
from unittest.mock import patch, mock_open, Mock
from src.build_dataset.get_align import set_file_locations, gentle_align_get, get_align
from os import path, remove
from textwrap import dedent
import json


class SetFileLocationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

        cls.FILE_DATA = 'TEST_AUDIO'
        cls.AUDIO_FILE_NAME = 'base/audio_file.mp4'
        cls.AUDIO_FILE_RAW_NAME = 'audio_file'
        cls.TRANS_FILE_NAME = 'transcript_file'

    @patch('builtins.open')
    def test_file_locs_correct_format(self, mocked_open):
        mocked_open.return_value = self.FILE_DATA
        ACTUAL_OPTIONS_DICT = set_file_locations(
            self.AUDIO_FILE_NAME, self.TRANS_FILE_NAME
        )

        EXPECTED_OPTIONS_DICT = {
            'params': (('async', 'false'),),
            'files': {
                'audio': (self.AUDIO_FILE_NAME, self.FILE_DATA),
                'transcript': (self.TRANS_FILE_NAME, self.FILE_DATA)
            },
            'align_name': f'jsons/{self.AUDIO_FILE_RAW_NAME}.json'
        }

        self.assertEqual(ACTUAL_OPTIONS_DICT, EXPECTED_OPTIONS_DICT)


class GentleAlignGetTests(unittest.TestCase):
    @patch('src.build_dataset.get_align.post')
    def test_gentle_response_is_json(self, mock_post):
        mock_post.return_value = dedent(
            '''
        {
            "test": "value",
            "should be": "valid JSON"
        }'''
        ).strip()
        expected_json = gentle_align_get(None, None)
        # throws exception if invalid JSON
        json_object = json.loads(expected_json)

    @patch('src.build_dataset.get_align.post')
    @patch('src.build_dataset.get_align.set_file_locations')
    def test_connection_refused_returns_none(self, mock_set_file, mock_post):
        mock_set_file.return_value = {'params': 'foo', 'files': 'bar'}
        mock_post.side_effect = ConnectionRefusedError()

        no_value = gentle_align_get(None, None)
        self.assertEqual(no_value, None)


class GetAlignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.AUDIO_FILE_NAME = 'testAudio.mp4'
        cls.AUDIO_RAW_NAME = 'testAudio'
        cls.TRANS_FILE_NAME = 'testTranscript.txt'
        cls.FILE_DATA = 'testData'

    @classmethod
    def tearDownClass(cls):
        # del align file
        remove(f'jsons/{cls.AUDIO_RAW_NAME}.json')

    @patch('src.build_dataset.get_align.set_file_locations')
    @patch('src.build_dataset.get_align.gentle_align_get')
    def test_align_in_correct_location(
        self, mock_gentle_align_get, mock_set_file_locations
    ):
        mock_response = Mock()
        mock_gentle_align_get.return_value = mock_response
        mock_response.text = '{\'test\': \'this is a test json file.\'}'

        EXPECTED_ALIGN_NAME = f'jsons/{self.AUDIO_RAW_NAME}.json'
        mock_set_file_locations.return_value = {
            'params': (('async', 'false'),),
            'files': {
                'audio': (self.AUDIO_FILE_NAME, self.FILE_DATA),
                'transcript': (self.TRANS_FILE_NAME, self.FILE_DATA),
            },
            'align_name': EXPECTED_ALIGN_NAME,
        }

        get_align(self.AUDIO_FILE_NAME, self.TRANS_FILE_NAME)
        self.assertTrue(path.exists(EXPECTED_ALIGN_NAME))
