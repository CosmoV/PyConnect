import time
import re 
import inspect

from functools import reduce

class ConnectorError(Exception):

	def __init__(self, message = None, body = None, messageDetails = None):
		if not message:
			message = 'Something is wrong'

		self.message = message
		self.body = body
		self.messageDetails = messageDetails

	@property
	def defaulfException(self):
		return ConnectorError()

	@property
	def notImplement(self):
		return ConnectorError('Not implement')

	def __str__(self):
		return '\n***\n<{0}>\n{1} >> {2}\n***'.format(self.message, 'Source' if not self.messageDetails else self.messageDetails,  self.body)


class ConnectableFunctionality():

	pass


def isConnectable(_class):
	try:
		exec('_class.__connectable{0}'.format(_class.__name__))
		return True
	except AttributeError as e:
		return False

def getAttrs(_class):
	return set((i for i in _class.__dict__ if not re.fullmatch(r'__(\w*?)', i)))

def getAllAttrs(_class):
	if _class.__base__ == object:
		return getAttrs(_class)
	else:
		return reduce(lambda i, j: i.union(getAllAttrs(j)), (i for i in _class.__bases__), set()).union(getAttrs(_class))
		

def Connectable(_class):

	_class.__connectable = True
	attrs = getAllAttrs(_class)

	for attr in attrs:
		if callable(eval('_class.{0}'.format(attr))):
			exec('_class.{0} = CallTransferDescriptor(CallTransferRegister(), _class.{0})'.format(attr))

	return _class


class Connector:

	def getWrapper(self):
		
		def packOrigin(original, handler, transfer = False):

			toTransfer, original = (True, transfer) if callable(transfer) else (transfer, original)

			def decorator(*args, __handler = handler, **kwargs):

				__handler(*args, **kwargs)

			def transferDecorator(*args, __original = original, __handler = handler, **kwargs):

				__handler(__original(*args, **kwargs))

			decorator.original = original
			transferDecorator.original = original

			return transferDecorator if toTransfer else decorator

		return packOrigin

	def connect(self, instanceA, methodA, instanceB, methodB):
		sender = self.getWrapper()(methodA, methodB)
		exec('locals()["instanceA"].{0} = sender'.format(methodA.__name__))

	def disconnect(self):
		instance = self.instance
		exec('locals()["instance"].{0} = self.original'.format(self.original.__name__))

		

class CallWpapper():

	def __init__(self, instance, toWrapp):
		
		self.toWrapp = toWrapp
		self.instance = instance
		self.connector = Connector() 
		self.preConnect()

	def preConnect(self):

		def instanceReferenceSaver(self, toWrapp):

			def decorator(*args, __self = self, __wrapped = toWrapp, **kwargs):

				return __wrapped(__self, *args, **kwargs)

			return decorator

		self.wrapped = instanceReferenceSaver(self.instance, self.toWrapp)
		self.wrapped.connect = self.connect
		self.wrapped.disconnect = self.disconnect

	def connect(self, handler):
		self.wrapped = self.connector.getWrapper()(self.wrapped, handler)

	def disconnect(self):
		self.wrapped = self.wrapped.original

	def update(self, toWrapp):
		self.toWrapp = toWrapp
		self.preConnect()

	def __call__(self, *args, **kwargs):
		return self.wrapped(*args, **kwargs)



class CallTransferRegister():

	def __init__(self):
		self.instances = dict()

	def isRegistered(self, instance):
		return instance in self.instances

	def toRegister(self, instance, method):
		self.instances[instance] = CallWpapper(instance, method)

	def unRegister(self, instance):
		pass

	def getWrapped(self, instance):
		return self.instances[instance]

		

class CallTransferDescriptor():

	_connectorDescriptor = True

	def __init__(self, registerInstance, original):
		self.original = original
		self.register = registerInstance

	def toRegister(self, instance):
		if not self.register.isRegistered(instance):
			self.register.toRegister(instance, self.original)

	def __get__(self, instance, owner):
		self.toRegister(instance)
		return self.register.getWrapped(instance)

	def __set__(self, instance, value):
		self.toRegister(instance)
		self.register.update(value)

	def __call__(self, *args, **kwargs):
		return self.wrapped(*args, **kwargs)



class SimpleDescriptor():

	def __get__(self, instance, owner):
		return lambda i: i

class A():

	attr = SimpleDescriptor()

	def bla(self):
		pass