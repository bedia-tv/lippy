class TestClass():
    TEST_STRING_BASE = 'this is a test list string'
    TEST_STRING_REPLACE = 'this is a test list false'
    _TEST_STRING_INSERT = 'this is a test list'
    _TEST_STRING_DELETE = 'this is a test list string extra'
    TEST_LIST_BASE = TEST_STRING_BASE.split()
    TEST_LIST_REPLACE = TEST_STRING_REPLACE.split()
    TEST_LIST_INSERT = _TEST_STRING_INSERT.split()
    TEST_LIST_DELETE = _TEST_STRING_DELETE.split()
    TEST_BASE_LEN = len(TEST_LIST_BASE)
    TEST_OPERATION_LIST_EQUAL = [
        ('nothing', index, index) for index in range(TEST_BASE_LEN)]
    TEST_OPERATION_LIST_REPLACE = TEST_OPERATION_LIST_EQUAL[:-1] + \
        [('replace', TEST_BASE_LEN - 1, TEST_BASE_LEN - 1)]
    TEST_OPERATION_LIST_INSERT = TEST_OPERATION_LIST_EQUAL[:-1] + \
        [('insert', TEST_BASE_LEN - 2, TEST_BASE_LEN - 1)]
    TEST_OPERATION_LIST_DELETE = TEST_OPERATION_LIST_EQUAL + \
        [('delete', TEST_BASE_LEN, TEST_BASE_LEN)]

    def subtract(self, x: str, y: str) -> str:
        return ''.join(x.rsplit(y))
