#!/usr/bin/env python3
"""
Contains the main function used to run the engine
"""

from uci import UniversalChessInterface

"""
[run_manush()] starts and runs the engine.
"""
def run_manush():
    uci = UniversalChessInterface()
    uci.run()

if __name__ == '__main__':
    run_manush()