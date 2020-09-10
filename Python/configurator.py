import omnetDataExtractor as ode 

def getConfiguration():
    print("Loading configuration.json")
    conf = ode.loadJsonFromFile("configuration.json")
    premadeConfigurationKey = conf["USE_PREMADE_CONFIGURATION"]
    if premadeConfigurationKey.isspace():
        print('Default configuration loaded')
        return conf
    print('Configuration "{conf}" loaded'.format(conf = premadeConfigurationKey ))
    return conf[premadeConfigurationKey]