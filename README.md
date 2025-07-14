# Learn-Assist Plugin for NVIDIA G-Assist

Transform your gaming PC into a powerful learning companion! This G-Assist plugin leverages context engineering to help students get better AI-powered educational support. Because your gaming PC isn't just for gaming – it's a versatile tool that can support your studies and learning journey.

## What Can It Do?
- 📚 Provide contextual educational support across multiple subjects
- 🎯 Use local markdown files as knowledge base for enhanced AI responses
- 📖 Support for English, Math, Physics, Chemistry, and Biology
- 🔧 Context engineering approach for better small language model performance
- 📝 Easy-to-update content system using simple markdown files
- 💡 Smart question answering using subject-specific educational context

## Open Source Project Information
This learn-assist plugin is an **open source project** developed for the **NVIDIA G-Assist Plugins Hackathon competition**. It was built using the weather plugin example as a reference to demonstrate how gaming PCs can be transformed into powerful educational tools.

The plugin uses a context engineering approach to help G-Assist's Small Language Model provide better learning results, proving that gaming hardware can effectively support students in their academic pursuits.

## 🎮 Why Use Your Gaming PC for Learning?
Your gaming PC has powerful hardware that's perfect for AI-assisted learning:
- **High-performance CPU**: Perfect for running AI models locally
- **Plenty of RAM**: Handles multiple educational resources simultaneously  
- **Fast storage**: Quick access to your learning materials
- **Always available**: Your gaming setup becomes a 24/7 study companion

## 📋 Before You Start
Make sure you have:
- 🖥️ Windows PC (gaming PC recommended!)
- 🐍 Python 3.6 or higher installed
- 🤖 NVIDIA G-Assist installed
- 📁 Basic understanding of markdown files

## 🚀 Quickstart

### 📥 Step 1: Get the Files
```cmd
git clone https://github.com/victortong-git/learn-assist.git
```
This downloads all the necessary files to your computer.

### ⚙️ Step 2: Setup and Build
1. **Run the setup script:**
```cmd
setup.bat
```
This installs all required Python packages automatically.

2. **Run the build script:**
```cmd
build.bat
```
This creates the executable and prepares all necessary files for installation.

### 📦 Step 3: Install the Plugin
1. Navigate to the `dist` folder created by the build script
2. Copy the `learn-assist` folder to:
```cmd
%PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins
```

💡 **Tip**: Make sure all files are copied, including:
- The executable (`learn-assist-plugin.exe`)
- `manifest.json`
- All subject markdown files (`.md` files)

## 📚 How to Use

Once everything is set up, you can get educational help through simple chat commands using the subject prefix syntax.

### 🎯 Command Format
Use the pattern: `[subject] [your question]`

### 📖 Available Subjects
The plugin comes with pre-loaded educational content for:
- **english** - Grammar, writing, literature
- **math** - Algebra, geometry, calculus  
- **physics** - Mechanics, electricity, thermodynamics
- **chemistry** - Atomic structure, chemical reactions, organic chemistry
- **biology** - Cell biology, genetics, ecology

### 💬 Example Commands
Try these commands with G-Assist:

**English:**
- "english What are past participles and how do I use them?"
- "english Explain the difference between active and passive voice"
- "english Help me understand different types of essays"

**Math:**
- "math How do I solve quadratic equations?"
- "math What's the pythagorean theorem and when do I use it?"
- "math Explain derivatives in calculus"

**Physics:**
- "physics What are Newton's three laws of motion?"
- "physics How does electricity work in circuits?"
- "physics Explain the concept of energy conservation"

**Chemistry:**
- "chemistry What's the difference between ionic and covalent bonds?"
- "chemistry How do I balance chemical equations?"
- "chemistry Explain the periodic table organization"

**Biology:**
- "biology How does photosynthesis work?"
- "biology What are the stages of mitosis?"
- "biology Explain DNA structure and function"

### 📋 Example Response
When you ask a question like "english What are past participles?", the plugin will:
1. Load the English educational context from `english.md`
2. Combine it with your specific question
3. Provide a comprehensive, context-aware answer using the educational material

## 🔧 Customizing Your Learning Content

### ➕ Adding New Subjects
1. Create a new markdown file in the plugin directory (e.g., `history.md`)
2. Add your educational content using markdown formatting
3. Update the `manifest.json` if needed
4. Rebuild the plugin using `build.bat`

### ✏️ Updating Existing Content
1. Open any of the subject `.md` files (e.g., `math.md`, `physics.md`)
2. Add or modify content using standard markdown syntax
3. Save the file
4. Rebuild using `build.bat` to apply changes

