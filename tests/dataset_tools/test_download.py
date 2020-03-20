from unittest import TestCase
from os import path, remove
from src.dataset_tools.download import (
    extract_transcript,
    save_transcript,
    get_transcript,
    get_options,
    handle_subtitles,
    download,
    file_locations,
)
from unittest.mock import patch
from textwrap import dedent


class ExtractTranscriptTests(TestCase):
    TEST_TTML = dedent(
        '''
        <?xml version='1.0' encoding='utf-8'?>
    <tt xmlns='http://www.w3.org/ns/ttml' xmlns:ttp='http://www.w3.org/ns/ttml#parameter' xmlns:tts='http://www.w3.org/ns/ttml#styling' xmlns:ttm='http://www.w3.org/ns/ttml#metadata' xmlns:xml='http://www.w3.org/XML/1998/namespace' ttp:timeBase='media' ttp:frameRate='24' xml:lang='en'>
    <head>
    <metadata>
    <ttm:title>Sample TTML</ttm:title>
    </metadata>
    </head>
    <body region='bottom' style='s1'>
    <p xml:id='subtitle1' begin='00:00:01.375' end='00:00:05.750'>A test subtitle. Let&#39;s hope it works...</p>
    </body>
    </tt>
    '''
    ).strip()

    EXPECTED_TRANSCRIPT = '\nSample TTML\nA test subtitle. Let\'s hope it works...\n'

    @classmethod
    def setUpClass(cls):
        cls.ACTUAL_TRANSCRIPT = extract_transcript(cls.TEST_TTML)

    def test_transcript_extraction_correct(self):
        self.assertEqual(self.ACTUAL_TRANSCRIPT, self.EXPECTED_TRANSCRIPT)

    def test_transcript_fixes_ascii_apostrophes(self):
        self.assertFalse('&#39;' in self.ACTUAL_TRANSCRIPT)


class SaveTranscriptTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_CLEANTEXT = 'Test cleantext'
        cls.TEST_VIDEOID = 'VIDEO_ID'
        cls.TTML_LOCATION = f'transcripts/{cls.TEST_VIDEOID}.en.ttml'
        cls.TRANSCRIPT_LOCATION = f'transcripts/{cls.TEST_VIDEOID}.txt'

        open(cls.TTML_LOCATION, 'a').close()

        save_transcript(cls.TEST_CLEANTEXT, cls.TEST_VIDEOID)

    @classmethod
    def tearDownClass(cls):
        # delete text file
        if path.exists(cls.TRANSCRIPT_LOCATION):
            remove(cls.TRANSCRIPT_LOCATION)

    def test_ttml_file_removed(self):
        self.assertFalse(path.exists(self.TTML_LOCATION))

    def test_transcript_file_exists(self):
        self.assertTrue(path.exists(self.TRANSCRIPT_LOCATION))

    def test_transcript_file_contents(self):
        with open(self.TRANSCRIPT_LOCATION, 'r') as transcript:
            EXPECTED_CLEARTEXT = transcript.read()

        self.assertEqual(self.TEST_CLEANTEXT, EXPECTED_CLEARTEXT)


class FileLocationsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.VIDEO_ID = 'foo'
        cls.EXPECTED_VIDEO_FILE = 'videos/foo.mp4'
        cls.EXPECTED_AUDIO_FILE = 'audio/foo.mp3'
        cls.EXPECTED_SUBS_FILE = 'transcripts/foo.txt'

        (
            cls.ACTUAL_VIDEO_FILE,
            cls.ACTUAL_AUDIO_FILE,
            cls.ACTUAL_SUBS_FILE,
            cls.ACTUAL_VIDEO_ID,
        ) = file_locations(cls.VIDEO_ID)

    def test_video_file_output(self):
        self.assertEqual(self.ACTUAL_VIDEO_FILE, self.EXPECTED_VIDEO_FILE)

    def test_audio_file_output(self):
        self.assertEqual(self.ACTUAL_AUDIO_FILE, self.EXPECTED_AUDIO_FILE)

    def test_subs_file_output(self):
        self.assertEqual(self.ACTUAL_SUBS_FILE, self.EXPECTED_SUBS_FILE)

    def test_videoid_output(self):
        self.assertEqual(self.VIDEO_ID, self.ACTUAL_VIDEO_ID)


class GetTranscript(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ACTUAL_VIDEOID = 'foo'
        cls.OTHER_VIDEOID = 'bar'

        cls.ACTUAL_CLEARTEXT = 'You should read this content.'
        cls.OTHER_CLEARTEXT = 'You shouldn\'t read this content.'
        with open(f'transcripts/{cls.ACTUAL_VIDEOID}.en.ttml', 'w+') as actual:
            actual.write(cls.ACTUAL_CLEARTEXT)

        with open(f'transcripts/{cls.OTHER_VIDEOID}.en.ttml', 'w+') as actual:
            actual.write(cls.OTHER_CLEARTEXT)

    @classmethod
    def tearDownClass(cls):
        remove(f'transcripts/{cls.ACTUAL_VIDEOID}.en.ttml')
        remove(f'transcripts/{cls.OTHER_VIDEOID}.en.ttml')

    def test_correct_file_read_from(self):
        OUTPUT_CLEARTEXT = get_transcript(self.ACTUAL_VIDEOID)
        self.assertEqual(OUTPUT_CLEARTEXT, self.ACTUAL_CLEARTEXT)


class DownloadTest(TestCase):
    class WorkingOptions(object):
        def download(self, url_list):
            return None

    class BrokenOptions(object):
        def download(self, url_list):
            raise Exception()

    @classmethod
    def setUpClass(cls):
        cls.URL = 'foo'

    @patch('src.dataset_tools.download.get_options')
    @patch('src.dataset_tools.download.handle_subtitles')
    def test_raise_exception_on_subs_download(
        self, mock_handle_subtitles, mock_get_options
    ):
        mock_get_options.return_value = [
            DownloadTest.BrokenOptions(),
            DownloadTest.WorkingOptions(),
            DownloadTest.WorkingOptions(),
        ]
        mock_handle_subtitles.side_effect = Exception()
        with self.assertRaises(Exception) as context:
            download(self.URL)

        self.assertTrue(
            'Error downloading subtitles' in str(context.exception))

    @patch('src.dataset_tools.download.get_options')
    @patch('src.dataset_tools.download.handle_subtitles')
    def test_raise_exception_on_audio_download(
        self, mock_handle_subtitles, mock_get_options
    ):
        mock_get_options.return_value = [
            DownloadTest.WorkingOptions(),
            DownloadTest.BrokenOptions(),
            DownloadTest.WorkingOptions(),
        ]
        mock_handle_subtitles.return_value = None
        with self.assertRaises(Exception) as context:
            download(self.URL)

        self.assertTrue('Error downloading audio' in str(context.exception))

    @patch('src.dataset_tools.download.get_options')
    @patch('src.dataset_tools.download.handle_subtitles')
    def test_raise_exception_on_video_download(
        self, mock_handle_subtitles, mock_get_options
    ):
        mock_get_options.return_value = [
            DownloadTest.WorkingOptions(),
            DownloadTest.WorkingOptions(),
            DownloadTest.BrokenOptions(),
        ]
        mock_handle_subtitles.return_value = None
        with self.assertRaises(Exception) as context:
            download(self.URL)

        self.assertTrue('Error downloading video' in str(context.exception))
