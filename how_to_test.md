# How to Test the Learn-Assist Plugin

This guide explains how to test the learn-assist plugin with various input examples and what to expect from the outputs.

## 📋 Overview

The learn-assist plugin provides educational context to enhance AI responses for secondary school students across five subjects: English, Math, Physics, Chemistry, and Biology.

## 🔧 Testing Setup

### Prerequisites
1. **Plugin is built**: Run `setup.bat` then `build.bat` to create executable
2. **Executable location**: `dist\learn-assist\learn-assist-plugin.exe`
3. **Educational files present**: All .md files copied to `dist\learn-assist\` folder
4. **Windows Command Prompt**: For testing with echo and pipes

### Test Environment
- **Testing Method**: Windows Command Line with echo and pipes
- **Plugin Communication**: JSON over stdin/stdout
- **Executable**: `learn-assist-plugin.exe`
- **Output**: Enhanced AI prompts with educational context

### Build Process
```cmd
cd plugins\learn-assist
setup.bat
build.bat
```

After building, the plugin will be available at:
```
plugins\learn-assist\dist\learn-assist\learn-assist-plugin.exe
```

## 📝 Test Cases by Subject

### 1. English Subject Tests

#### Test Case 1.1: Grammar Question

**Windows Command Line Test:**
```cmd
cd dist\learn-assist
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"What are past participles and how do I use them?"}}]} | learn-assist-plugin.exe
```

**Alternative with file (for complex questions):**
```cmd
cd dist\learn-assist
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"What are past participles and how do I use them?"}}]} > test_input.json
learn-assist-plugin.exe < test_input.json
```

**Expected Plugin Output:**
```json
{
  "success": true,
  "message": "Using the following educational context for english:\n\n[COMPLETE ENGLISH.MD CONTENT - 11,150 bytes]\n\nPlease answer this student question: What are past participles and how do I use them?\n\nProvide a clear, educational response that references the context material when relevant."
}
```

**Output Verification:**
- Check output starts with `{"success":true`
- Verify message contains "# English Language Learning Guide"
- Confirm output size is approximately 11,300+ characters
- Look for specific content like "Past Participles - Complete Guide"

**Expected AI Enhancement:**
- Should reference verb tense explanations from content
- Include examples of regular and irregular past participles
- Mention perfect tenses, passive voice, and adjectival uses
- Provide grade-appropriate explanations with examples

#### Test Case 1.2: Writing Skills

**Windows Command Line Test:**
```cmd
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"How do I write a strong thesis statement?"}}]} | learn-assist-plugin.exe
```

**Expected AI Enhancement:**
- Reference essay structure guidelines from content
- Include five-paragraph essay format
- Mention argumentative essay requirements
- Provide thesis statement examples and templates

#### Test Case 1.3: Literature Analysis

**Windows Command Line Test:**
```cmd
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"What are the different types of conflict in stories?"}}]} | learn-assist-plugin.exe
```

**Expected AI Enhancement:**
- Reference literary elements section
- List: Person vs. Person, Person vs. Self, Person vs. Nature, Person vs. Society
- Include examples and explanations for each type
- Connect to story elements and character development

### 2. Math Subject Tests

#### Test Case 2.1: Algebra Question

**Windows Command Line Test:**
```cmd
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"math","question":"How do I solve quadratic equations?"}}]} | learn-assist-plugin.exe
```

**Expected Plugin Output Size:** ~10,800 characters

**Expected AI Enhancement:**
- Reference multiple solving methods (factoring, quadratic formula, completing square)
- Include step-by-step examples
- Mention discriminant and solution types
- Provide practice strategies

#### Test Case 2.2: Geometry Question

**Windows Command Line Test:**
```cmd
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"math","question":"How do I find the area of different shapes?"}}]} | learn-assist-plugin.exe
```

**Expected AI Enhancement:**
- Reference geometry formulas section
- Include rectangle, triangle, circle area formulas
- Provide worked examples
- Connect to real-world applications

#### Test Case 2.3: Word Problems

**Windows Command Line Test:**
```cmd
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"math","question":"How do I solve word problems step by step?"}}]} | learn-assist-plugin.exe
```

**Expected AI Enhancement:**
- Reference problem-solving strategies section
- Include the 6-step method
- Provide examples of different word problem types
- Include tips for translating words to math

### 3. Physics Subject Tests

#### Test Case 3.1: Mechanics Question
**Student Input:**
```
learn-assist physics What is Newton's second law and how do I use it?
```

**Expected Plugin Output Size:** ~13,400 characters

**Expected AI Enhancement:**
- Reference Newton's laws section
- Explain F = ma with examples
- Include free body diagram guidance
- Provide problem-solving strategies

#### Test Case 3.2: Motion Question
**Student Input:**
```
learn-assist physics How do I solve projectile motion problems?
```

**Expected AI Enhancement:**
- Reference kinematics and projectile motion sections
- Explain horizontal vs. vertical motion independence
- Include relevant equations and examples
- Connect to real-world scenarios

### 4. Chemistry Subject Tests

#### Test Case 4.1: Chemical Equations
**Student Input:**
```
learn-assist chemistry How do I balance chemical equations?
```

**Expected Plugin Output Size:** ~10,400 characters

**Expected AI Enhancement:**
- Reference chemical reactions section
- Include step-by-step balancing method
- Provide examples of different reaction types
- Include common mistakes to avoid

#### Test Case 4.2: Atomic Structure
**Student Input:**
```
learn-assist chemistry What's the difference between atoms, molecules, and ions?
```

**Expected AI Enhancement:**
- Reference atomic structure section
- Explain protons, neutrons, electrons
- Define cations and anions with examples
- Connect to periodic table concepts

### 5. Biology Subject Tests

#### Test Case 5.1: Cell Biology
**Student Input:**
```
learn-assist biology What are the main parts of a cell and their functions?
```

**Expected Plugin Output Size:** ~10,800 characters

**Expected AI Enhancement:**
- Reference cell structure section
- Distinguish prokaryotic vs. eukaryotic cells
- List organelles and their functions
- Include plant vs. animal cell differences

#### Test Case 5.2: Genetics
**Student Input:**
```
learn-assist biology How does DNA replication work?
```

**Expected AI Enhancement:**
- Reference genetics section
- Explain base pairing and double helix
- Include steps of replication process
- Connect to cell division concepts

## 🚨 Error Test Cases

### Test Case E.1: Invalid Subject
**Student Input:**
```
learn-assist history What caused World War I?
```

**Expected Plugin Output:**
```json
{
  "success": false,
  "message": "Educational content for subject 'history' not found. Available subjects may include: english, math, physics, chemistry, biology."
}
```

### Test Case E.2: Missing Parameters
**Plugin Input:**
```json
{
  "tool_calls": [
    {
      "func": "get_learning_context",
      "params": {
        "subject": "english"
      }
    }
  ]
}
```

**Expected Plugin Output:**
```json
{
  "success": false,
  "message": "Both 'subject' and 'question' parameters are required."
}
```

### Test Case E.3: Empty Question
**Student Input:**
```
learn-assist math 
```

**Expected Behavior:** Should handle gracefully with appropriate error message.

## 📊 Performance Expectations

### Response Characteristics
- **Plugin Response Time:** < 100ms (file reading)
- **Output Size by Subject:**
  - English: ~11,300 characters
  - Math: ~10,800 characters
  - Physics: ~13,400 characters
  - Chemistry: ~10,400 characters
  - Biology: ~10,800 characters

### Content Quality Indicators
Each response should include:
- ✅ Grade-level appropriate content (6-12)
- ✅ Specific examples and explanations
- ✅ Step-by-step guidance where applicable
- ✅ Real-world connections
- ✅ Study tips and strategies
- ✅ Common mistakes to avoid

## 🧪 Windows Command Line Testing Procedure

### Step 1: Setup and Build
```cmd
REM Navigate to plugin directory
cd plugins\learn-assist

