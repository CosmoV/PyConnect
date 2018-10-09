import unittest
import connectors_units
import interfaces_units

testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(connectors_units.ConnectorTests))
testSuite.addTest(unittest.makeSuite(interfaces_units.InterfaceTests))

runner = unittest.TextTestRunner()

runner.run(testSuite)
