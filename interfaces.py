from connectors import * 


class InterfaceError(Exception):

	def __init__(self, formatMessage, *args):

		self.formatMessage = formatMessage
		self.args = args

	@classmethod
	def defaulfException(self):
		return ConnectorError()

	@classmethod
	def notImplement(self):
		return ConnectorError('Not implement')

	@classmethod
	def extInterfaceError(self, _class):
		return InterfaceError('Can\'t extend the interface, the passed class is not an interface {0}', _class)
	
	@classmethod
	def notCompability(self, *classes):
		return InterfaceError('dfdsfdsf', *classes)
	
	def __str__(self):
		return formatMessage.format(args)


def isInterface(_class):
	if _class is IInterface:
		return True
	elif _class is object:
		return False
	for baseClass in _class.__bases__:
		if not isInterface(baseClass):
			return False
	return True


def ExtendInterface(*toExtend):
	
	def interfaceExtender(_interface):
		nonlocal toExtend

		PreWrapp = type(_interface.__name__ + '__', (toInheritance), {})
		Wrapped = type(PreWrapp.__name__ + 'Wrapped', (_class, PreWrapp), {})

		for _interface in (_class for _class in toExtend if isInterface(_class)):
			ExtInterface.simmetricRules.update(_interface.simmetricRules)
			ExtInterface.masterRules.update(_interface.masterRules)
			ExtInterface.slaveRules.update(_interface.slaveRules)

		return ExtInterface

	return interfaceExtender

def Interface(*toInheritance):

	def interfaceDecorator(_class):
		nonlocal toInheritance

		PreWrapp = type(_class.__name__ + '__', (toInheritance), {})
		Wrapped = type(PreWrapp.__name__ + 'Wrapped', (_class, PreWrapp), {})

		try:
			Wrapped.interfacesSet
		except AttributeError as e:
			Wrapped.interfacesSet = set()

		for classReference in (__class for __class in toInheritance if isInterface(__class)):
			Wrapped.interfacesSet.add(classReference)
				
		return Wrapped

	return interfaceDecorator

	
class TypeGetter():
	
	def __init__(self, _type):
		self._type = _type

	def __get__(self, instance, owner):

		try:	
			master, slave = owner._master, owner._slave
		except AttributeError as e:
			self.createMaster(owner)
			self.createSlave(owner)

		return owner._master if self._type == IInterface.master else owner._slave


	def transfer(self, owner, suffix):
		
		Wrapped = type(owner.__name__ + suffix, (owner,), {})
		Wrapped._parent = owner
		Wrapped._different = True
		
		return Wrapped

	def createMaster(self, owner):

		Wrapped = self.transfer(owner, 'Master')
		Wrapped._type = Wrapped.master
		owner._master = Wrapped
		

	def createSlave(self, owner):

		Wrapped = self.transfer(owner, 'Slave')
		Wrapped._type = Wrapped.slave
		owner._slave = Wrapped


class ParentReferenceGetter():

	def __get__(self, instance, owner):

		return owner._parent

		
class IInterface:

	master = 'master'
	slave = 'slave'
	neutral = 'neutral'
	notIn = 'notIn'
	_different = False
	_type = neutral
	_parent = object

	def haveAttr(self, attrName):
		return attrName in self.__dict__

	def addAttr(self, attrName, value):
		self.__dict__[attrName] = value

	def toKey(self, source):
		return str(source)

	def appendAttrDict(self, attrName, data):
		if not self.haveAttr(attrName):
			self.__dict__[attrName] = dict()

		copy = self.__dict__[attrName].copy()

		for key, value in rules.items():
			if key not in self.__dict__[attrName]:
				self.__dict__[attrName][key] = value
			else:
				self.__dict__[attrName] = copy
				raise(ConnectorError('Interface collision by rule <{0}>'.format(key), (self.interfaceRules, value)))


	def appendInstanceTypeControlByInterface(self, data):
		typeControl, interface = data[0], data[1]
		if not self.haveAttr('typeControlByInterface'):
			self.typeControlByInterface = set()
		self.typeControlByInterface[str(interface)] = typeControl

	def getInstanceTypeControlByInterface(self, interface):
		if not self.haveAttr('typeControlByInterface'):
			self.typeControlByInterface = 43534
		self.typeControlByInterface

	def appendInterfaceRules(self, rules):
		self.appendAttrDict('interfaceRules', rules)

	def getRules(self):
		if not self.haveAttr('interfaceRules'):
			self.interfaceRules = dict()
		return self.interfaceRules

	def appendMasterInterfaceRules(self, rules):
		self.appendAttrDict('interfaceMasterRules', rules)
	
	def getMasterInterfaceRules(self):
		if not self.haveAttr('interfaceMasterRules'):
			self.interfaceMasterRules = dict()

	def appendSlaveInterfaceRules(self, rules):
		self.appendAttrDict('interfaceSlaveRules', rules)
	
	def getSlaveInterfaceRules(self):
		if not self.haveAttr('interfaceMasterRules'):
			self.interfaceMasterRules = dict()

	

	@classmethod
	def isDifferent(cls):
		return cls._different
	
	@classmethod
	def Parent(cls):
		return cls._parent

	@classmethod
	def typeControl(cls):
		return cls._type

	def connectionIsAllowed(self, _class, interface):
		if not self.haveAttr('unsupportKey'):
			self.addAttr('unsupportKey', self.toKey(self.__class__))
			self.__dict__[self.unsupportKey] = dict()

		key = self.toKey(_class)

		return not (key in self.__dict__[self.unsupportKey] and interface in self.__dict__[self.unsupportKey][key])
		

	def addUnsupported(self, _class, interface):
		if self.connectionIsAllowed(_class, interface):
			key = self.toKey(_class)
			if key not in self.__dict__[self.unsupportKey]:
				self.__dict__[self.unsupportKey][key] = set()

			self.__dict__[self.unsupportKey][key].add(interface)


	def typeControlByInterface(self, interface):
		if interface in self.interfacesSet:
			return self.neutral 
		if interface.Master in self.interfacesSet or interface.Slave in self.interfacesSet:
			return interface.Master if interface.Master in self.interfacesSet else interface.Slave
		return self.notIn


	Master = TypeGetter(master)
	Slave = TypeGetter(slave)

	masterRules = property(getMasterInterfaceRules, appendMasterInterfaceRules)
	slaveRules = property(getSlaveInterfaceRules, appendSlaveInterfaceRules)
	simmetricRules = property(getRules, appendInterfaceRules)
	#transferRules = property(getTransferRules, setTransferRules)
	typeInstance = property(getInstanceTypeControlByInterface, appendInstanceTypeControlByInterface)


