"""
Learn Assist Plugin - A Windows-based plugin that provides educational context from local markdown files.

This plugin communicates through standard input/output pipes and provides educational context
from local markdown files to enhance AI responses for student learning assistance.

The plugin is a service that:
1. Listens for commands through standard input
2. Processes learning context requests by reading markdown files
3. Returns formatted AI prompts through standard output
4. Maintains detailed logging of all operations

Dependencies:
    - ctypes: For Windows API interaction
    - logging: For operation logging
    - json: For message serialization/deserialization
    - os: For file operations

Usage:
    The plugin is designed to be run as a Windows service and communicates through
    standard input/output pipes. It accepts JSON-formatted commands and returns
    JSON-formatted responses.

Example Command Format:
    {
        "tool_calls": [
            {
                "func": "get_learning_context",
                "params": {"subject": "english", "question": "What are past participles?"}
            }
        ]
    }

Example Response Format:
    {
        "success": true,
        "message": "Using the following educational context: [markdown content], please answer this student question: What are past participles?"
    }
"""

import json
import sys
import logging
import os
from ctypes import byref, windll, wintypes
from typing import Optional, Dict, Any

# Type definitions
Response = Dict[bool, Optional[str]]

# Configure logging with a more detailed format
LOG_FILE = os.path.join(os.environ.get('USERPROFILE', '.'), 'learn-assist-plugin.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

def get_learning_context(params: dict = None) -> dict:
    """
    Retrieves educational context from a local markdown file and formats it with the student's question.
    
    Args:
        params (dict, optional): Dictionary containing parameters. Must include 'subject' and 'question' keys.
            Example: {"subject": "english", "question": "What are past participles?"}
        
    Returns:
        dict: A dictionary containing:
            - success (bool): Whether the operation was successful
            - message (str): Formatted AI prompt with educational context or error message
            
    Example:
        >>> get_learning_context({"subject": "english", "question": "What are past participles?"})
        {
            "success": True,
            "message": "Using the following educational context: [english.md content], please answer this student question: What are past participles?"
        }
        
    Raises:
        No exceptions are raised. All errors are caught and returned in the response dict.
    """
    if not params or "subject" not in params or "question" not in params:
        logging.error("Both 'subject' and 'question' parameters are required in get_learning_context")
        return {"success": False, "message": "Both 'subject' and 'question' parameters are required."}
    
    subject = params["subject"]
    question = params["question"]
    
    # Get the directory where the plugin executable is located
    # When running as PyInstaller executable, use sys.executable instead of __file__
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        plugin_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Running as Python script
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
    
    markdown_file = os.path.join(plugin_dir, f"{subject}.md")
    
    try:
        # Check if the markdown file exists
        if not os.path.exists(markdown_file):
            logging.error(f"Markdown file not found: {markdown_file}")
            return {
                "success": False, 
                "message": f"Educational content for subject '{subject}' not found. Available subjects may include: english, math, physics, chemistry, biology."
            }
        
        # Read the markdown file
        with open(markdown_file, 'r', encoding='utf-8') as file:
            educational_content = file.read().strip()
        
        if not educational_content:
            logging.warning(f"Markdown file is empty: {markdown_file}")
            return {
                "success": False,
                "message": f"Educational content for subject '{subject}' is empty."
            }
        
        # Create a formatted prompt that combines the educational context with the student's question
        formatted_prompt = (
            f"Using the following educational context for {subject}:\n\n"
            f"{educational_content}\n\n"
            f"Please answer this student question: {question}\n\n"
            f"Provide a clear, educational response that references the context material when relevant."
        )
        
        logging.info(f"Successfully retrieved learning context for subject: {subject}")
        return {
            "success": True,
            "message": formatted_prompt
        }
        
    except FileNotFoundError:
        logging.error(f"Markdown file not found: {markdown_file}")
        return {
            "success": False,
            "message": f"Educational content for subject '{subject}' not found."
        }
    except PermissionError:
        logging.error(f"Permission denied reading file: {markdown_file}")
        return {
            "success": False,
            "message": f"Permission denied accessing educational content for subject '{subject}'."
        }
    except UnicodeDecodeError as e:
        logging.error(f"Failed to decode markdown file {markdown_file}: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to read educational content for subject '{subject}' due to encoding issues."
        }
    except Exception as e:
        logging.error(f"Unexpected error while retrieving learning context for subject: {subject}. Error: {str(e)}")
        return {
            "success": False,
            "message": f"An unexpected error occurred while accessing educational content: {str(e)}"
        }

def main():
    """
    Main entry point for the learn-assist plugin.
    
    Sets up command handling and maintains the main event loop for processing commands.
    The plugin supports the following commands:
        - initialize: Initializes the plugin
        - shutdown: Terminates the plugin
        - get_learning_context: Retrieves educational context for a subject and question
        
    The function continues running until a shutdown command is received.
    
    Command Processing:
        1. Reads input from standard input
        2. Parses the JSON command
        3. Executes the appropriate function
        4. Writes the response to standard output
        
    Error Handling:
        - Invalid commands are logged and ignored
        - Communication errors are logged
        - All errors are caught and handled gracefully
    """
    INITIALIZE_COMMAND = 'initialize'
    SHUTDOWN_COMMAND = 'shutdown'
    GET_LEARNING_CONTEXT_COMMAND = 'get_learning_context'

    commands = {
        'initialize': lambda _: {"success": True, "message": "Learn Assist Plugin initialized"},
        'shutdown': lambda _: {"success": True, "message": "Learn Assist Plugin shutdown"},
        'get_learning_context': get_learning_context,
    }
    
    logging.info('Learn Assist Plugin started')
    
    while True:
        command = read_command()
        if command is None:
            logging.error('Error reading command')
            continue
        
        tool_calls = command.get("tool_calls", [])
        for tool_call in tool_calls:
            logging.info(f"Tool call: {tool_call}")
            func = tool_call.get("func")
            logging.info(f"Function: {func}")
            params = tool_call.get("params", {})
            logging.info(f"Params: {params}")
            
            if func == INITIALIZE_COMMAND:
                response = commands.get(INITIALIZE_COMMAND, lambda _: {"success": False, "message": "Unknown command"})({})
            elif func == GET_LEARNING_CONTEXT_COMMAND:
                logging.info(f"Getting learning context for {params}")
                response = get_learning_context(params)
                logging.info(f"Learning context response: {response}")
            elif func == SHUTDOWN_COMMAND:
                response = commands.get(SHUTDOWN_COMMAND, lambda _: {"success": False, "message": "Unknown command"})({})
                write_response(response)
                logging.info('Shutdown command received, terminating plugin')
                return
            else:
                response = {'success': False, 'message': f"Unknown function call: {func}"}
            
            write_response(response)
    
def read_command() -> dict | None:
    """ Reads a command from the communication pipe.

    Returns:
        Command details if the input was proper JSON; `None` otherwise
    """
    try:
        STD_INPUT_HANDLE = -10
        pipe = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)

        # Read in chunks until we get the full message
        chunks = []
        while True:
            BUFFER_SIZE = 4096
            message_bytes = wintypes.DWORD()
            buffer = bytes(BUFFER_SIZE)
            success = windll.kernel32.ReadFile(
                pipe,
                buffer,
                BUFFER_SIZE,
                byref(message_bytes),
                None
            )

            if not success:
                logging.error('Error reading from command pipe')
                return None
            
            # Add the chunk we read
            chunk = buffer.decode('utf-8')[:message_bytes.value]
            chunks.append(chunk)

             # If we read less than the buffer size, we're done
            if message_bytes.value < BUFFER_SIZE:
                break

        # Combine all chunks and parse JSON
        retval = ''.join(chunks)
        return json.loads(retval)

    except json.JSONDecodeError:
        logging.error(f'Received invalid JSON: {retval}')
        return None
    except Exception as e:
        logging.error(f'Exception in read_command(): {str(e)}')
        return None


def write_response(response: Response) -> None:
    """ Writes a response to the communication pipe.

    Parameters:
        response: Response
    """
    try:
        STD_OUTPUT_HANDLE = -11
        pipe = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        json_message = json.dumps(response) + '<<END>>'
        message_bytes = json_message.encode('utf-8')
        message_len = len(message_bytes)

        bytes_written = wintypes.DWORD()
        success = windll.kernel32.WriteFile(
            pipe,
            message_bytes,
            message_len,
            bytes_written,
            None
        )

        if not success:
            logging.error('Error writing to response pipe')

    except Exception as e:
        logging.error(f'Exception in write_response(): {str(e)}')


if __name__ == '__main__':
    main()