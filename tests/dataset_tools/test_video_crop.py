from unittest import TestCase
from unittest.mock import patch
from os import path, remove
from src.dataset_tools.video_crop import (
    load_align,
    crop_words,
    crop_word,
    crop_video,
    save_to_file,
    apply_padding,
    get_face_bounds,
    OutputType,
)
from moviepy.video.io.VideoFileClip import VideoFileClip

from shutil import rmtree
from io import StringIO


@patch('src.dataset_tools.video_crop.crop_word')
class CropWordsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_VALID_WORD = {
            'case': 'success',
            'alignedWord': 'valid',
            'start': '1',
            'end': '2',
        }
        TEST_FAIL_WORD = {
            'case': 'failure',
            'alignedWord': 'valid',
            'start': '1',
            'end': '2',
        }
        TEST_UNK_WORD = {
            'case': 'success',
            'alignedWord': '<unk>',
            'start': '1',
            'end': '2',
        }

        cls.TEST_VIDEOID = 'foobar'
        TEST_ALIGN = []
        for i in range(10):
            TEST_ALIGN.append(TEST_VALID_WORD)

        TEST_ALIGN_WITH_FAIL_LIST = TEST_ALIGN[:]
        for i in range(5):
            TEST_ALIGN_WITH_FAIL_LIST.append(TEST_FAIL_WORD)
            cls.TEST_ALIGN_WITH_FAIL = {'words': TEST_ALIGN_WITH_FAIL_LIST}

        TEST_ALIGN_WITH_UNK_LIST = TEST_ALIGN[:]
        for i in range(5):
            TEST_ALIGN_WITH_UNK_LIST.append(TEST_UNK_WORD)
            cls.TEST_ALIGN_WITH_UNK = {'words': TEST_ALIGN_WITH_UNK_LIST}

    def test_ignore_invalid_words(self, mock_crop_word):
        crop_words(self.TEST_ALIGN_WITH_FAIL, self.TEST_VIDEOID, False)

        self.assertEqual(mock_crop_word.call_count, 10)

    def test_ignore_unk_words(self, mock_crop_word):
        crop_words(self.TEST_ALIGN_WITH_UNK, self.TEST_VIDEOID, False)

        self.assertEqual(mock_crop_word.call_count, 10)


@patch('moviepy.video.io.VideoFileClip')
class SaveToFileTest(TestCase):
    @classmethod
    def setUpClass(cls):
        class MockVideoFileClip(object):
            def write_videofile(self, filename, audio_codec):

                open(filename, 'a').close()

        cls.VIDEOID = 'foobar'
        cls.FINALWORD = MockVideoFileClip()
        cls.FOUNDWORD = 'TEST_WORD'
        cls.FILENAME_PREDICT = 'predictFile'
        cls.FILENAME_TRAIN = 'trainFile'
        cls.FILENAME_VAL = 'validateFile'

        save_to_file(
            cls.FINALWORD,
            cls.FOUNDWORD,
            cls.FILENAME_PREDICT,
            OutputType.PREDICT,
        )
        save_to_file(
            cls.FINALWORD,
            cls.FOUNDWORD,
            cls.FILENAME_TRAIN,
            OutputType.TRAIN,
        )
        save_to_file(
            cls.FINALWORD, cls.FOUNDWORD, cls.FILENAME_VAL, OutputType.VAL
        )

    @classmethod
    def tearDownClass(cls):
        rmtree(f'dataset/{cls.FOUNDWORD}')
        remove(f'predict/{cls.FILENAME_PREDICT}.mp4')

    def test_predict_saves_in_correct_location(self, mock_video_file_clip):
        expect_file_name = f'predict/{self.FILENAME_PREDICT}.mp4'
        self.assertTrue(path.exists(expect_file_name))

    def test_train_saves_in_correct_location_train(self, mock_video_file_clip):
        expect_file_name = f'dataset/{self.FOUNDWORD}/train/{self.FILENAME_TRAIN}.mp4'
        self.assertTrue(path.exists(expect_file_name))

    def test_val_saves_in_correct_location_train(self, mock_video_file_clip):
        expect_file_name = f'dataset/{self.FOUNDWORD}/val/{self.FILENAME_VAL}.mp4'
        self.assertTrue(path.exists(expect_file_name))


