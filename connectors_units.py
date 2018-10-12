import unittest
from connectors import * 



class ConnectorTests(unittest.TestCase):

	def setUp(self):

		@Connectable
		class A():
			
			def iSender(self, value):
				return value + '_gamma'

		class B():

			def __init__(self):
				self.value = 'beta'

			def iReader(self, value):
				self.value = value

			def clear(self):
				self.value = 'space'

		self.A, self.B = A, B

	def test_base_connector_functionality(self):

		a, b = self.A(), self.B()
		connector = Connector()
		connector.connect(a, a.iSender, b, b.iReader)
		a.iSender('42')
		self.assertEqual('42', b.value)

	def test_connectable_decorator(self):

		a, b = self.A(), self.B()
		a.iSender.connect(b.iReader)
		a.iSender('alcor')
		self.assertEqual('alcor', b.value)

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

		a, b = self.A(), self.B()

		a.iSender.connect(b.iReader)
		a.iSender('alpha')
		self.assertEqual('alpha', b.value)
		a.iSender.disconnect()

		b.value = 'beta'
		a.iSender.connect(b.iReader)
		a.iSender.disconnect()
		a.iSender('alpha')
		self.assertEqual('beta', b.value, 'check disconnect')

		b.value = 'beta'
		a.iSender.connect(b.iReader, transfer = True)
		a.iSender('alpha')
		self.assertEqual('alpha_gamma', b.value)
		a.iSender.disconnect()
		
		def logger(value):
			return value + '_log'

		b.value = 'beta'
		a.iSender.connect(b.iReader, transfer = logger)
		a.iSender('alpha')
		self.assertEqual('alpha_log', b.value)

	def test_multy_subscribe(self):

		a, b, c = self.A(), self.B(), self.B()

		b.value, c.value = '_', '_'
		a.iSender.connect(b.iReader)
		a.iSender.connect(c.iReader)
		a.iSender('Jo')
		#self.assertEqual('JoJo', b.value + c.value)
		
		a.iSender.disconnect()

		a.iSender.addSubscriber(b.iReader)
		a.iSender('mercurial')
		self.assertEqual('mercurial', b.value)
		a.iSender.unsubscribe(b.iReader)
		a.iSender('Jo')
		self.assertEqual('mercurial', b.value)



if __name__ == '__main__':
	unittest.main()
