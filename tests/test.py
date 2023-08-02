import unittest
import ivts

class TestIvts(unittest.TestCase):

    def test_init(self):
        i = ivts.IVTS()
        current = i.I
        self.assertIsNone(current)

if __name__ == "__main__":
    unittest.main()