class InterfaceConnector():

	def __init__(self):
		self.instances = dict()
		self.connector = Connector()
		self.interfaceConnection = namedtuple('connection', 'instance interface')

	def transfer(self, instance):

		try:
			instance.implemented
			instance._sys_interfacesKeys		
		except AttributeError as e:
			instance._sys_interfacesKeys = dict()
			instance.implemented = dict()

		return instance


	def connectBySpecific(self, instanceA, instanceB, *interfaces):

		self.checkInterfaceCompatibility(instanceA.__class__, instanceB.__class__, IInterface)
		instanceA, instanceB = self.transfer(instanceA), self.transfer(instanceB)		

	def dictInit(self, _dict, key, default = dict()):
		_dict[key] = _dict[key] if key in _dict else default

	def connect(self, instanceA, instanceB):

		interfaces = self.checkCompatibility(instanceA, instanceB)
		instanceA, instanceB = self.transfer(instanceA), self.transfer(instanceB)
		self.dictInit(instanceA._sys_interfacesKeys, instanceB)
		self.dictInit(instanceB._sys_interfacesKeys, instanceA)
		self.mergeByInterfaces(instanceA, instanceB, *interfaces)

	def mergeByInterfaces(self, instanceA, instanceB, *interfaces):

		for interface in interfaces:
			if instanceA.connectionIsAllowed(instanceB.__class__, interface) and instanceB.connectionIsAllowed(instanceA.__class__, interface):
				self.mergeByInterface(instanceA, instanceB, interface)

	def getInterfaces(self, instance):

		try:
			return set((interface if not interface.isDifferent else interface.Parent() for interface in instance.interfacesSet))
		except AttributeError as e:
			return set()

	def mergeByInterface(self, instanceA, instanceB, interface):

		for sender, reciever in interface.simmetricRules.items():
			self._connect(instanceA, instanceB, sender, reciever, interface)
			self._connect(instanceB, instanceA, sender, reciever, interface)

		if instanceA.isDifferent:
			if instanceA.typeControl() != instanceB.typeControl():
				master = instanceA if instanceA.typeControl() == instanceA.master else instanceB
				slave = instanceA if instanceA.typeControl() == instanceA.slave else instanceB
				for sender, reciever in interface.masterRules.items():
					self._connect(master, slave, sender, reciever, interface)
				for sender, reciever in interface.slaveRules.items():
					self._connect(slave, master, sender, reciever, interface)


	def _connect(self, instanceA, instanceB, nameFuncA, nameFuncB, interfaceKey, transfer = False):

		sender, reciever = eval('instanceA.' + nameFuncA), eval('instanceB.' + nameFuncB)
		connector = Connector()
		connector.connect(instanceA, sender, instanceB, reciever, transfer)
		self.dictInit(instanceA._sys_interfacesKeys[instanceB], interfaceKey, set())
		instanceA._sys_interfacesKeys[instanceB][interfaceKey].add(connector)

	def checkCompatibility(self, instanceA, instanceB):

		interfaces = self.getInterfaces(instanceA).intersection(self.getInterfaces(instanceB))

		if not len(interfaces):
			raise ConnectorError('Compatibility interfaces not found', (instanceA, instanceB), 'Classes')

		return interfaces


	def disconnect(self, instanceA, instanceB):
		if instanceB in instanceA._sys_interfacesKeys:
			for key, value in instanceA._sys_interfacesKeys[instanceB].items():
				next(map(lambda e: e.disconnect(), value))



