import unittest
from machinerylib import * 

class ConnectorTest(unittest.TestCase):

	def test_difference_references_to_interfaces_set(self):

		''' Check Interface decorator. Sets of interfaces of different classes should not refer to the same object. '''

		class SimpleInterface(IInterface):
			pass

		@Interface(SimpleInterface)
		class A_difference():
			pass

		@Interface(SimpleInterface)
		class B_difference():
			pass

		self.assertFalse(A_difference.interfacesSet is B_difference.interfacesSet)


	def test_check_master_slave_inheritance(self):

		''' Different classes when attaching an interface must refer to the same object. '''
		
		class SimpleInterface(IInterface):
			pass

		@Interface(SimpleInterface.Master)
		class A_check_ms():
			pass

		@Interface(SimpleInterface.Slave)
		class B_check_ms():
			pass

		@Interface(SimpleInterface.Master)
		class C_check_ms():
			pass	
				
		c_set, a_set, b_set  = C_check_ms.interfacesSet.copy(), A_check_ms.interfacesSet.copy(), B_check_ms.interfacesSet.copy()
		
		self.assertTrue(len(c_set.intersection(b_set)) == 0)

		self.assertTrue(len(c_set.intersection(a_set)) == 1 and (a_set.pop() is c_set.pop()))

		self.assertIs(SimpleInterface.Master, C_check_ms.interfacesSet.copy().pop())


	def test_check_master_slave_inheritance(self):
			pass




if __name__ == '__main__':
	unittest.main()