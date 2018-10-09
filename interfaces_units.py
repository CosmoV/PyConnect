import unittest
from interfaces import * 


class IClientServer(IInterface):

	simmetricRules = {
		'send' : 'recieve'
	}

	masterRules = {
		'sendCommand' : 'readCommand',
		'sendResponse' : 'recieve'
	}

	slaveRules = {
		'doRequest' : 'sendResponse'
	}


class IObserver(IInterface):

	simmetricRules = {}

	masterRules = {}

	slaveRules = {
		'sendInfo' : 'recieveInfo'
	}


@Interface(IObserver.Master)
class Observer():

	empty = 'empty'
	server = 'server'
	client = 'client'

	def __init__(self, _client, _server):
		self.handler = dict()
		self.handler['serverRecieve'] =  lambda _self = self, key = 'serverRecieve', e = self.empty: self.add(key, e)
		self.handler['serverReceivedRequest'] = lambda _self = self, key = 'serverRecievedRequest', e = self.empty: _self.add(key, e)
		self.handler['serverSendCallCount'] = lambda _self = self, key = 'serverRecieve', e = 0: _self.add(key, e)
		self.handler['sendCommandCount'] = lambda _self = self, key = 'serverRecieve', e = 0: _self.add(key, e)
		self.handler['checkResponse'] = lambda _self = self, key = 'serverRecieve', e = 0: _self.add(key, e)
		self._client = _client
		self._server = _server

		for key, value in self.handler.items():
			value()

	def add(self, key, value):
		self.__dict__[key] = value
		return True


	def recieveInfo(self, message):
		self._server.message = message
		


@Interface(IClientServer.Master, IObserver.Slave)
class Server():

	empty = 'empty'

	def __init__(self, message):
		self.message = message

	def send(self, data):
		return data

	def sendCommand(self, command):
		return command
	
	def recieve(self, message):
		self.send(message)

	def sendResponse(self, request):
		return 'Server accept >> {0}'.format(request)

	def sendInfo(self, *args, **kwargs):
		return (args, kwargs)


@Interface(IClientServer.Slave, IObserver.Slave)
class Client:

	def setMessage(self, mess):
		self.message = mess

	def send(self, message):
		return message

	def readCommand(self, data):
		print('{0}'.format(data))

	def doRequest(self,f):
		return 'some request'

	def recieve(self, message):
		self.sendInfo(message)

	def sendInfo(self, message):
		return message

	def checkAns(self, message):
		self.message = message


class InterfaceTests(unittest.TestCase):

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


	def test_connect_instances(self):

			connector = InterfaceConnector()
			server = Server('default')
			client = Client()
			observer = Observer(client, server)
			client.addUnsupported(Server, IObserver)
			connector.connect(client, server)
			connector.connect(client, observer)
			connector.connect(server, observer)
			client.send('kepler')
			self.assertEqual('kepler', server.message)

if __name__ == '__main__':
	unittest.main()
