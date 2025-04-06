# TagFlow

TagFlow is a simple and effective tool designed to automate the process of inserting tags on platforms like **SoundCloud** and other websites where a large amount of repetitive data entry is required. The program saves time by automating the insertion of tags, which is especially useful when uploading a large number of tracks or other content.

## 💡 Project History

The idea for TagFlow came to me when I was uploading audio to **SoundCloud**. I realized that each time I posted new audio, I had to manually enter the same tags over and over again. This was not only inconvenient but also time-consuming. I found myself repeating the same actions constantly, and that’s when I decided to automate the process.

That's how **TagFlow** was born — an easy-to-use tool for quickly inserting and managing tags, with customizable themes and keyboard shortcuts.

## 📋 Features

- **Automatic tag insertion**: The program automatically inserts tags from a predefined list stored in a text file. This eliminates the need to manually enter the same data.
- **Keyboard shortcuts**: Supports hotkeys for quick tag insertion (e.g., press F4 to insert the next tag).
- **Theme customization**: You can change the interface theme for a more personalized experience.
- **File management**: Tag data is stored in a text file that can be easily updated and configured.
- **User-friendly interface**: Simple to use, no technical knowledge required to get started.

## 🛠 Installation

### Requirements:

- Python 3.7 or higher
- Libraries: `keyboard`, `pyperclip`, `watchdog`, `tkinter`, `PIL`

### Instructions:

1. Clone the repository:
```bash
git clone https://github.com/1mcold/TagFlow.git
```
3. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Run the application:
  ```bash
  python main.py
  ```

## 🔧 Usage
- **Load tags**: You can load a list of tags from a text file (tags.txt), where each tag should be on a new line.
- **Automatic insertion:** Press F4 to insert the next tag.
- **Settings**: Press F6 to open the settings window where you can toggle the auto-typer and change the theme.
- **Reset**: Press F7 to reset the tag index and start inserting from the first tag again.
- **Exit**: Press F2 to exit the program.

## 🎨 Themes
The program supports theme customization. You can select a theme by choosing a JSON file with your preferred colors. You can create your own themes or use one of the predefined options.





## 🤝 Contributions
If you have any ideas for improving the program or if you find any bugs, feel free to create issues or submit pull requests!
