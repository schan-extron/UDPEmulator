class customJsonParser:
    def __init__(self, data):
        self.data = data
        self.models = []
        self.commands = dict()
        self.ethernetType = ''
        self.port = ''

    def getModels(self):
        return self.models

    def getCommands(self):
        return self.commands

    def getEtherentType(self):
        return self.ethernetType

    def getPort(self):
        return self.port

    def storePortAndType(self):
        # Traverse through the list of protocols
        for index in range(0, self.data['Protocols'].__len__()):
            # If EthernetType key exists in the dicionary index, then check if UDP or HTTP is available
            if 'EthernetType' in self.data['Protocols'][index]:
                if 'HTTP' in self.data['Protocols'][index]['EthernetType'] or 'UDP' in self.data['Protocols'][index]['EthernetType']:
                    #
                    self.port = str(self.data['Protocols'][index]['Port'])
                    self.ethernetType = self.data['Protocols'][index]['EthernetType'].strip('Ethernet_')
                    break

    def storeModelsAndCommands(self):
        tempSet = set()
        tempCmdList = set()
        tempCmdAndStateDict = {}

        # Add list of models to a set
        for model in self.data['Models']['SpecificModels']:
            # Only add the model if Ethernet is supported
            if 'Ethernet' in model['SupportedItems']['Protocols']:
                tempSet.add(model['Name'])
                # Add supported commands for each model to a temporary list
                for i in model['SupportedItems']['Commands']:
                    tempCmdList.add(i)

        # Traverse through the list of all available commands
        for commandIndex in self.data['Commands']:
            # Store the list of Parameters into temp variable. Some lists can come back empty
            tempLiveList = commandIndex['Parameters']
            if commandIndex['InternalName'] in tempCmdList and tempLiveList:
                # If Live is true, then start storing the states of the command
                if tempLiveList[0]['Live']:
                    # For commands with states, the value of each key will be a LIST
                    # Check if EnumStates exists (only for commands with enum parameter)
                    if 'EnumStates' in commandIndex['Parameters'][0]:
                        tempStateList = []
                        # Traverse through list to grab the enum states
                        for states in commandIndex['Parameters'][0]['EnumStates']:
                            # Append the states to a temporary list
                            tempStateList.append(states['Name'])
                        # Add the temporary list to a dictionary, using the command name as the key
                        tempCmdAndStateDict[commandIndex['InternalName']] = tempStateList
                    # For commands with number value parameters, the value of each key will be a DICTIONARY
                    else:
                        # Create a dictionary to hold temp values
                        tempDict = {
                            'Max' : commandIndex['Parameters'][0]['Max'],
                            'Min' : commandIndex['Parameters'][0]['Min'],
                            'Step' : commandIndex['Parameters'][0]['Interval'],
                        }
                        tempCmdAndStateDict[commandIndex['InternalName']] = tempDict
                    # Case of string value parameter?

        self.models = list(tempSet)
        self.commands = tempCmdAndStateDict
        print('CUSTOMJSONPARSER DONE')