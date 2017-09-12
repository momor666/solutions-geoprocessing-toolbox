#------------------------------------------------------------------------------
# Copyright 2017 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------

import logging
import arcpy
from arcpy.sa import *
import sys
import traceback
import datetime
import os

# Add parent folder to python path if running test case standalone
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import Configuration
import UnitTestUtilities
import DataDownload

class ClearingOperationsNumberFeaturesTestCase(unittest.TestCase):

    toolboxUnderTest = None # Set to Pro or ArcMap toolbox at runtime

    inputArea = None
    pointFeatures = None
    output = None


    scratchGDB = None
    def setUp(self):
        if Configuration.DEBUG == True: print("         ClearingOperationsNumberFeaturesTestCase.setUp")

        ''' Initialization needed if running Test Case standalone '''
        Configuration.GetLogger()
        Configuration.GetPlatform()
        ''' End standalone initialization '''
        self.toolboxUnderTest = Configuration.clearingOperationsToolboxPath

        UnitTestUtilities.checkArcPy()
        DataDownload.runDataDownload(Configuration.clearingOperationsPath, \
           Configuration.clearingOperationsInputGDB, Configuration.clearingOperationsURL)

        if (self.scratchGDB == None) or (not arcpy.Exists(self.scratchGDB)):
            self.scratchGDB = UnitTestUtilities.createScratch(Configuration.clearingOperationsPath)

        # set up inputs
        self.inputArea = os.path.join(Configuration.clearingOperationsInputGDB, r"AO")
        self.pointFeatures = os.path.join(Configuration.clearingOperationsInputGDB, r"Structures")


        UnitTestUtilities.checkFilePaths([Configuration.clearingOperationsPath])

        UnitTestUtilities.checkGeoObjects([Configuration.clearingOperationsInputGDB, self.toolboxUnderTest, self.scratchGDB, self.inputArea, self.pointFeatures])

    def tearDown(self):
        if Configuration.DEBUG == True: print("         ClearingOperationsNumberFeaturesTestCase.tearDown")
        UnitTestUtilities.deleteScratch(self.scratchGDB)

    def testClearingOperationsNumberFeatures(self):
        if Configuration.DEBUG == True:print(".....ClearingOperationsNumberFeaturesTestCase.testClearingOperationsNumberFeatures")
        print("Importing toolbox...")
        arcpy.ImportToolbox(self.toolboxUnderTest)
        arcpy.env.overwriteOutput = True

        #inputs
        fieldToNumber = "number"
        output = os.path.join(self.scratchGDB, "numFields")
        #Testing
        runToolMsg="Running tool (Number Features)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        #try:
        #Calling the NumberFeatures_ClearingOperations Script Tool
        arcpy.NumberFeatures_clrops(self.inputArea, self.pointFeatures, fieldToNumber, output)
        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        result = arcpy.GetCount_management(output)
        count = int(result.getOutput(0))

        cursor = arcpy.SearchCursor(output)
        row = cursor.next()
        val = row.getValue(fieldToNumber)
        print("Field number first row: " + str(val) + " should not be null")

        self.assertIsNotNone(val)

        print("number features: " + str(count))
        self.assertEqual(count, 90)

if __name__ == "__main__":
    unittest.main()       