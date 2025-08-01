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
LOG_FILE = os.path.join(os.environ.get('USERPROFILE', '.'), 'learnassist-plugin.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

def process_educational_question(question: str, content: str, subject: str) -> str:
    """
    Processes a student's question using educational content and returns a focused answer.
    Similar to how weather plugin processes API data to return focused weather info,
    or stock plugin processes market data to return focused stock prices.
    
    Args:
        question (str): The student's question
        content (str): The educational content from markdown file
        subject (str): The subject area (english, math, etc.)
        
    Returns:
        str: Focused educational answer based on the content
    """
    question_lower = question.lower().strip()
    
    # Parse what the student is asking about
    topic_keywords = {
        'adjective': ['adj', 'adjective', 'adjectives'],
        'noun': ['noun', 'nouns'],
        'verb': ['verb', 'verbs'], 
        'adverb': ['adverb', 'adverbs'],
        'tense': ['tense', 'tenses'],
        'grammar': ['grammar', 'punctuation'],
        'photosynthesis': ['photosynthesis'],
        'respiration': ['respiration', 'cellular respiration'],
        'cell': ['cell', 'cells'],
        'atom': ['atom', 'atomic', 'atoms'],
        'element': ['element', 'elements'],
        'force': ['force', 'forces'],
        'newton': ['newton', 'law'],
        'energy': ['energy', 'kinetic', 'potential'],
        'motion': ['motion', 'velocity', 'acceleration'],
        'fraction': ['fraction', 'fractions'],
        'algebra': ['algebra', 'equation', 'solve'],
        'geometry': ['geometry', 'triangle', 'circle', 'area']
    }
    
    # Find what topic they're asking about
    for topic, keywords in topic_keywords.items():
        if any(keyword in question_lower for keyword in keywords):
            # Extract and format the relevant information
            answer = extract_topic_info(content, topic, keywords)
            if answer:
                return answer
    
    # If no specific topic found, provide a subject-specific helpful response
    subject_examples = {
        'eng': 'nouns, verbs, adjectives, adverbs, tenses',
        'english': 'nouns, verbs, adjectives, adverbs, tenses',
        'math': 'fractions, algebra, geometry, equations',
        'mathematics': 'fractions, algebra, geometry, equations',
        'phy': 'forces, energy, motion, newton laws',
        'physics': 'forces, energy, motion, newton laws',
        'chem': 'atoms, elements, molecules, reactions',
        'chemistry': 'atoms, elements, molecules, reactions',
        'bio': 'cells, photosynthesis, respiration, genetics',
        'biology': 'cells, photosynthesis, respiration, genetics'
    }
    
    examples = subject_examples.get(subject.lower(), 'specific concepts')
    return f"I can help with {subject} topics. Try asking about specific concepts like {examples}."

def extract_topic_info(content: str, topic: str, keywords: list) -> str:
    """
    Extracts relevant information about a specific topic from educational content.
    Returns a focused, formatted answer like other plugins do.
    """
    lines = content.split('\n')
    topic_section = []
    capturing = False
    section_started = False
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line.lower()
        
        # Start capturing when we find the topic
        if any(keyword in line_lower for keyword in keywords):
            capturing = True
            topic_section.append(line_clean)
            section_started = True
        elif capturing:
            # Continue capturing until we hit another major section
            if line_clean.startswith('##') and not any(keyword in line_lower for keyword in keywords):
                # Hit different section, but only stop if we've captured some content
                if section_started and len([l for l in topic_section if l.startswith('-')]) > 0:
                    break
                else:
                    # This might be a related section, continue
                    topic_section.append(line_clean)
            elif line_clean.startswith('**') and not any(keyword in line_lower for keyword in keywords):
                # Hit different topic within same section, but only stop if we have substantial content
                if len([l for l in topic_section if l.startswith('-')]) >= 3:
                    break
                else:
                    # Continue capturing - might be related content
                    topic_section.append(line_clean)
            elif line_clean.startswith('-') or line_clean == '' or not line_clean.startswith('#'):
                # Continue capturing content within this topic
                topic_section.append(line_clean)
        
        # Stop if we have enough content (about 6-10 lines of actual content)
        content_lines = [l for l in topic_section if l and not l.startswith('#') and not l.startswith('**')]
        if capturing and len(content_lines) >= 10:
            break
    
    if topic_section:
        # Format the response like other plugins - clean and focused
        result = '\n'.join(topic_section).strip()
        # Remove excessive blank lines
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        return result
    
    return ""

def get_learning_context(params: dict = None) -> dict:
    """
    Processes a student's educational question and returns a focused answer.
    Similar to how weather plugin processes weather data or stock plugin processes stock data.
    
    Args:
        params (dict, optional): Dictionary containing parameters. Must include 'subject' and 'question' keys.
            Example: {"subject": "english", "question": "What are adjectives?"}
        
    Returns:
        dict: A dictionary containing:
            - success (bool): Whether the operation was successful
            - message (str): Focused educational answer or error message
            
    Example:
        >>> get_learning_context({"subject": "english", "question": "What are adjectives?"})
        {
            "success": True,
            "message": "**Adjectives (adj)**\n- Describe or modify nouns\n- Examples: big, small, red, happy, beautiful, interesting\n- Usage: \"The big dog\" / \"She is happy\" / \"It's a beautiful day\""
        }
        
    Raises:
        No exceptions are raised. All errors are caught and returned in the response dict.
    """
    if not params or "subject" not in params or "question" not in params:
        logging.error("Both 'subject' and 'question' parameters are required in get_learning_context")
        return {"success": False, "message": "Both 'subject' and 'question' parameters are required."}
    
    subject = params["subject"]
    question = params["question"]
    
    # Map both short and long subject names to correct file names for easier student use
    subject_mapping = {
        'eng': 'eng',
        'english': 'eng',
        'math': 'math',
        'mathematics': 'math',
        'phy': 'phy', 
        'physics': 'phy',
        'chem': 'chem',
        'chemistry': 'chem',
        'bio': 'bio',
        'biology': 'bio'
    }
    
    # Get the actual file name to use
    file_subject = subject_mapping.get(subject.lower(), subject)
    
    # Get the directory where the plugin executable is located
    # When running as PyInstaller executable, use sys.executable instead of __file__
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        plugin_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Running as Python script
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
    
    markdown_file = os.path.join(plugin_dir, f"{file_subject}.md")
    
    try:
        # Check if the markdown file exists
        if not os.path.exists(markdown_file):
            logging.error(f"Markdown file not found: {markdown_file}")
            return {
                "success": False, 
                "message": f"Educational content for subject '{subject}' not found. Available subjects: eng/english, math, phy/physics, chem/chemistry, bio/biology."
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
        
        # Process the educational question and return focused answer like other plugins
        educational_answer = process_educational_question(question, educational_content, subject)
        
        logging.info(f"Successfully processed educational question for subject: {subject}")
        return {
            "success": True,
            "message": educational_answer
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
        'initialize': lambda _: {"success": True, "message": "Plugin initialized"},
        'shutdown': lambda _: {"success": True, "message": "Plugin shutdown"},
        'get_learning_context': get_learning_context,
    }
    
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
                response = commands.get(INITIALIZE_COMMAND, lambda _: {"success": False, "message": "Unknown command"})()
            elif func == GET_LEARNING_CONTEXT_COMMAND:
                logging.info(f"Getting learning context for {params}")
                response = get_learning_context(params)
                logging.info(f"Learning context: {response}")
            elif func == SHUTDOWN_COMMAND:
                response = commands.get(SHUTDOWN_COMMAND, lambda _: {"success": False, "message": "Unknown command"})()
                write_response(response)
                return
            else:
                response = {'success': False, 'message': "Unknown function call"}
            
            write_response(response)
    
def read_command() -> dict | None:
    ''' Reads a command from the communication pipe.

    Returns:
        Command details if the input was proper JSON; `None` otherwise
    '''
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
        logging.error(f'Received invalid JSON (length: {len(retval)}): {retval[:500]}...')
        return None
    except Exception as e:
        logging.error(f'Exception in read_command(): {str(e)}')
        return None


def write_response(response:Response) -> None:
    ''' Writes a response to the communication pipe.

    Parameters:
        response: Response
    '''
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