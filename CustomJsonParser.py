class customJsonParser:
    def __init__(self, data):
        self.data = data
        self.models = []
        self.commands = []

    def getModels(self):
        return self.models

    def getCommands(self):
        return self.commands

    def storeModelsAndCommands(self):
        tempSet = set()
        tempCmdList = []
        for model in self.data['SpecificModels']:
            if 'Ethernet' in model['SupportedItems']['Protocols']:
                tempSet.add(model['Name'])
                tempCmdList += model['SupportedItems']['Commands']
        self.models = list(tempSet)
        self.commands = list(set(tempCmdList))


