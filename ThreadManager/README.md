Given how openAI's thread system works, it seems very important to have a dedicated thread manager to poll threads, parse tool calls, and monitor tokens.
At first sketch out, this thread manager must:

* Take user input
* Monitor run status
* Parse tool calls 
* Suplly outputs of tool calls back to threads
* Supply the output of the thread when run status is complete
* Close inactive/failed threads at some point
* Monitor the usage stats and track amount of tokens used.

I might need a class for the tool\_calls that encapulates them and exposes the function name, arguments,id and result. This class can probably inheirt from openai's tool call class and just have getters/setters for the desired properties. 
