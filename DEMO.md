# Storybook Demo Guide

This guide walks you through a complete demo of Storybook's features.

## Prerequisites

1. Install Storybook:
   ```bash
   cd storybook
   pip install -e .
   ```

2. Set your Anthropic API key:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

## Demo Walkthrough

### 1. Launch Storybook

```bash
storybook
```

You should see the ASCII banner and main menu.

### 2. Import the Sample Manuscript

1. Select **"3. Import Project"**
2. Enter file path: `examples/sample_chapter.md`
3. Project name: `demo_mystery`
4. Manuscript title: `The Lost Key`
5. Genre: Select **"Mystery"**
6. When asked to open the project, select **"Yes"**

You should now see the project menu with word count (~1,100 words).

### 3. Run an Automated Review

From the project menu:

1. Select **"2. Run Automated Review"**
2. When asked about focus areas, select **"Yes"**
3. Choose to focus on:
   - Characters (Yes)
   - Plot (Yes)
   - Prose (Yes)
4. Wait for the review (2-3 minutes)

The review will:
- Track characters (Sarah, Dr. Chen, the old man, mysterious figures)
- Analyze plot structure
- Evaluate prose quality
- Provide detailed feedback

### 4. View Tracked Characters

From the project menu:

1. Select **"3. View Characters"**

You should see a table showing:
- Sarah (protagonist)
- Dr. Elizabeth Chen
- The old man
- Other characters Claude identified

### 5. Interactive Chat Session

From the project menu:

1. Select **"1. Chat with Editor"**
2. Try these example prompts:

**Example 1: Character Development**
```
You: How can I make Sarah more memorable as a protagonist?
```

**Example 2: Plot Suggestion**
```
You: What should happen in Chapter 3? I want to increase tension.
```

**Example 3: Prose Improvement**
```
You: Improve the description of the key in the opening scene.
```

**Example 4: Specific Edit**
```
You: Add more sensory details to the scene where Sarah enters Dr. Chen's office.
```

**Example 5: Continuity Check**
```
You: Check if I've been consistent with the key's description throughout the manuscript.
```

3. Type `quit` when done

### 6. Export the Manuscript

From the project menu:

1. Select **"5. Export Manuscript"**
2. Enter export path: `my_novel.docx`
3. Check that the file was created

### 7. View Plot Events

From the project menu:

1. Select **"4. View Plot Events"**

You should see tracked events like:
- Sarah finds the key
- Meeting with the old man
- Confrontation at Dr. Chen's office

### 8. Project Settings

From the project menu:

1. Select **"6. Project Settings"**
2. Update any metadata (title, genre, author)

### 9. Create a New Project from Scratch

1. Select **"7. Back to Main Menu"**
2. Select **"1. New Project"**
3. Project name: `my_novel`
4. Title: `Your Novel Title`
5. Genre: Choose your genre
6. Select to open the project
7. Select **"1. Chat with Editor"**
8. Try: `I want to write a mystery novel about a detective who can see ghosts. Help me outline the first chapter.`

## Expected Results

After completing this demo, you should have:

1. ✅ Imported a sample manuscript
2. ✅ Generated a comprehensive literary review
3. ✅ Viewed automatically tracked characters and plot events
4. ✅ Had interactive conversations with the AI editor
5. ✅ Exported a manuscript to DOCX format
6. ✅ Created a new project from scratch
7. ✅ Experienced the full workflow

## Common Demo Scenarios

### Scenario 1: Grammar and Style Review

```
Chat: Review this paragraph for grammar and style:
"The key was laying on the ground. It's surface was covered with symbols that Sarah didn't understood."

Expected: Claude identifies:
- "laying" should be "lying"
- "It's" should be "Its"
- "didn't understood" should be "didn't understand"
```

### Scenario 2: Character Consistency

```
Chat: I mentioned the old man had a "walking stick" in Chapter 1 but later called it a "cane". Is this consistent?

Expected: Claude checks consistency and suggests:
- Pick one term and use it throughout
- Or explain why the terminology changed
```

### Scenario 3: Plot Development

```
Chat: I'm stuck on the cliffhanger at the end of Chapter 2. What are some ways I could resolve it in Chapter 3?

Expected: Claude provides multiple plot options while maintaining story consistency.
```

### Scenario 4: Prose Enhancement

```
Chat: This sentence feels flat: "Sarah was scared." Make it more vivid.

Expected: Claude suggests:
- "Sarah's heart hammered against her ribs."
- "Cold dread crept up Sarah's spine."
- "Sarah's breath caught in her throat."
```

## Tips for Demo Success

1. **Be Specific**: Ask focused questions for better results
2. **Iterate**: Build on previous responses
3. **Use Tools**: Ask Claude to track characters and events
4. **Save Work**: Export regularly to backup your progress
5. **Experiment**: Try different types of editing requests

## Performance Notes

- **First request**: May take 10-15 seconds (initializing)
- **Subsequent requests**: 5-10 seconds typically
- **Full reviews**: 2-5 minutes depending on manuscript length
- **Costs**: Approximately $0.10-0.30 for a full demo

## Troubleshooting Demo Issues

**Issue**: "No such file or directory: examples/sample_chapter.md"
**Solution**: Make sure you're in the `storybook` directory

**Issue**: Chat responses are very slow
**Solution**: Check your internet connection and API key

**Issue**: Import fails with "python-docx not found"
**Solution**: Install optional dependencies: `pip install python-docx pypdf`

**Issue**: Permission errors when editing
**Solution**: This is expected! Type 'y' to approve edits or 'n' to deny

## Next Steps After Demo

1. Try with your own manuscript
2. Explore different genres and styles
3. Experiment with custom editing requests
4. Set up automated workflows
5. Share feedback and suggestions

## Demo Script (Copy-Paste)

Here's a quick demo you can copy-paste:

```bash
# Set up
cd storybook
pip install -e .
export ANTHROPIC_API_KEY="your-key"

# Launch
storybook

# Then in Storybook:
# 1. Select "3" (Import Project)
# 2. Enter: examples/sample_chapter.md
# 3. Name: demo_mystery
# 4. Title: The Lost Key
# 5. Genre: Mystery
# 6. Open: Yes
# 7. Select "2" (Run Automated Review)
# 8. Focus areas: Yes to all
# 9. Wait for review...
# 10. Select "3" (View Characters)
# 11. Select "1" (Chat with Editor)
# 12. Type: "How can I improve the opening scene?"
# 13. Type: quit
# 14. Select "5" (Export)
# 15. Enter: demo_novel.md
# 16. Done!
```

Enjoy your demo! 🎉