REM Run setup (creates virtual environment)
setup.bat

REM Build the plugin executable
build.bat

REM Navigate to built plugin
cd dist\learn-assist

REM Verify files are present
dir
REM Should show: learn-assist-plugin.exe, manifest.json, *.md files
```

### Step 2: Basic Functionality Test
Test one question from each subject:

```cmd
REM Test English
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"What are past participles?"}}]} | learn-assist-plugin.exe

REM Test Math  
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"math","question":"How do I solve quadratic equations?"}}]} | learn-assist-plugin.exe

REM Test Physics
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"physics","question":"What is Newton's second law?"}}]} | learn-assist-plugin.exe

REM Test Chemistry
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"chemistry","question":"How do I balance chemical equations?"}}]} | learn-assist-plugin.exe

REM Test Biology
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"biology","question":"What is photosynthesis?"}}]} | learn-assist-plugin.exe
```

**Verification for each test:**
- Output starts with `{"success":true`
- Response contains educational content (10,000+ characters)
- Student question is embedded in the message
- Content includes subject-specific information

### Step 3: Error Testing
```cmd
REM Test invalid subject
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"history","question":"What caused WWI?"}}]} | learn-assist-plugin.exe

REM Test missing question parameter
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english"}}]} | learn-assist-plugin.exe

REM Test missing subject parameter  
echo {"tool_calls":[{"func":"get_learning_context","params":{"question":"Help me"}}]} | learn-assist-plugin.exe

REM Test empty parameters
echo {"tool_calls":[{"func":"get_learning_context","params":{}}]} | learn-assist-plugin.exe
```

**Expected Error Responses:**
- Invalid subject: `{"success":false,"message":"Educational content for subject 'history' not found..."}`
- Missing parameters: `{"success":false,"message":"Both 'subject' and 'question' parameters are required."}`

### Step 4: Output Validation
```cmd
REM Save output to file for analysis
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"Test question"}}]} | learn-assist-plugin.exe > test_output.txt

