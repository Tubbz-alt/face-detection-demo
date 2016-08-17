# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Bower plugin just run bower install after copying whole source content.

Copy is performed by inheriting from the dump plugin.
"""

import os
import shutil

import snapcraft
from snapcraft.plugins import dump, nodejs


class BowerPlugin(dump.DumpPlugin, nodejs.NodePlugin):

    def build(self):
        # Setup build and install directory with source ssets
        dump.DumpPlugin.build(self)

        # Call manually the nodejs provisionning as plugins hooks are not
        # idemnpotent and second plugin super() call will recall BasePlugin
        # which removes the directories:
        # https://bugs.launchpad.net/snapcraft/+bug/1595964

        # Install node and bower locally
        self._nodejs_tar.provision(
            self.installdir, clean_target=False, keep_tarball=True)
        self.run(['npm', 'install', '-g', 'bower'])

        # Run bower component install
        self.run(['bower', 'install'], cwd=self.installdir)

        # Remove bower and npm from final installation
        for npmdir in ['bin', 'etc', 'include', 'lib', 'share']:
            shutil.rmtree(os.path.join(self.installdir, npmdir))