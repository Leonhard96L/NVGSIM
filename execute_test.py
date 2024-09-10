# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 12:10:07 2024

@author: simulator
"""

import Init_flyout
import RecurrentQTGs_auto
import RecurrentQTGs_manu

def execute_test(test_item, ref_dir, test_dir, ismqtg, gui_output, gui_input):
    if ismqtg:
        Init_flyout.main(ref_dir, test_item, gui_output, gui_input)