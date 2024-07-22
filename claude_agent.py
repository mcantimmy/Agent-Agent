import os
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.serpapi_tools import SerpApiTools
from phi.tools.python import PythonTools

class AssistantGenerator:
    def __init__(self):
        self.primary_assistant = Assistant(
            name="Primary Assistant",
            llm=OpenAIChat(model="gpt-4"),
            description="An AI that specializes in creating other AI assistants based on user requests."
        )

    def generate_specialized_assistant(self, user_input):
        prompt = f"Create a specialized AI assistant to address the following user request: '{user_input}'. Provide a name, description, and any specific instructions for this assistant. Consider how web search and Python code execution capabilities could be used to fulfill this request."
        response = self.primary_assistant.run(prompt)
        print(response)
        
        # Parse the response to extract assistant details
        lines = response.split('\n')
        name = lines[0].split(': ')[1]
        description = lines[1].split(': ')[1]
        instructions = '\n'.join(lines[2:])
        
        # Create and return the specialized assistant with additional tools
        return Assistant(
            name=name,
            llm=OpenAIChat(model="gpt-4"),
            description=description,
            instructions=instructions,
            tools=[
                SerpApiTools(api_key=os.getenv("SERPAPI_API_KEY")),
                PythonTools(pip_install=True,run_code=True)
            ]
        )

    def process_request(self, user_input):
        # Generate a specialized assistant
        specialized_assistant = self.generate_specialized_assistant(user_input)
        
        # Use the specialized assistant to process the user's request
        result = specialized_assistant.run(user_input)
        
        return result
    
    # Example usage
if __name__ == "__main__":
    generator = AssistantGenerator()
    
    while True:
        user_input = input("Enter your request (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        
        result = generator.process_request(user_input)
        print("\nSpecialized Assistant's Response:")
        print(result)
        print("\n" + "-"*50 + "\n")