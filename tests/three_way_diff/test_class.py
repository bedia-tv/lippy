class TestClass():
    TEST_STRING_BASE = 'script'
    TEST_STRING_REPLACE = 'scripf'
    TEST_STRING_INSERT = 'scrip'
    TEST_STRING_DELETE = 'scripte'
    TEST_LIST_BASE = ['this', 'is', 'a', 'test', 'list', 'string']
    TEST_LIST_REPLACE = ['this', 'is', 'a', 'test', 'list', 'false']
    TEST_LIST_INSERT = ['this', 'is', 'a', 'test', 'list']
    TEST_LIST_DELETE = ['this', 'is', 'a', 'test', 'list', 'string', 'extra']
    TEST_BASE_LEN = len(TEST_STRING_BASE)
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
