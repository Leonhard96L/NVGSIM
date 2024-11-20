# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 12:10:07 2024

@author: simulator
"""

import Init_flyout_V2
import RecurrentQTGs_auto
import RecurrentQTGs_manu


def execute_test(test_item, test_dir, ismqtg, gui_output, gui_input):
    if ismqtg:
        Init_flyout_V2.main(test_item, test_dir, gui_output, gui_input)
    else:
        if test_item['is_automatic']:
            RecurrentQTGs_auto.main(test_item, test_dir, gui_output, gui_input)
        else:
            RecurrentQTGs_manu.main(test_item, test_dir, gui_output, gui_input)
