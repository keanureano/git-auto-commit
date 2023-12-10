# (GAC) Git Auto Commit

GAC is a command-line interface (CLI) application that explores and compares three transformer model-based techniques for automated commit message generation. The techniques include utilizing the Base model, Fine-tuning, and Prompt engineering, with the overarching goal of streamlining the commit message generation process and enhancing software development workflows.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/keanureano/git-auto-commit
   ```

2. **Navigate to the project directory:**

   ```bash
   cd git-auto-commit
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add the project directory to the system's PATH (Optional, VSCode Terminal only):**
   If you want to run the application using a simplified command (gac) from any directory, follow these steps in VSCode Terminal:

- Open VSCode terminal and type the following command to get the full path of `gac.py`:
  ```
  echo $PWD\gac.py
  ```
- Copy the displayed path.
- Type the following command to open your PowerShell profile for editing:
  ```
  code $PROFILE
  ```
- Add the following function to the profile, replacing `FILE_PATH` with the copied path:

```
function gac {
    py "FILE_PATH" $args
}
```

- Save changes to the file.
- Restart VSCode.
- Now, you can run the application using the gac command in VSCode from any directory.

```
git add <file>
gac
```