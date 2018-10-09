import unittest
from connectors import * 


class ConnectorTests(unittest.TestCase):

	def test_base_connector_functionality(self):

		class A_base_connector_functionality():

			def __init__(self):
				self.data = 0

			def handler(self, data):
				self.data = data

		class B_base_connector_functionality():

			def send(self, data):
				return data

		a, b = A_base_connector_functionality(), B_base_connector_functionality()
		connector = Connector()
		connector.connect(b, b.send, a, a.handler)
		b.send(42)
		self.assertEqual(42, a.data)

	def test_connectable_decorator(self):
		
		@Connectable
		class A_test_connectable_decorator():
	
			def sendInfo(self, info):
				return info

		class B_test_connectable_decorator():

			def __init__(self):
				self.info = 'empty'
			
			def infoReader(self, info):
				b.info = info

		a, b = A_test_connectable_decorator(), B_test_connectable_decorator()

		a.sendInfo.connect(b.infoReader)
		a.sendInfo('alcor')
		self.assertEqual('alcor', b.info)

	def test_connect_with_function_without_args(self):

		@Connectable
		class A_connect_with_function_without_args():
			
			def info(self):
				pass

		class B_connect_with_function_without_args():
			
			def __init__(self):
				self.value = 0

			def call(self):
				self.value = 11235

		a, b = A_connect_with_function_without_args(), B_connect_with_function_without_args()
		a.info.connect(b.call)
		a.info()
		self.assertEqual(11235, b.value)


if __name__ == '__main__':
	unittest.main()
