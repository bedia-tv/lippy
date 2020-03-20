from unittest import TestCase, mock
from os import path, remove
from src.dataset_tools.run_dataset import run_dataset


class RunDatasetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_output = 'train'
        cls.valid_playlist_file = 'valid_playlist.txt'
        cls.url = 'mock_url'
        cls.valid_audio_file = 'valid_audio.mp3'
        cls.valid_transcript_file = 'valid_transcript.txt'
        cls.videoid = 'mock_videoid'

        cls.valid_files = [
            cls.valid_playlist_file,
            cls.valid_audio_file,
            cls.valid_transcript_file
        ]

        for file in cls.valid_files:
            open(file, 'a').close()

    @classmethod
    def tearDownClass(cls):
        for file in cls.valid_files:
            if path.exists(file):
                remove(file)

    def test_build_with_no_output(self):
        function = 'build'
        no_output = None
        with self.assertRaises(ValueError):
            run_dataset(function, no_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_build_with_invalid_output(self):
        function = 'build'
        invalid_output = 'mock_output'
        with self.assertRaises(ValueError):
            run_dataset(function, invalid_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_build_with_no_playlist(self):
        function = 'build'
        no_playlist_file = None
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, no_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_build_with_invalid_playlist(self):
        function = 'build'
        invalid_playlist_file = 'mock_playlist'
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, invalid_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    @mock.patch('src.dataset_tools.run_dataset.build')
    def test_build_calls_build_with_valid_input(self, mock_build):
        function = 'build'
        run_dataset(function, self.valid_output, self.valid_playlist_file,
                    self.url, self.valid_audio_file, self.valid_transcript_file,
                    self.videoid)
        self.assertTrue(mock_build.called)

    def test_download_with_no_url(self):
        function = 'download'
        url = None
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, self.valid_playlist_file,
                        url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    @mock.patch('src.dataset_tools.run_dataset.download')
    def test_download_with_url(self, mock_download):
        function = 'download'
        run_dataset(function, self.valid_output, self.valid_playlist_file,
                    self.url, self.valid_audio_file, self.valid_transcript_file,
                    self.videoid)
        self.assertTrue(mock_download.called)

    def test_align_with_no_audio(self):
        function = 'align'
        no_audio_file = None
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, self.valid_playlist_file,
                        self.url, no_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_align_with_invalid_audio(self):
        function = 'align'
        invalid_audio_file = 'mock_audio'
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, self.valid_playlist_file,
                        self.url, invalid_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_align_with_no_transcript(self):
        function = 'align'
        no_transcript_file = None
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, no_transcript_file,
                        self.videoid)

    def test_align_with_invalid_transcript(self):
        function = 'align'
        invalid_transcript_file = 'mock_transcript'
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, invalid_transcript_file,
                        self.videoid)

    @mock.patch('src.dataset_tools.run_dataset.get_align')
    def test_align_calls_get_align_with_valid_input(self, mock_get_align):
        function = 'align'
        run_dataset(function, self.valid_output, self.valid_playlist_file,
                    self.url, self.valid_audio_file, self.valid_transcript_file,
                    self.videoid)
        self.assertTrue(mock_get_align.called)

    def test_crop_with_no_output(self):
        function = 'crop'
        no_output = None
        with self.assertRaises(ValueError):
            run_dataset(function, no_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_crop_with_invalid_output(self):
        function = 'crop'
        invalid_output = 'mock_output'
        with self.assertRaises(ValueError):
            run_dataset(function, invalid_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        self.videoid)

    def test_crop_with_no_videoid(self):
        function = 'crop'
        no_videoid = None
        with self.assertRaises(ValueError):
            run_dataset(function, self.valid_output, self.valid_playlist_file,
                        self.url, self.valid_audio_file, self.valid_transcript_file,
                        no_videoid)

    @mock.patch('src.dataset_tools.run_dataset.crop_video')
    def test_crop_calls_crop_video_with_valid_input(self, mock_crop_video):
        function = 'crop'
        run_dataset(function, self.valid_output, self.valid_playlist_file,
                    self.url, self.valid_audio_file, self.valid_transcript_file,
                    self.videoid)
        self.assertTrue(mock_crop_video.called)
