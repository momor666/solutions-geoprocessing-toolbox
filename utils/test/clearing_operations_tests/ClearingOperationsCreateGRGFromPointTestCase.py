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

class ClearingOperationsCreateGRGFromPointTestCase(unittest.TestCase):

    toolboxUnderTest = None # Set to Pro or ArcMap toolbox at runtime

    pointTarget = None
    inputArea = None
    output = None


    scratchGDB = None
    def setUp(self):
        if Configuration.DEBUG == True: print("         ClearingOperationsCreateGRGFromPointTestCase.setUp")

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
        self.pointTarget = os.path.join(Configuration.clearingOperationsInputGDB, r"CenterPoint")
        self.inputArea = os.path.join(Configuration.clearingOperationsInputGDB, r"AO")

        UnitTestUtilities.checkFilePaths([Configuration.clearingOperationsPath])

        UnitTestUtilities.checkGeoObjects([Configuration.clearingOperationsInputGDB, self.toolboxUnderTest, self.scratchGDB, self.pointTarget, self.inputArea])

    def tearDown(self):
        if Configuration.DEBUG == True: print("         ClearingOperationsCreateGRGFromPointTestCase.tearDown")
        UnitTestUtilities.deleteScratch(self.scratchGDB)

    def testClearingOperationsPointTarget(self):
        if Configuration.DEBUG == True:print(".....ClearingOperationsCreateGRGFromPointTestCase.testClearingOperationsPointTarget")
        print("Importing toolbox...")
        arcpy.ImportToolbox(self.toolboxUnderTest)
        arcpy.env.overwriteOutput = True

        #inputs
        numCellsH = 9
        numCellsV = 9
        cellWidth = 100
        cellHeight = 100
        cellUnits = "Meters"
        labelStart = "Lower-Left"
        labelStyle = "Alpha-Numeric"
        labelSeparator = "-" # Only used for Alpha-Alpha but required parameter?
        gridRotationAngle = 0

        output = os.path.join(self.scratchGDB, "ptTarget")

        #Testing
        runToolMsg="Running tool (Point Target)"
        arcpy.AddMessage(runToolMsg)
        Configuration.Logger.info(runToolMsg)

        try:
            # Calling the PointTargetGRG_ClearingOperations Script Tool
            arcpy.CreateGRGFromPoint_clrops(self.pointTarget, \
                numCellsH, numCellsV, \
                cellWidth, cellHeight, "Meters", \
                labelStart, labelStyle, labelSeparator, gridRotationAngle, \
                output)

        except arcpy.ExecuteError:
            UnitTestUtilities.handleArcPyError()
        except:
            UnitTestUtilities.handleGeneralError()

        result = arcpy.GetCount_management(output)
        count = int(result.getOutput(0))
        print("number features: " + str(count))
        self.assertGreaterEqual(count, 80)

        #TODO: determine if should be added back in
        #cursor = arcpy.da.SearchCursor(output, 'SHAPE@')
        #cursor2 = arcpy.da.SearchCursor(self.pointTarget, 'SHAPE@')
        #ptRow = cursor2.next()
        #ptGeo = ptRow[0]
        #intersect = False
        #for row in cursor:
        #    intersectFeat= row[0].touches(ptGeo)
        #    #print(str(intersectFeat))
        #    if intersectFeat == True:
        #        intersect = True
        #self.assertTrue(intersect)

if __name__ == "__main__":
    unittest.main()       