### 📝 Markdown File Structure
Each subject file should include:
```markdown
# Subject Name

## Main Topics
- Topic 1
- Topic 2

## Detailed Explanations
### Subtopic 1
Content here...

### Subtopic 2
Content here...
```

## 🔍 Troubleshooting Tips

### 📊 Logging
The plugin logs all activity to:
```
%USERPROFILE%\learn-assist-plugin.log
```
Check this file for detailed error messages and debugging information.

### ❗ Common Issues
- **"Subject not found"**: Make sure the markdown file exists and is named correctly
- **"Empty content"**: Check that your markdown file has content
- **Plugin not responding**: Verify the plugin is properly installed in the G-Assist plugins directory

### 🧪 Testing Your Setup
Use the provided test file:
```cmd
how_to_test.md
```
This contains instructions for manually testing your plugin functionality.

## 👨‍💻 Developer Documentation

### 🏗️ Plugin Architecture
The learn-assist plugin is built as a Python-based G-Assist plugin that uses local markdown files as a knowledge base. It follows a context engineering approach where educational content is dynamically loaded and combined with user questions to enhance AI responses.

### 🔧 Core Components

#### Command Handling
- `read_command()`: Reads JSON-formatted commands from G-Assist's input pipe
- `write_response()`: Sends JSON-formatted responses back to G-Assist
- Uses Windows API for secure pipe communication

#### Educational Context Processing
- `get_learning_context()`: Main function that processes learning requests
- Loads subject-specific markdown content
- Combines educational context with student questions
- Returns formatted prompts for enhanced AI responses

### 📋 Available Commands

#### `initialize`
Initializes the plugin and sets up the environment.
- No parameters required
- Returns: `{"success": true, "message": "Learn Assist Plugin initialized"}`

#### `shutdown`
Gracefully terminates the plugin.
- No parameters required
- Returns: `{"success": true, "message": "Learn Assist Plugin shutdown"}`

#### `get_learning_context`
Retrieves educational context for a specified subject and question.
- Parameters:
  ```json
  {
    "subject": "string",  // Required: Subject prefix (english, math, etc.)
    "question": "string"  // Required: Student's question
  }
  ```
- Returns:
  ```json
  {
    "success": true,
    "message": "Formatted educational prompt with context"
  }
  ```

### 🔄 Command Processing
Input Format:
```json
{
    "tool_calls": [
        {
            "func": "get_learning_context",
            "params": {
                "subject": "math",
                "question": "How do I solve quadratic equations?"
            }
        }
    ]
}
```

Output Format:
```json
{
    "success": true,
    "message": "Using the following educational context for math:\n\n[math.md content]\n\nPlease answer this student question: How do I solve quadratic equations?\n\nProvide a clear, educational response that references the context material when relevant."
}
```

### 🛠️ Dependencies
- Python 3.6+
- Standard library modules:
  - json: For message serialization/deserialization
  - logging: For operation logging
  - os: For file path operations
  - ctypes: For Windows API interaction

### ➕ Adding New Educational Functions
To add a new educational function:
1. Implement the function with signature: `def new_function(params: dict = None) -> dict`
2. Add the function to the `commands` dictionary in `main()`
3. Update `manifest.json` with the new function definition
4. Test manually using the testing procedures in `how_to_test.md`
5. Rebuild and reinstall the plugin

## 🚀 Next Steps & Enhancement Ideas
- **📱 Mobile sync**: Sync learning progress across devices
- **🎯 Progress tracking**: Track learning milestones and achievements
- **👥 Study groups**: Collaborative learning features
- **🔍 Smart search**: Advanced content search across all subjects
- **📊 Analytics**: Learning pattern analysis and recommendations
- **🌐 Online resources**: Integration with educational websites and APIs
- **🎨 Interactive content**: Support for images, diagrams, and multimedia
- **🧠 Adaptive learning**: Personalized content based on learning style

## 🤝 Want to Contribute?
We'd love your help making this educational plugin even better! Here's how you can contribute:

- 📝 **Add educational content**: Create new subject markdown files
- 🐛 **Report bugs**: Help us identify and fix issues
- 💡 **Suggest features**: Share ideas for new educational features
- 🔧 **Code contributions**: Improve the plugin functionality
- 📚 **Documentation**: Help improve setup guides and examples

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute.

## 📄 License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- 🏆 **Built for the NVIDIA G-Assist Plugins Hackathon competition**
- 🌦️ **Inspired by the G-Assist weather plugin example**
- 🎮 **Powered by NVIDIA G-Assist technology**
- 📚 **Educational content inspired by standard curriculum guidelines**
- 🔧 **Built with Python and Windows API integration**
- 🤖 **Enhanced by context engineering techniques for better AI responses**

---

*Transform your gaming PC into the ultimate learning companion! 🎮📚*
