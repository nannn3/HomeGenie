from time import sleep
from openai import OpenAI
from datetime import date
import json
import pdb
from Calendar import EventAdder
CONFIG_FILE = 'secrets.json'


class HomeGenie:
    def __init__(self,config_file):
        self.config = self.load_config(config_file)
        self.client = OpenAI(api_key=self.config["openAI_API_key"])
        self.assistant_id = self.config["assistant_id"]
        self.assistant =self.client.beta.assistants.retrieve(
            assistant_id = self.assistant_id
            )

    def load_config(self,config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config
    
    def get_required_functions(self,tool_call):
        arguments = json.loads(tool_call.function.arguments)
        name = tool_call.function.name
        tool_call_id = tool_call.id
        return{"tool_call_id":tool_call_id,'name':name,'arguments':arguments}
    
    
        
    

if __name__ == '__main__':
    genie = HomeGenie(CONFIG_FILE)
    #TODO: This should go in a thread manager class that manages threads by ID
    thread = genie.client.beta.threads.create()
    extra_context = f"The current date is {date.today().weekday()} {date.today()}\n\n"
    run = genie.client.beta.threads.runs.create(
            thread_id = thread.id,
            assistant_id = genie.assistant_id,
            instructions = extra_context + "Scheudle a doctor's appointment next Friday at 9AM"
            )

    while 1: #Poll for completion or required actions:
        run = genie.client.beta.threads.runs.retrieve(
                thread_id = thread.id,
                run_id = run.id
                
                )
        print("Sleeping\n")
        sleep(1)
        if run.status != "in_progress" and run.status != 'queued':
            break;
    
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    required_calls = []
    for tool_call in tool_calls:
        required_calls.append(genie.get_required_functions(tool_call))

    #Create calendar events
    EventAdder=EventAdder.GoogleCalendarEventAdder(CONFIG_FILE)
    events = []
    pdb.set_trace()
    for call in required_calls:
        if call["name"] == "schedule_event":
            args = call['arguments']
            events.append(EventAdder.create_events(**args))
    if len(events) != 0:
        added_events = EventAdder.add_events_to_calendar(events)
        print(added_events)
    
