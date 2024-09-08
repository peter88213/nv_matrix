"""Build the nv_matrix novelibre plugin package.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the nv_matrix project. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copy2
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
from package_builder import PackageBuilder

VERSION = '4.4.1'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_matrix'
    LOCAL_LIB = 'nvmatrixlib'
    GERMAN_TRANSLATION = True

    def add_extras(self):
        self.add_icons()

    def add_icons(self):
        super().add_icons()
        copy2('../icons/mLogo32.png', f'{self.buildDir}/icons')


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