REM Check file size (should be 11,000+ characters)
dir test_output.txt

REM View content (use more or type)
more test_output.txt
```

### Step 5: Batch Testing Script
Create `test_all.bat`:
```cmd
@echo off
echo Testing Learn-Assist Plugin...
echo.

echo Testing English...
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"What are past participles?"}}]} | learn-assist-plugin.exe > test_english.json

echo Testing Math...
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"math","question":"How do I solve quadratic equations?"}}]} | learn-assist-plugin.exe > test_math.json

echo Testing Physics...
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"physics","question":"What is Newton's second law?"}}]} | learn-assist-plugin.exe > test_physics.json

echo Testing Chemistry...
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"chemistry","question":"How do I balance equations?"}}]} | learn-assist-plugin.exe > test_chemistry.json

echo Testing Biology...
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"biology","question":"What is photosynthesis?"}}]} | learn-assist-plugin.exe > test_biology.json

echo.
echo All tests completed. Check test_*.json files for results.
echo File sizes:
dir test_*.json
```

### Step 6: Performance Testing
```cmd
REM Time the plugin response
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"Test"}}]} | learn-assist-plugin.exe

REM Plugin should respond in under 1 second
REM Output should be immediate after command execution
```

## 🚀 Quick Test Commands Reference

### Essential Tests (Copy-Paste Ready)
```cmd
REM Build and navigate
cd plugins\learn-assist && setup.bat && build.bat && cd dist\learn-assist

REM Test all subjects quickly
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english","question":"What are past participles?"}}]} | learn-assist-plugin.exe
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"math","question":"How do quadratic equations work?"}}]} | learn-assist-plugin.exe  
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"physics","question":"What is Newton's second law?"}}]} | learn-assist-plugin.exe
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"chemistry","question":"How do I balance equations?"}}]} | learn-assist-plugin.exe
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"biology","question":"What is photosynthesis?"}}]} | learn-assist-plugin.exe

REM Test error cases
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"invalid","question":"test"}}]} | learn-assist-plugin.exe
echo {"tool_calls":[{"func":"get_learning_context","params":{"subject":"english"}}]} | learn-assist-plugin.exe
```

### Expected Success Indicators
- **All valid subjects**: Start with `{"success":true`
- **Output size**: 10,000-13,500 characters per response
- **Content verification**: Search for subject-specific keywords:
  - English: "Past Participles", "Essay Writing", "Literary Elements"
  - Math: "Quadratic Formula", "Algebra", "Geometry"  
  - Physics: "Newton's Laws", "Kinematics", "Energy"
  - Chemistry: "Atomic Structure", "Chemical Reactions", "Periodic Table"
  - Biology: "Cell Biology", "Genetics", "Photosynthesis"

### Expected Error Responses
- **Invalid subject**: `{"success":false,"message":"Educational content for subject 'invalid' not found..."`
- **Missing question**: `{"success":false,"message":"Both 'subject' and 'question' parameters are required."}`

## 📋 Expected AI Response Quality

### Good AI Response Indicators
- **References specific content** from the educational context
- **Uses appropriate terminology** for grade level
- **Provides step-by-step explanations** when applicable
- **Includes relevant examples** from the context
- **Follows pedagogical best practices**

### Example Quality Check
For the question "What are past participles?", the AI should:
- Define past participles clearly
- Distinguish regular vs. irregular forms
- Give specific examples from the context
- Explain usage in perfect tenses and passive voice
- Provide practice tips

## 🔍 Troubleshooting

### Common Issues
1. **File not found errors:** Check .md files are in plugin directory
2. **Empty responses:** Verify file encoding is UTF-8
3. **JSON parsing errors:** Check parameter formatting
4. **Large response handling:** Ensure G-Assist can handle ~13KB responses

### Debug Tips
1. Check plugin logs for detailed error messages
2. Verify file permissions on .md files
3. Test with simple questions first
4. Validate JSON formatting with online tools

## 📈 Success Metrics

### Plugin Performance
- **Success Rate:** >95% for valid inputs
- **Response Time:** <100ms average
- **Error Handling:** Graceful degradation for invalid inputs

### Educational Effectiveness
- **Content Coverage:** All major topics for each subject
- **Grade Appropriateness:** Suitable for grades 6-12
- **Practical Application:** Real-world examples and connections

## 🎯 Advanced Testing

### Load Testing
- Test multiple concurrent requests
- Verify plugin handles file access properly
- Check memory usage with large educational files

### Content Evolution Testing
- Test with updated .md files
- Verify plugin picks up content changes
- Check backward compatibility

### Cross-Subject Testing
- Test rapid switching between subjects
- Verify no content bleeding between subjects
- Check plugin state management

---

This testing guide ensures comprehensive validation of the learn-assist plugin's functionality, performance, and educational effectiveness across all supported subjects.