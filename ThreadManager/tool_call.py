import json


def tool_call_factory(openai_tool_call):
    '''
    Turns an openai_tool_call into a custom one
    '''
    return tool_call(openai_tool_call)

class tool_call():
    '''
    Wraps an openai tool call object to easily expose the function name, arguments, id, and result
    ''' 
    def __init__(self, tool_call):
        """
        Extract the required functions from a tool call.

        Args:
            tool_call: The tool call object.
        """
        self.arguments = json.loads(tool_call.function.arguments)
        self.name = tool_call.function.name
        self.id = tool_call.id
        self.result = None 
    '''
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
    Properties
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
    '''
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name = value

    @property
    def arguments(self):
        return self._arguments
    @arguments.setter
    def arguments(self,value):
        assert(isinstance(value,dict)) #Function arguments need to be as a dictionary to be unpacked correctly
        self._arguments = value

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,value):
        self._id = value

    @property
    def result(self):
        return self._result
    @result.setter
    def result(self,value):
        assert(isinstance(value,str) or value is None) #If not a string openAI will reject it
        self._result = value 
    '''
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    End Properties
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    '''
if __name__ == "__main__":
    call = tool_call()
    print(call)
    exit()
