import unittest
from connectors import * 

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


	def test_connect_instances(self):


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

				def __init__(self):
					self.handler = dict()
					self.handler['serverRecieve'] =  lambda _self = self, key = 'serverRecieve', e = _self.empty: self.add(key, e)
					self.handler['serverReceivedRequest'] = lambda _self = self, key = 'serverRecieve', e = _self.empty: _self.add(key, e)
					self.handler['serverSendCallCount'] = lambda _self = self, key = 'serverRecieve', e = 0: _self.add(key, e)
					self.handler['sendCommandCount'] = lambda _self = self, key = 'serverRecieve', e = 0: _self.add(key, e)
					self.handler['checkResponse'] = lambda _self = self, key = 'serverRecieve', e = 0: _self.add(key, e)

					for key, value in self.handler:
						value()

				def add(self, key, value):
					self.__dict__[key] = value
					return true

				def recieveInfo(self, funcName, value):
					self.handler[funcName](value)


			@Interface(IClientServer.Master, IObserver.Slave)
			class Server():

				empty = 'empty'

				def __init__(self):
					pass

				def send(self, data):
					return data

				def sendCommand(self, command):
					return command
				
				def recieve(self, data):
					print('Server recieve %d ' % data)

				def sendResponse(self, request):
					print('Server accept >> {0}'.format(request))
					return 'Server accept >> {0}'.format(request)


			@Interface(IClientServer.Slave, IObserver.Slave)
			class Client:

				def __init__(self, data):
					self.data = data

				def setMessage(self, mess):
					self.message = mess

				def send(self, data):
					return data

				def readCommand(self, data):
					print('eaa %d' % (data + 1))

				def doRequest(self):
					print('dsfdsfdsf')
					return 'some request'

				def recieve(self, data):
					print('Client recieve %s ' % data)

			connector = Connector()
			server = Server()
			client = Client('I\'m client')
			client.__dict__[str(client.__class__)] = dict()
			client.__dict__[str(client.__class__)][str(server.__class__)] = set()
			client.__dict__[str(client.__class__)][str(server.__class__)].add(IObserver)

			connector.connect(client, server)
			client.send(5435)


if __name__ == '__main__':
	unittest.main()