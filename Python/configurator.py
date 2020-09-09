import omnetDataExtractor as ode 

def getConfiguration():
    print("Loading configuration.json")
    conf = ode.loadJsonFromFile("configuration.json")
    premadeConfigurationKey = conf["USE_PREMADE_CONFIGURATION"]
    if premadeConfigurationKey.isspace():
        return conf
    return conf[premadeConfigurationKey]