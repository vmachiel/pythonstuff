import attach
import unittest


class TestKnowValues(unittest.TestCase):

    list_of_test_foldernames = (
        ("hello", "hello_2"),
        ("hello2", "hello2_2"),
        ("hello545", "hello545_2"),
        ("hello904352", "hello904352_2"),
        ("hello1", "hello1_2"),
        ("hello53431", "hello53431_2"),
        ("hello_", "hello_2"),
        ("hello_2", "hello_3"),
        ("hello_4324", "hello_4324_2"),
        ("hello__", "hello__2"),
        ("hello__2", "hello__3"),
        ("hello__4234", "hello__4234_2")
    )

    def test_attach_input_output_conversion(self):
        for oldfolder, newfolder in self.list_of_test_foldernames:
            test_answer = attach.destination_path_correction(oldfolder)
            self.assertEqual(newfolder, test_answer)


if __name__ == '__main__':
    unittest.main()
