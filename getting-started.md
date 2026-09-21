# Getting started

Everything below takes an afternoon. Do it before our first real meeting so we can spend that time on the physics instead of on `pip`.

## 1. Python

Install [Miniforge](https://github.com/conda-forge/miniforge) (or Anaconda, if your machine already has it). Then make one environment per project:

```bash
conda create -n thesis python=3.11
conda activate thesis
pip install numpy scipy matplotlib jupyterlab
```

Never install into the `base` environment. When something breaks six months from now, a throwaway environment is the difference between a five-minute fix and a lost week.

## 2. Git

Install [git](https://git-scm.com/downloads) and make a [GitHub account](https://github.com/signup). If you're a student, get the [Student Developer Pack](https://education.github.com/pack) — it's free and includes Copilot.

The three commands that cover 95% of what you need:

```bash
git add -A            # stage what changed
git commit -m "..."   # save a snapshot, with a message that says why
git push              # send it to GitHub
```

Commit whenever something works. A commit is a save point you can return to, and "it worked on Tuesday" is only useful if Tuesday still exists.

## 3. A repository for your work

I'll create a private repository for your thesis and add you to it. Your code, notes and data processing live there. That gives you a backup, a history of what you tried, and a way for me to look at your code without a chain of email attachments.

Large raw data does **not** go in git — I'll show you where it goes instead.

## 4. The libraries you'll probably need

Depending on the topic:

```bash
pip install InfraPy     # infrared image analysis
pip install pysfmov     # SFMOV thermal file reader
pip install pyLMS       # Siemens LMS TestLab .mat files
pip install pyNNST      # non-stationarity index
pip install pyidi       # image-based displacement identification
```

## 5. Writing

Use the [LaTeX templates](https://github.com/LolloCappo/Latex_template) from the start, not in the last month. [Overleaf](https://www.overleaf.com/) works if you'd rather not install a TeX distribution locally, and the templates drop straight into it.

Keep a `notes.md` in your repository from day one: what you tried, what the result was, what you decided. It costs two minutes a day and saves weeks at writing time.

---

Stuck on any of this? Open an [issue](../../issues/new) — setup problems are a perfectly good reason to use it.
