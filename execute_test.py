# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 12:10:07 2024

@author: simulator
"""

import Init_flyout
import RecurrentQTG_auto
import RecurrentQTG_manu
import MQTG_auto
import MQTG_manu
from test_mode import TestMode


def execute_test(test_item, test_dir, mode, gui_output, gui_input):
    if mode == TestMode.REFERENCE:
        Init_flyout.main(test_item, test_dir, gui_output, gui_input)

    elif mode == TestMode.MQTG:
        if test_item['is_automatic']:
            MQTG_auto.main(test_item, test_dir, gui_output, gui_input)
        else:
            MQTG_manu.main(test_item, test_dir, gui_output, gui_input)

    elif mode == TestMode.QTG:
        if test_item['is_automatic']:
            RecurrentQTG_auto.main(test_item, test_dir, gui_output, gui_input)
        else:
            RecurrentQTG_manu.main(test_item, test_dir, gui_output, gui_input)
