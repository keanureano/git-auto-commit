# (GAC) Git Auto Commit

Git Auto Commit is a Command Line Interface (CLI) application developed as part of our Computer Science thesis, designed to automate the generation of commit messages for software developers.

Leveraging large language models, the program extracts differential (diff) data from code changes, generates natural language commit messages, and automates the commit execution process. Data collection involves retrieving data from Facebook’s React repository via GitHub API, followed by a cleaning and filtering process to ensure data accuracy. Through testing, the application demonstrates its effectiveness and accuracy across various scenarios.

Key findings highlight the successful integration of large language model techniques, with a comparative analysis revealing the strengths and limitations of base, fine-tuned, and prompt-engineered models. The study concludes with recommendations for future research, emphasizing the exploration of lightweight large language models, newer evaluation techniques, and alternative deployment strategies to enhance codebase management systems.

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
- Copy the displayed path. It should look something like this:
  ```
  C:\...\...\gac.py
  ```
- Type the following command to open your PowerShell profile for editing:
  ```
  code $PROFILE
  ```
- Add the following function to the profile, replacing `FILE_PATH` with the copied path:

  ```
  function gac {
     python "FILE_PATH" $args
  }
  ```

- Save changes to the file.
- Restart VSCode.
- Now, you can run the application using the gac command in VSCode from any directory.

## Usage

Run the following commands to add a file and generate a comimt:

```
git add <file>
gac <-b, -e, -f, -c>
```

For additional options and information, you can run:

```
gac --help
or
python gac.py --help
```
