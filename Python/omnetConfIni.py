import configparser as cp

class OmnetRunAttr:
    def __init__(self, name, valueString):
        '''
        @name is the name of the attribute
        @valueString can be a scalar or a list of values separeted by comma es. "1.0, 2.0, 3.0"
        '''
        self.name = name
        self.__parseValueString(valueString)
        return
    
    def __parseValueString(self, valueStr):
        listValues = valueStr.split(",")
        if len(listValues) > 1 :
            self.value = listValues
        else:
            self.value = valueStr
        #self.value = 
        return

class OmnetConfIni(cp.ConfigParser):
    def __init__(self, filename = None):
        super().__init__()

        self.__omnetRunVar = dict()

        if filename is not None:
            self.read(filename)
        return
    
    def __loadOmnetRunAttr(self):
        self.__omnetRunVar = dict()

        for sectionK in self.sections():
            section = self[sectionK]
            for key in section.keys():
                actualItem = section[key]
                print(f"[DEBUG] <{key}>: {actualItem}")
        return

    def read(self,filename):
        super().read(filename)
        self.__loadOmnetRunAttr()
        print(f"Ini file loaded from: {filename}")
        return 

    def getOmnetRunAttr(self):
        return self.__omnetRunVar