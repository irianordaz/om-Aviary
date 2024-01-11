import unittest
import copy

from aviary.interface.utils.check_phase_info import check_phase_info
from aviary.interface.default_phase_info.simple import phase_info as phase_info_flops
from aviary.interface.default_phase_info.two_dof import phase_info as phase_info_gasp
from aviary.variable_info.enums import EquationsOfMotion

SIMPLE = EquationsOfMotion.SIMPLE
TWO_DEGREES_OF_FREEDOM = EquationsOfMotion.TWO_DEGREES_OF_FREEDOM


class TestCheckInputs(unittest.TestCase):
    def test_correct_input_simple(self):
        # This should pass without any issue as it's the same valid dict as before
        self.assertTrue(check_phase_info(phase_info_flops, mission_method=SIMPLE))

    def test_incorrect_tuple(self):
        # Let's replace a tuple with a float in the 'climb' phase
        incorrect_tuple_phase_info = copy.deepcopy(phase_info_flops)
        incorrect_tuple_phase_info['climb']['user_options']['initial_altitude'] = 10.668e3
        with self.assertRaises(ValueError):
            check_phase_info(incorrect_tuple_phase_info, mission_method=SIMPLE)

    def test_incorrect_unit(self):
        # Let's replace a valid unit with an invalid one in the 'climb' phase
        incorrect_unit_phase_info = copy.deepcopy(phase_info_flops)
        incorrect_unit_phase_info['climb']['user_options']['initial_altitude'] = (
            10.668e3, 'invalid_unit')
        with self.assertRaisesRegex(ValueError,
                                    "Key initial_altitude in phase climb has an invalid unit invalid_unit."):
            check_phase_info(incorrect_unit_phase_info, mission_method=SIMPLE)

    def test_correct_input_gasp(self):
        # This should pass without any issue as it's the same valid dict as before
        self.assertTrue(check_phase_info(phase_info_gasp,
                        mission_method=TWO_DEGREES_OF_FREEDOM))

    def test_incorrect_mission_method(self):
        # Let's pass an incorrect mission_method name
        incorrect_mission_method = 'INVALID_METHOD'
        with self.assertRaises(ValueError):
            check_phase_info(phase_info_flops, mission_method=incorrect_mission_method)


if __name__ == '__main__':
    unittest.main()