class ApplyPaddingTests(TestCase):
    def test_padding_applies_normally(self):
        ACTUAL_PADDING = apply_padding(5, 10, 1, 20)
        EXPECTED_PADDING = (4, 11)
        self.assertEqual(ACTUAL_PADDING, EXPECTED_PADDING)

    def test_padding_on_left_side_only(self):
        ACTUAL_PADDING = apply_padding(5, 10, 1, 10)
        EXPECTED_PADDING = (4, 10)
        self.assertEqual(ACTUAL_PADDING, EXPECTED_PADDING)

    def test_padding_on_right_side_only(self):
        ACTUAL_PADDING = apply_padding(0, 10, 1, 20)
        EXPECTED_PADDING = (0, 11)
        self.assertEqual(ACTUAL_PADDING, EXPECTED_PADDING)

    def test_no_padding(self):
        ACTUAL_PADDING = apply_padding(0, 10, 1, 10)
        EXPECTED_PADDING = (0, 10)
        self.assertEqual(ACTUAL_PADDING, EXPECTED_PADDING)

    def test_reversed_start_end(self):
        ACTUAL_PADDING = apply_padding(10, 5, 1, 20)
        EXPECTED_PADDING = apply_padding(5, 10, 1, 20)
        self.assertEqual(ACTUAL_PADDING, EXPECTED_PADDING)

    def test_partial_padding_not_applied(self):
        ACTUAL_PADDING = apply_padding(5, 10, 100, 20)
        EXPECTED_PADDING = (5, 10)
        self.assertEqual(ACTUAL_PADDING, EXPECTED_PADDING)


class GetFaceBoundsTest(TestCase):
    class MockFace:
        def __init__(self, left, right, bottom, top):
            self.leftv = left
            self.rightv = right
            self.bottomv = bottom
            self.topv = top

        def left(self):
            return self.leftv

        def right(self):
            return self.rightv

        def bottom(self):
            return self.bottomv

        def top(self):
            return self.topv

    @classmethod
    def setUpClass(cls):
        cls.MIDDLE_FACE = GetFaceBoundsTest.MockFace(5, 10, 10, 5)
        cls.TOP_LEFT_FACE = GetFaceBoundsTest.MockFace(0, 5, 15, 10)
        cls.BOTTOM_RIGHT_FACE = GetFaceBoundsTest.MockFace(10, 15, 5, 0)

    def test_bound_same_faces(self):
        EXPECTED_RESULT = {'left': 5, 'right': 10, 'top': 5, 'bottom': 10}
        self.assertEqual(
            EXPECTED_RESULT, get_face_bounds(
                self.MIDDLE_FACE, self.MIDDLE_FACE)
        )

    def test_bound_different_faces(self):
        EXPECTED_RESULT = {'left': 0, 'right': 15, 'top': 0, 'bottom': 15}
        self.assertEqual(
            EXPECTED_RESULT, get_face_bounds(
                self.TOP_LEFT_FACE, self.BOTTOM_RIGHT_FACE)
        )

    def test_bound_is_reflexive(self):
        self.assertEqual(
            get_face_bounds(self.TOP_LEFT_FACE, self.BOTTOM_RIGHT_FACE),
            get_face_bounds(self.BOTTOM_RIGHT_FACE, self.TOP_LEFT_FACE),
        )


