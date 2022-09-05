#
# KodeBlox Copyright 2019 Sayak Mukhopadhyay
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http: //www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import functools
import logging
import tkinter as tk
from typing import Optional

import semantic_version
import sys
from theme import theme

import l10n
import myNotebook as nb
from config import config, appname, appversion

plugin_name = "Statistics"

logger = logging.getLogger(f'{appname}.{plugin_name}')

_ = functools.partial(l10n.Translations.translate, context=__file__)

CLIENT_ID = 386149818227097610

VERSION = '3.1.0'

# Add global var for Planet name (landing + around)
statistics: Optional[tk.Frame] = None

this = sys.modules[__name__]  # For holding module globals


def plugin_prefs(parent, cmdr, is_beta):
    """
    Return a TK Frame for adding to the EDMC settings dialog.
    """
    if isinstance(appversion, str):
        core_version = semantic_version.Version(appversion)

    elif callable(appversion):
        core_version = appversion()

    logger.info(f'Core EDMC version: {core_version}')
    if core_version < semantic_version.Version('5.0.0-beta1'):
        logger.info('EDMC core version is before 5.0.0-beta1')
        this.disableStatistics = tk.IntVar(value=config.getint("disable_statistics"))
    else:
        logger.info('EDMC core version is at least 5.0.0-beta1')
        this.disableStatistics = tk.IntVar(value=config.get_int("disable_statistics"))

    frame = nb.Frame(parent)
    nb.Checkbutton(frame, text="Disable Statistics", variable=this.disableStatistics).grid()
    nb.Label(frame, text='Version %s' % VERSION).grid(padx=10, pady=10, sticky=tk.W)

    return frame


def prefs_changed(cmdr, is_beta):
    """
    Save settings.
    """
    config.set('disable_presence', this.disableStatistics.get())


def plugin_start3(plugin_dir):
    return 'Statistics'


def journal_entry(cmdr, is_beta, system, station, entry, state):
    global statistics
    if entry['event'] == 'Statistics':
        exploration_stats = entry['Exploration']
        row = statistics.grid_size()[1]
        new_widget_1 = tk.Label(statistics, text="Total Hyperspace Distance:")
        new_widget_1.grid(row=row, column=0, sticky=tk.W)
        new_widget_2 = tk.Label(statistics, text=exploration_stats["Total_Hyperspace_Distance"])
        new_widget_2.grid(row=row, column=1, sticky=tk.W)
        theme.update(this.frame)


def plugin_app(parent: tk.Frame) -> tk.Frame:
    global statistics
    statistics = tk.Frame(parent)
    return statistics
