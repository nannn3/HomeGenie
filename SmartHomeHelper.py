from time import sleep
from openai import OpenAI
from datetime import date
import json
import pdb
from Calendar import EventAdder
from ThreadManager import tool_call
CONFIG_FILE = 'secrets.json'
SLEEP_DELAY = 5

class HomeGenie:
    def __init__(self, config_file):
        """
        Initialize the HomeGenie class.

        Args:
           config_file (str): Path to the configuration file.
        """
        self.config = self.load_config(config_file)
        self.client = OpenAI(api_key=self.config["openAI_API_key"])
        self.assistant_id = self.config["assistant_id"]
        self.assistant = self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id
        )

    def load_config(self, config_file):
        """
        Load the configuration from a JSON file.

        Args:
            config_file (str): Path to the configuration file.

        Returns:
            dict: The loaded configuration.
        """
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config


    def create_thread(self):
        """
        Create a new thread using the OpenAI client.

        Returns:
            object: The created thread.
        """
        return self.client.beta.threads.create()

    def run_thread(self, thread_id, assistant_id, instructions):
        """
        Run a thread with specific instructions.

        Args:
            thread_id: The ID of the thread to run.
            assistant_id: The ID of the assistant to use.
            instructions: The instructions to pass to the thread.

        Returns:
            object: The run object containing the thread status.
        """
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions=instructions
        )

    def retrieve_run_status(self, thread_id, run_id):
        """
        Retrieve the status of a running thread.

        Args:
            thread_id: The ID of the thread.
            run_id: The ID of the run.

        Returns:
            object: The run object containing the updated status.
        """
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

    def create_calendar_events(self, calls):
        """
        Create calendar events based on the required tool calls.

        Args:
            required_calls (list): A list of tool_calls.

        Returns:
            list: A list of added events.
        """
        event_adder = EventAdder.GoogleCalendarEventAdder(CONFIG_FILE)
        created_events =[]
        for call in calls:
            assert(call.name == "schedule_event") # This should be the only name that calls this function
            args = call.arguments
            added = event_adder.add_events_to_calendar([event_adder.create_event(**args)])
            created_events.append(added)
        return created_events
    
    def parse_tool_calls(self,tool_calls):
        '''
        converts openai's toolcalls into custom ones that have important info easily exposed
        Args:
            tools_calls : (list of openAI tool_calls
        Returns: 
            The same list as custom tool_calls
        '''
        return [tool_call.tool_call_factory(call) for call in tool_calls]

        
    def main(self):
        """
        Main function to run the HomeGenie assistant.
        """
        genie = HomeGenie(CONFIG_FILE)
        thread = genie.create_thread()
        extra_context = f"The current date is {date.today().weekday()}, {date.today()}\n\n"
        run = genie.run_thread(
            thread_id=thread.id,
            assistant_id=genie.assistant_id,
            instructions=extra_context + "Schedule a doctor's appointment on August 1st at 9AM"
        )
            
        #TODO Use async polling
        while True:  # Poll for completion or required actions:
            run = genie.retrieve_run_status(
                thread_id=thread.id,
                run_id=run.id
            )
            print("Sleeping\n")
            sleep(SLEEP_DELAY)
            if run.status != "in_progress" and run.status != 'queued':
                break

        #TODO: This is only required if there is actually a required action and the prompt doesn't go straight to completed. 
        # Creating tool calls might have to be done in the thread manager
        print(run.status)
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        pdb.set_trace()
        function_calls = genie.parse_tool_calls(tool_calls)
        # Create calendar events
        added_events = genie.create_calendar_events(required_calls)
        tool_outputs = []
        for event,call in zip(added_events,required_calls):
            output = f'Event {event["summary"]} was added to the calendar on {event["start"]["dateTime"]}'
            print(output)
            tool_outputs.append({"tool_call_id":call['tool_call_id'],"output":output})
            
        if added_events:
            run = genie.client.beta.threads.runs.submit_tool_outputs(
                    thread_id = thread.id,
                    run_id = run.id,
                    tool_outputs = tool_outputs
                    )

            while genie.retrieve_run_status(
                    thread_id = thread.id,
                    run_id = run.id).status != 'completed':
                sleep(SLEEP_DELAY)

            message = self.client.beta.threads.messages.list(thread_id = thread.id)
            print(message.data[0].content[0])


if __name__ == '__main__':
    HomeGenie(CONFIG_FILE).main()
