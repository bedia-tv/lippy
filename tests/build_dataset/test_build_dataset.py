from unittest import TestCase
from unittest.mock import patch
from os import path, remove
from src.build_dataset.build_dataset import (
    setup_dirs,
    clear_dirs,
    get_processed_videos,
    get_playlist_videos,
    build,
    add_to_dataset,
)
from src.build_dataset.download import download
from src.build_dataset.get_align import get_align
from io import StringIO
from textwrap import dedent


@patch("builtins.open")
class AddToDatasetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.VIDEOID = "foo"
        cls.VALIDATE = False

    @patch("src.build_dataset.build_dataset.download")
    @patch("src.build_dataset.build_dataset.get_align")
    def test_download_error_stops_align(self, mock_align, mock_download, mock_open):
        mock_download.side_effect = Exception()
        mock_align.return_value = None

        add_to_dataset(self.VIDEOID, self.VALIDATE)
        self.assertEqual(mock_align.call_count, 0)

    @patch("src.build_dataset.build_dataset.download")
    @patch("src.build_dataset.build_dataset.get_align")
    @patch("src.build_dataset.build_dataset.crop_video")
    def test_download_error_stops_crop(
        self, mock_crop, mock_align, mock_download, mock_open
    ):
        mock_download.side_effect = Exception()
        mock_align.return_value = None
        mock_crop.return_value = None

        add_to_dataset(self.VIDEOID, self.VALIDATE)
        self.assertEqual(mock_crop.call_count, 0)

    @patch("src.build_dataset.build_dataset.download")
    @patch("src.build_dataset.build_dataset.get_align")
    @patch("src.build_dataset.build_dataset.crop_video")
    def test_align_error_stops_crop(
        self, mock_crop, mock_align, mock_download, mock_open
    ):
        mock_download.return_value = [
            f"videos/{self.VIDEOID}.mp4",
            f"audio/{self.VIDEOID}.mp3",
            f"transcripts/{self.VIDEOID}.txt",
            self.VIDEOID,
        ]
        mock_align.side_effect = Exception()
        mock_crop.return_value = None

        add_to_dataset(self.VIDEOID, self.VALIDATE)
        self.assertEqual(mock_crop.call_count, 0)


class SetupDirsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        setup_dirs()

    def test_setup_dirs_creates_outputs(self):
        self.assertTrue(path.exists("dataset"))

    def test_setup_dirs_creates_audio(self):
        self.assertTrue(path.exists("audio"))

    def test_setup_dirs_creates_videos(self):
        self.assertTrue(path.exists("videos"))

    def test_setup_dirs_creates_transcripts(self):
        self.assertTrue(path.exists("transcripts"))

    def test_setup_dirs_creates_jsons(self):
        self.assertTrue(path.exists("jsons"))

    def test_setup_dirs_creates_validate(self):
        self.assertTrue(path.exists("predict"))


class ClearDirsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        setup_dirs()

        cls.VIDEOID = "foobar"
        # create fake file in each folder
        cls.AUDIO_FILENAME = f"audio/{cls.VIDEOID}.mp3"
        cls.JSONS_FILENAME = f"jsons/{cls.VIDEOID}.json"
        cls.TRANS_FILENAME = f"transcripts/{cls.VIDEOID}.txt"
        cls.VIDEO_FILENAME = f"videos/{cls.VIDEOID}.mp4"

        files = [
            cls.AUDIO_FILENAME,
            cls.JSONS_FILENAME,
            cls.TRANS_FILENAME,
            cls.VIDEO_FILENAME,
        ]

        for file in files:
            open(file, "a").close()

        clear_dirs(cls.VIDEOID)

    def test_clear_dirs_deleted_audio_file(self):
        # check file is not in audio folder
        self.assertFalse(path.exists(self.AUDIO_FILENAME))

    def test_clear_dirs_deleted_json_file(self):
        # check file is not in audio folder
        self.assertFalse(path.exists(self.JSONS_FILENAME))

    def test_clear_dirs_deleted_transcript_file(self):
        # check file is not in audio folder
        self.assertFalse(path.exists(self.TRANS_FILENAME))

    def test_clear_dirs_deleted_video_file(self):
        # check file is not in audio folder
        self.assertFalse(path.exists(self.VIDEO_FILENAME))


class GetProcessedvideosTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.EMPTY_FILE = "empty.txt"
        cls.POPULATED_FILE = "pop.txt"
        with open(cls.POPULATED_FILE, "w+") as pop:
            pop.write("foo\n")
            pop.write("bar\n")

    @classmethod
    def tearDownClass(cls):
        if path.exists(cls.EMPTY_FILE):
            remove(cls.EMPTY_FILE)
        if path.exists(cls.POPULATED_FILE):
            remove(cls.POPULATED_FILE)

    def test_file_is_created(self):
        processed_videos = get_processed_videos(self.EMPTY_FILE)

        self.assertTrue(path.exists(self.EMPTY_FILE))

    def test_empty_file_returns_empty_list(self):
        processed_videos = get_processed_videos(self.EMPTY_FILE)

        self.assertEqual(len(processed_videos), 0)

    def test_populated_file_context(self):
        processed_videos = get_processed_videos(self.POPULATED_FILE)

        self.assertEqual(len(processed_videos), 2)


class GetPlaylistVideosTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.EMPTY_FILE = "empty.txt"
        cls.POPULATED_FILE = "pop.txt"
        with open(cls.POPULATED_FILE, "w+") as pop:
            pop.write("foo\n")
            pop.write("bar\n")

    @classmethod
    def tearDownClass(cls):
        if path.exists(cls.EMPTY_FILE):
            remove(cls.EMPTY_FILE)
        if path.exists(cls.POPULATED_FILE):
            remove(cls.POPULATED_FILE)

    def test_file_is_created(self):
        processed_videos = get_playlist_videos(self.EMPTY_FILE)

        self.assertTrue(path.exists(self.EMPTY_FILE))

    def test_empty_file_returns_empty_list(self):
        processed_videos = get_playlist_videos(self.EMPTY_FILE)

        self.assertEqual(len(processed_videos), 0)

    def test_populated_file_returns_context(self):
        processed_videos = get_playlist_videos(self.POPULATED_FILE)

        self.assertEqual(len(processed_videos), 2)


class BuildTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.PLAYLIST_FILE = "playlist.txt"

    @patch("src.build_dataset.build_dataset.get_playlist_videos")
    @patch("src.build_dataset.build_dataset.get_processed_videos")
    @patch("src.build_dataset.build_dataset.add_to_dataset")
    def test_processed_videos_are_not_reprocessed(
        self, mock_add_to_dataset, mock_processed_videos, mock_playlist_videos
    ):
        mock_add_to_dataset.return_value = None
        mock_processed_videos.return_value = {"foo"}
        mock_playlist_videos.return_value = ["foo"]

        build(self.PLAYLIST_FILE)
        self.assertEqual(mock_add_to_dataset.call_count, 0)

    @patch("src.build_dataset.build_dataset.get_playlist_videos")
    @patch("src.build_dataset.build_dataset.get_processed_videos")
    @patch("src.build_dataset.build_dataset.add_to_dataset")
    def test_new_videos_are_processed(
        self, mock_add_to_dataset, mock_processed_videos, mock_playlist_videos
    ):
        mock_add_to_dataset.return_value = None
        mock_processed_videos.return_value = {"foo"}
        mock_playlist_videos.return_value = ["foo", "bar"]

        build(self.PLAYLIST_FILE)
        self.assertEqual(mock_add_to_dataset.call_count, 1)
