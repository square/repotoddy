#!/usr/bin/env python

"""
Created by Wesley Whetstone 03/10/2017

Copyright 2017 Square Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

try:
    from reposadolib import reposadocommon
except ImportError:
    print('Failed to import reposado! Did you symlink it?')
    print ('Please Try. \n `ln -s /path/to/reposado/code/* .`')
    exit()


import imp
import sys
import os
import plistlib
import datetime

PREF_PATH = None


def configure_prefs():
    """Configures prefs for use"""
    _prefs = {}
    keysAndPrompts = [
        ('ReposadoBranchOrderList',
            'Arrange Reposado Branches for automation.'
            '\nTo arrange. (y) \nUse existing. (Enter)'
            '\nExit. (Ctrl-C)'
            '\nCurrent Config:'),
        ('MunkiPkginfoPath', '\nPath to put Apple Software Update pkginfo'
            ' metadata in munki.'),
        ('DaysTillForceInstall', '\nNumber of days from munki import to '
            'set force installs.'),
        ('ForceInstallHour', '\nHour of the day to set munki force install '
            '(24 Hour time).'),
        ('ForceInstallMinute', '\nMinute of the hour to set munki force '
            'install.'),
        ('MunkiCatalog', '\nName of munki catalog for software update'
            ' metadata.')
        ]

    for (key, prompt) in keysAndPrompts:
        newvalue = raw_input('{0} [{1}]: '.format(prompt, pref(key)))
        newvalue = newvalue or pref(key) or ''
        try:
            if key == 'ReposadoBranchOrderList' and newvalue.lower() == 'y':
                cur_branches = reposadocommon.getCatalogBranches().keys()
                newvalue = arrange_branches(cur_branches)
        except AttributeError:
            pass
        _prefs[key] = newvalue or pref(key) or ''
    toddy_plist = pref_file()
    try:
        old_prefs = plistlib.readPlist(toddy_plist)
    except IOError as e:
        old_prefs = {}
    for key, value in old_prefs.iteritems():
        if key not in _prefs.keys():
            _prefs[key] = value
    if _prefs['ReposadoBranchOrderList'] == 'y':
        print('WARNING: Please setup reposado with at least two branches '
              'to use repotoddy...')
        _prefs['ReposadoBranchOrderList'] = []
    plistlib.writePlist(_prefs, toddy_plist)


def get_main_dir():
    '''Returns the directory name of the script or the directory name of the exe
    if py2exe was used
    Code from http://www.py2exe.org/index.cgi/HowToDetermineIfRunningFromExe
    '''
    if (hasattr(sys, 'frozen') or hasattr(sys, 'importers') or
            imp.is_frozen("__main__")):
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])


def pref_file():
  ''' Returns preference file '''
  if PREF_PATH:
    return os.path.abspath(PREF_PATH)

  return os.path.join(get_main_dir(), 'repotoddy_prefs.plist')


def pref(key):
    '''Returns the value of preference key'''
    toddy_plist = pref_file()
    try:
        prefs = plistlib.readPlist(toddy_plist)
    except IOError:
        return ''
    try:
        return prefs[key]
    except Exception as e:
        return ''


def diff_branches(branch_list):
    '''Displays differences between two branches'''
    catalog_branches = reposadocommon.getCatalogBranches()
    for branch in branch_list:
        if branch not in catalog_branches:
            reposadocommon.print_stderr(
                'ERROR: %s is not a valid branch name.' % branch)
            return
    branch1 = set(catalog_branches[branch_list[0]])
    branch2 = set(catalog_branches[branch_list[1]])
    unique_to_first = branch1 - branch2
    if len(unique_to_first) == 0:
        print('No items to move.')


def arrange_branches(branch_list):
    '''user interaction to arrange branches in preferred order'''
    arranged_branches = []
    branch_num = 0
    while len(branch_list) > 0:
        branch_list_len = len(branch_list)
        print('')
        for x in xrange(0, branch_list_len):
            print('{0} = {1}'.format(x, branch_list[x]))
        print('\nFrom the list above.\nSelect the next branch in the order you'
              ' would like repotoddy to process the branches.'
              '\nEnter "n" to exit before using all branches.')
        answer = raw_input('\nEnter Branch Number -->: ')
        try:
            if answer.lower() == 'n':
                return arranged_branches
            ans_type = int(answer)
        except ValueError:
            continue
        if ans_type < branch_list_len:
            # remove the selected number from our list
            item_to_remove = branch_list[ans_type]
            branch_list.remove(item_to_remove)
            arranged_branches.append(item_to_remove)
    return arranged_branches


def get_munki_apple_update_template():
    '''Returns a default template for apple update metadata in munki'''
    pkginfo_template = {
        'catalogs': [''],
        'display_name': '',
        'force_install_after_date': '',
        'installer_type': 'apple_update_metadata',
        'name': '',
        'version': ''
    }
    return pkginfo_template


def time_from_now_in_days(days):
    '''returns a time _days_ in the future'''
    now = datetime.datetime.now()
    days_to_add = datetime.timedelta(days=days)
    future_time = now + days_to_add
    return future_time


def get_force_install():
    '''Returns a date format based on our preferences for when to set a
    force install '''
    forceinstall_days = int(pref('DaysTillForceInstall'))
    forcetime = time_from_now_in_days(forceinstall_days)
    forcehour = int(pref('ForceInstallHour'))
    forceminute = int(pref('ForceInstallMinute'))
    forcetime = forcetime.replace(
        hour=forcehour, minute=forceminute, second=0)
    return forcetime


if __name__ == '__main__':
    ''' ready, set, NOPE '''
    print('Not meant to be run on its own..')
