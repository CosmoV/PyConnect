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
		class A():
	
			def sendInfo(self, info):
				return info

		class B():

			def __init__(self):
				self.info = 'empty'
			
			def infoReader(self, info):
				b.info = info

		a, b = A(), B()

		a.sendInfo.connect(b.infoReader)
		a.sendInfo('alcor')
		self.assertEqual('alcor', b.info)

	def test_connect_with_function_without_args(self):

		@Connectable
		class A():
			
			def info(self):
				pass

		class B():
			
			def __init__(self):
				self.value = 0

			def call(self):
				self.value = 11235

		a, b = A(), B()
		a.info.connect(b.call)
		a.info()
		self.assertEqual(11235, b.value)

	def test_base_connectable_decorator_finctionality(self):

		@Connectable
		class A():
			
			def iTransfer(self, value):
				return value + '_gamma'

		class B():

			def __init__(self):
				self.value = 'beta'

			def iReader(self, value):
				self.value = value

		a, b = A(), B()

		a.iTransfer.connect(b.iReader)
		a.iTransfer('alpha')
		a.iTransfer.disconnect()
		self.assertEqual('alpha', b.value)

		b.value = 'beta'
		a.iTransfer.connect(b.iReader)
		a.iTransfer.disconnect()
		a.iTransfer('alpha')
		self.assertEqual('beta', b.value)

		b.value = 'beta'
		a.iTransfer.connect(b.iReader, transfer = True)
		a.iTransfer('alpha')
		self.assertEqual('alpha_gamma', b.value)


if __name__ == '__main__':
	unittest.main()
