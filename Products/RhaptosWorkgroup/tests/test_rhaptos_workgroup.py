#------------------------------------------------------------------------------#
#   test_rhaptos_workgroup.py                                                  #
#                                                                              #
#       Authors:                                                               #
#       Rajiv Bakulesh Shah <raj@enfoldsystems.com>                            #
#                                                                              #
#           Copyright (c) 2009, Enfold Systems, Inc.                           #
#           All rights reserved.                                               #
#                                                                              #
#               This software is licensed under the Terms and Conditions       #
#               contained within the "LICENSE.txt" file that accompanied       #
#               this software.  Any inquiries concerning the scope or          #
#               enforceability of the license should be addressed to:          #
#                                                                              #
#                   Enfold Systems, Inc.                                       #
#                   4617 Montrose Blvd., Suite C215                            #
#                   Houston, Texas 77006 USA                                   #
#                   p. +1 713.942.2377 | f. +1 832.201.8856                    #
#                   www.enfoldsystems.com                                      #
#                   info@enfoldsystems.com                                     #
#------------------------------------------------------------------------------#
"""Unit tests.
$Id: $
"""


from Products.RhaptosTest import config
import Products.RhaptosWorkgroup
config.products_to_load_zcml = [('configure.zcml', Products.RhaptosWorkgroup),]
config.products_to_install = ['RhaptosWorkgroup']
config.extension_profiles = ['Products.RhaptosWorkgroup:default']

from Products.RhaptosTest import base


class TestRhaptosWorkgroup(base.RhaptosTestCase):

    def afterSetUp(self):
        self.folder.invokeFactory('Workgroup', 'workgroup')
        self.workgroup = self.folder.workgroup

    def beforeTearDown(self):
        pass

    def test_workgroup_set_title(self):
        # Make sure that setTitle doesn't actually modify the title of the
        # workgroup.
        self.assertFalse(self.workgroup.title)
        self.assertFalse(self.workgroup.Title())
        self.workgroup.setTitle('bunk_title')
        self.assertFalse(self.workgroup.title)
        self.assertFalse(self.workgroup.Title())

    def test_workgroup_set_description(self):
        # Make sure that setDescription doesn't actually modify the description
        # of the workgroup.
        self.assertFalse(self.workgroup.description)
        self.assertFalse(self.workgroup.Description())
        self.workgroup.setDescription('bunk_description')
        self.assertFalse(self.workgroup.description)
        self.assertFalse(self.workgroup.Description())

    def test_workgroup(self):
        self.assertEqual(1, 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRhaptosWorkgroup))
    return suite