@patch('src.dataset_tools.video_crop.apply_padding')
@patch('src.dataset_tools.video_crop.get_faces')
class CropWordTest(TestCase):
    class MockVideoFileClip(object):
        def __init__(self):
            self.duration = 0

        def subclip(self, start, end):
            return self

        def get_frame(t):
            return None

    @classmethod
    def setUpClass(cls):
        cls.TEST_WORD = 'foo'
        cls.START, cls.END = 0.5, 0.8
        cls.VIDEOID = 'fooID'
        cls.FACE_ONE = {'left': 10, 'right': 20, 'top': 10, 'bottom': 20}
        cls.FACE_TWO = {'left': 0, 'right': 10, 'top': 0, 'bottom': 10}

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_crop_on_missing_start_face(self, mock_stdout, mock_get_faces, mock_apply_padding):
        mock_get_faces.side_effect = [[], [self.FACE_ONE]]
        mock_apply_padding.return_value = (self.START, self.END)
        with patch('src.dataset_tools.video_crop.VideoFileClip') as mock_video_file_clip:
            mock_video_file_clip = CropWordTest.MockVideoFileClip()
            crop_word(
                self.TEST_WORD,
                self.START,
                self.END,
                self.VIDEOID,
                False,
            )
        self.assertTrue('No faces' in mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_crop_on_missing_end_face(self, mock_stdout, mock_get_faces, mock_apply_padding):
        mock_get_faces.side_effect = [[self.FACE_ONE], []]
        mock_apply_padding.return_value = (self.START, self.END)
        with patch('src.dataset_tools.video_crop.VideoFileClip') as mock_video_file_clip:
            mock_video_file_clip = CropWordTest.MockVideoFileClip()
            crop_word(
                self.TEST_WORD,
                self.START,
                self.END,
                self.VIDEOID,
                False,
            )
        self.assertTrue('No faces' in mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_crop_on_multiple_start_faces(self, mock_stdout, mock_get_faces, mock_apply_padding):
        mock_get_faces.side_effect = [
            [self.FACE_ONE, self.FACE_TWO], [self.FACE_ONE]]
        mock_apply_padding.return_value = (self.START, self.END)
        with patch('src.dataset_tools.video_crop.VideoFileClip') as mock_video_file_clip:
            mock_video_file_clip = CropWordTest.MockVideoFileClip()
            crop_word(
                self.TEST_WORD,
                self.START,
                self.END,
                self.VIDEOID,
                False,
            )
        self.assertTrue('Multiple' in mock_stdout.getvalue())
    @patch('sys.stdout', new_callable=StringIO)
    def test_no_crop_on_multiple_end_faces(self, mock_stdout, mock_get_faces, mock_apply_padding):
        mock_get_faces.side_effect = [
            [self.FACE_ONE], [self.FACE_ONE, self.FACE_TWO]]
        mock_apply_padding.return_value = (self.START, self.END)
        with patch('src.dataset_tools.video_crop.VideoFileClip') as mock_video_file_clip:
            mock_video_file_clip = CropWordTest.MockVideoFileClip()
            crop_word(
                self.TEST_WORD,
                self.START,
                self.END,
                self.VIDEOID,
                False,
            )
        self.assertTrue('Multiple' in mock_stdout.getvalue())

    @patch('src.dataset_tools.video_crop.save_to_file')
    @patch('src.dataset_tools.video_crop.get_face_bounds')
    @patch('src.dataset_tools.video_crop.crop')
    def test_crop_with_one_start_end_face(
        self,
        mock_save_to_file,
        mock_get_face_bounds,
        mock_crop,
        mock_get_faces,
        mock_apply_padding,
    ):
        mock_get_faces.side_effect = [[self.FACE_ONE], [self.FACE_TWO]]
        mock_get_face_bounds.return_value = self.FACE_ONE
        mock_apply_padding.return_value = [self.START, self.END]
        with patch('src.dataset_tools.video_crop.VideoFileClip') as mock_video_file_clip:
            mock_video_file_clip = CropWordTest.MockVideoFileClip()
            crop_word(
                self.TEST_WORD,
                self.START,
                self.END,
                self.VIDEOID,
                False,
            )
        self.assertEqual(mock_crop.call_count, 1)
