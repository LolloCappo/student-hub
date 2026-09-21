# Getting started

Everything below takes an afternoon. Do it before our first real meeting so we can spend that time on the physics instead of on `pip`.

## 1. Python and VS Code

Install Python from **[python.org/downloads](https://www.python.org/downloads/)**. On Windows, tick **"Add python.exe to PATH"** in the first installer screen — it is off by default, and skipping it causes most of the problems you would otherwise hit later.

Then install **[Visual Studio Code](https://code.visualstudio.com/)** and its **[Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)**.

Check it worked:

```bash
python --version
pip --version
```

## 2. One environment per project

Never install packages into the system Python. Make a virtual environment inside each project folder instead:

```bash
python -m venv .venv
```

Activate it — Windows:

```bash
.venv\Scripts\activate
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Then install what you need:

```bash
pip install numpy scipy matplotlib jupyterlab
```

In VS Code, press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, and pick the one inside `.venv`. The bottom bar should then show your environment name.

When something breaks six months from now, a throwaway environment is the difference between a five-minute fix and a lost week. Record what you installed:

```bash
pip freeze > requirements.txt
```

## 3. Git

Install [git](https://git-scm.com/downloads) and make a [GitHub account](https://github.com/signup). If you're a student, get the [Student Developer Pack](https://education.github.com/pack) — it's free and includes Copilot.

The three commands that cover 95% of what you need:

```bash
git add -A            # stage what changed
git commit -m "..."   # save a snapshot, with a message that says why
git push              # send it to GitHub
```

Commit whenever something works. A commit is a save point you can return to, and "it worked on Tuesday" is only useful if Tuesday still exists.

Add a `.gitignore` with at least `.venv/` in it, so your environment never ends up in the repository.

## 4. A repository for your work

I'll create a private repository for your thesis and add you to it. Your code, notes and data processing live there. That gives you a backup, a history of what you tried, and a way for me to look at your code without a chain of email attachments.

Large raw data does **not** go in git — I'll show you where it goes instead.

## 5. The libraries you'll probably need

Depending on the topic:

```bash
pip install InfraPy     # infrared image analysis
pip install pysfmov     # SFMOV thermal file reader
pip install pyLMS       # Siemens LMS TestLab .mat files
pip install pyNNST      # non-stationarity index
pip install pyidi       # image-based displacement identification
```

## 6. Writing

Use the [LaTeX templates](templates/) from the start, not in the last month. [Overleaf](https://www.overleaf.com/) works if you'd rather not install a TeX distribution locally, and the templates drop straight into it.

Keep a `notes.md` in your repository from day one: what you tried, what the result was, what you decided. It costs two minutes a day and saves weeks at writing time.

---

Stuck on any of this? Open an [issue](../../issues/new) — setup problems are a perfectly good reason to use it.
