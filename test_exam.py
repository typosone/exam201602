import unittest
import sys
from io import StringIO, SEEK_SET

from exam import exam, test


class StdIOHook:
    def __init__(self):
        self.held = None

    def set_hook_stdout(self):
        self.held = sys.stdout
        sys.stdout = StringIO()  # type: StringIO

    def release_hook_stdout(self):
        sys.stdout.close()
        sys.stdout = self.held
        self.held = None

    def reset_stdout(self):
        if self.held is not None:
            sys.stdout.truncate(0)
            sys.stdout.seek(0, SEEK_SET)


class TestTest(unittest.TestCase, StdIOHook):
    def setUp(self):
        self.set_hook_stdout()

    def test_test(self):
        test.test()
        self.assertEqual(sys.stdout.getvalue(), 'ok\n')

    def test_test2(self):
        test.test()
        self.assertEqual(sys.stdout.getvalue(), 'ok\n')
        self.reset_stdout()
        test.test2()
        self.assertEqual(sys.stdout.getvalue(), 'ng\n')

    def tearDown(self):
        self.release_hook_stdout()


class ExamTest(unittest.TestCase, StdIOHook):
    def setUp(self):
        self.set_hook_stdout()

    def tearDown(self):
        self.release_hook_stdout()

    def test_hello(self):
        exam.hello('John')
        self.assertEqual(sys.stdout.getvalue(), 'hello, John!\n')

    def test_length(self):
        exam.length('Dive into python3!')
        self.assertEqual(sys.stdout.getvalue(), '18\n')
        self.reset_stdout()
        exam.length('Python Tutorial')
        self.assertEqual(sys.stdout.getvalue(), '15\n')

    def test_slicing2to5(self):
        exam.slicing2to5('Dive into python3!')
        self.assertEqual(sys.stdout.getvalue(), 've \n')
        self.reset_stdout()
        exam.slicing2to5('Python Tutorial')
        self.assertEqual(sys.stdout.getvalue(), 'tho\n')


    def test_number_sign(self):
        exam.number_sign(-3)
        self.assertEqual(sys.stdout.getvalue(), '-\n')
        self.reset_stdout()
        exam.number_sign(0)
        self.assertEqual(sys.stdout.getvalue(), '0\n')
        self.reset_stdout()
        exam.number_sign(10)
        self.assertEqual(sys.stdout.getvalue(), '+\n')

