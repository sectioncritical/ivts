import unittest
import ivts

class TestIvtsEncoder(unittest.TestCase):

    def test_init(self):
        enc = ivts.Encoder()
        self.assertIsNotNone(enc)

    def test_config_u1_nominal(self):
        enc = ivts.Encoder()
        res = enc.set_config(ivts.MeasureType.U1, ivts.TriggerMode.CYCLIC,
                1000)
        expected = bytes([0x21, 2, 0x03, 0xE8, 0, 0, 0, 0])
        self.assertEqual(0x411, res[0])
        self.assertEqual(expected, res[1])

    def test_trigger(self):
        enc = ivts.Encoder()
        res = enc.trigger([ivts.MeasureType.As, ivts.MeasureType.U1])
        expected = bytes([0x31, 0, 0x42, 0, 0, 0, 0, 0])
        self.assertEqual(0x411, res[0])
        self.assertEqual(expected, res[1])

    def test_store(self):
        enc = ivts.Encoder()
        res = enc.store()
        expected = bytes([0x32, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(0x411, res[0])
        self.assertEqual(expected, res[1])

    def test_set_mode_run_stop(self):
        enc = ivts.Encoder()
        res = enc.set_run_mode(immed_is_run=True, startup_is_run=False)
        expected = bytes([0x34, 1, 0, 0, 0, 0, 0, 0])
        self.assertEqual(0x411, res[0])
        self.assertEqual(expected, res[1])

    def test_set_mode_stop_run(self):
        enc = ivts.Encoder()
        res = enc.set_run_mode(immed_is_run=False, startup_is_run=True)
        expected = bytes([0x34, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(0x411, res[0])
        self.assertEqual(expected, res[1])

if __name__ == "__main__":
    unittest.main()
