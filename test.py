import unittest
import unittest.util

from tests.test_options import TestOptions
from tests.test_instance import TestInstance
from tests.patcher import *

unittest.util._MAX_LENGTH = 2000


if __name__ == '__main__':
    unittest.main()
