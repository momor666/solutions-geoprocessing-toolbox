# coding: utf-8
'''
------------------------------------------------------------------------------
 Copyright 2015 - 2017 Esri
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
------------------------------------------------------------------------------
 TestRunner.py
------------------------------------------------------------------------------
 requirements:
 * ArcGIS Desktop 10.X+ or ArcGIS Pro 1.X+
 * Python 2.7 or Python 3.4
 author: ArcGIS Solutions
 company: Esri
==================================================
 description:
 This test suite collects all of the capability toolbox test suites:
 * HelicopterLandingZoneToolsTestSuite.py
 * ERGToolsTestSuite.py
 * PointOfOriginToolsTestSuite.py

==================================================
 history:
 10/06/2015 - MF - placeholder
 10/30/2015 - MF - tests running
 17/25/2017 - MF - remove deprecated tool tests
==================================================
'''

import os
import sys
import datetime
import logging
import unittest
import arcpy
import Configuration
import UnitTestUtilities
import DataDownload

logFileFromBAT = None
if len(sys.argv) > 1:
    logFileFromBAT = sys.argv[1] #if we have an explicit log file name passed in

def main():
    ''' main test logic '''
    if Configuration.DEBUG == True:
        print("TestRunner.py - main")
    else:
        print("Debug messaging is OFF")

    # setup logger
    logName = None
    if not logFileFromBAT == None:
        logName = logFileFromBAT
        Configuration.Logger = UnitTestUtilities.initializeLogger(logFileFromBAT)
    else:
        logName = UnitTestUtilities.getLoggerName()
        Configuration.Logger = UnitTestUtilities.initializeLogger(logName)
    print("Logging results to: " + str(logName))
    UnitTestUtilities.setUpLogFileHeader()
    
    result = runTestSuite()

    logTestResults(result)

    return result.wasSuccessful()

def logTestResults(result):
    ''' Write the log file '''
    resultHead = resultsHeader(result)
    print(resultHead)
    Configuration.Logger.info(resultHead)
    
    if len(result.errors) > 0:
        rError = resultsErrors(result)
        print(rError)
        Configuration.Logger.error(rError)
        
    if len(result.failures) > 0:
        rFail = resultsFailures(result)
        print(rFail)
        Configuration.Logger.error(rFail)
    Configuration.Logger.info("END OF TEST =========================================\n")

    return

def resultsHeader(result):
    ''' Generic header for the results in the log file '''
    msg = "RESULTS =================================================\n\n"
    msg += "Number of tests run: " + str(result.testsRun) + "\n"
    msg += "Number of errors: " + str(len(result.errors)) + "\n"
    msg += "Number of failures: " + str(len(result.failures)) + "\n"
    return msg

def resultsErrors(result):
    ''' Error results formatting '''
    msg = "ERRORS =================================================\n\n"
    for i in result.errors:
        for j in i:
            msg += str(j)
        msg += "\n"
    return msg

def resultsFailures(result):
    ''' Assert failures formatting '''
    msg = "FAILURES ===============================================\n\n"
    for i in result.failures:
        for j in i:
            msg += str(j)
        msg += "\n"
    return msg

def runTestSuite():
    ''' collect all test suites before running them '''
    if Configuration.DEBUG == True: print("TestRunner.py - runTestSuite")
    testSuite = unittest.TestSuite()
    result = unittest.TestResult()

    #What Platform are we running on?
    Configuration.GetPlatform()
    Configuration.Logger.info(Configuration.Platform + " =======================================")

    testSuite.addTests(addIncidentAnalysisSuite())
    testSuite.addTests(addSunPositionAnalysisSuite())
    testSuite.addTests(addGeoNamesSuite())

    #TODO: Clearing Operations Test Suite
    #TODO: Incident Analysis Test Suite
    #TODO: MAoT Test Suite
    #TODO: MAoW Test Suite
    #TODO: Sun Position Analysis Test Suite

    print("running " + str(testSuite.countTestCases()) + " tests...")

    # Run all of the tests added above
    testSuite.run(result)

    print("Test success: {0}".format(str(result.wasSuccessful())))

    return result

def addIncidentAnalysisSuite():
    ''' Add all IncidentAnalysis tests  '''
    if Configuration.DEBUG == True: print("TestRunner.py - addIncidentAnalysisSuite")
    from incident_analysis_tests import IncidentAnalysisToolsTestSuite
    suite = IncidentAnalysisToolsTestSuite.getTestSuite()
    return suite

def addSunPositionAnalysisSuite():
    ''' Add all SunPositionAnalysis tests '''
    if Configuration.DEBUG == True: print("TestRunner.py - addSunPositionAnalysisSuite")
    from sun_position_analysis_tests import SunPositionAnalysisToolsTestSuite
    suite = SunPositionAnalysisToolsTestSuite.getTestSuite()
    return suite

def addGeoNamesSuite():
    ''' Add all SunPositionAnalysis tests '''
    if Configuration.DEBUG == True: print("TestRunner.py - addGeoNamesSuite")
    from geonames_tests import GeoNamesToolsTestSuite
    suite = GeoNamesToolsTestSuite.getTestSuite()
    return suite

# MAIN =============================================
if __name__ == "__main__":
    if Configuration.DEBUG == True:
        print("TestRunner.py")
    exitAsCode = main()
    if exitAsCode:
        sys.exit(0)
    else:
        sys.exit(1)
