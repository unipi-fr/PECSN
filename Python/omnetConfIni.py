import configparser as cp
import re
import ast

class OmnetRunAttr:
    def __init__(self, name, valueString):
        '''
        @name is the name of the attribute
        @valueString a list of values separeted by comma es. "1.0, 2.0, 3.0"
        '''
        self.name = name
        self.__parseValuesString(valueString)
        return
    @staticmethod
    def slpitValueAndUnit(singleValueStr):
        numberRegularExpression = re.compile("[+-]?([0-9]*[.])?[0-9]+")
        textRegularExpression = re.compile("[a-zA-Z]+")

        searchDigit = numberRegularExpression.search(singleValueStr)
        searchText = textRegularExpression.search(singleValueStr)

        digit = ast.literal_eval(searchDigit.group()) if searchDigit else None
        unit = searchText.group() if searchText else None

        return (digit,unit)

    def __parseListValue(self, listValuesStr):
        self.value = list()
        for valueStr in listValuesStr:
            (digit, unit) = self.slpitValueAndUnit(valueStr)
            self.value.append(digit)
            self.unit = unit
        return

    def __parseValuesString(self, valueStr):
        listValues = valueStr.split(",")
        self.__parseListValue(listValues)
        return

    def __str__(self):
        return f"name: '{self.name}', unit: '{self.unit}', value: <{self.value}>"

class OmnetConfIni(cp.ConfigParser):
    def __init__(self, filename = None):
        super().__init__()

        self.__omnetRunAttributes = list()

        if filename is not None:
            self.read(filename)
        return
    
    def __loadOmnetRunAttr(self):
        self.__omnetRunAttributes = list()

        for sectionK in self.sections():
            section = self[sectionK]
            for key in section.keys():
                actualItem = section[key]

                if not actualItem.startswith("$"):
                    continue

                #print(f"[DEBUG] <{key}>: {actualItem}")
                startNameIndex = actualItem.find("{")+1
                endNameIndex = actualItem.find("=")

                name = actualItem[startNameIndex:endNameIndex].strip()

                if endNameIndex == -1: #onlyName
                    #print(f"\t[DEBUG] Skipped, only name -> param '{name}'alredy defined before")
                    continue
                
                values = actualItem[actualItem.find("=")+1:actualItem.find("}")].strip()
                tmpAttr = OmnetRunAttr(name,values)
                self.__omnetRunAttributes.append(tmpAttr)
                #print(f"\t[DEBUG] '{name}'")
                #print(f"\t[DEBUG] '{values}'")
                #print(f'\t[DEBUG] {tmpAttr}')

        return

    def read(self,filename):
        super().read(filename)
        self.__loadOmnetRunAttr()
        print(f"Ini file loaded from: {filename}")
        return 

    def getOmnetRunAttr(self):
        return self.__omnetRunAttributes