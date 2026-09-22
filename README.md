This is my first repository.


# Git & Bash Assignment — Answers

**Repo:** object-programming
**Author:** Amaury Martinotti

A short project to practice the full Git workflow: initializing a repository,
staging and committing, working with branches, merging, and pushing to GitHub.
Below are the commands used for each part and my answers to the questions.

---

## Part 1 — Setup & config
- Verify Git is installed: `git --version`
- Configure username: `git config --global user.name "amaury-mtti"`
- Configure email: `git config --global user.email "amaury.martinotti@gmail.com"`
q
## Part 2 — Create the repository
- Create a folder: `mkdir my-first-repo`
- Navigate into it: `cd my-first-repo`
- Initialize a repo: `git init`
- Create a file: `touch readme.txt`

## Part 3 — First commit
1. Show the current state of the repo: `git status`
2. Stage `readme.txt`: `git add readme.txt`
3. Commit with a message: `git commit -m "Add readme file"`
4. Show commit history: `git log`

## Part 4 — Make changes
1. Edit the file (add a line): `echo "This is my first repository." >> readme.txt`
2. **What does `git status` show now?**
   It lists `readme.txt` under "Changes not staged for commit" and marks it as
   **modified** — Git sees the file changed since the last commit, but the change
   hasn't been added to the staging area yet.
3. Stage and commit: `git add readme.txt` then
   `git commit -m "Add description line to readme"`
4. **How many commits now?** 2 commits.

## Part 5 — Exploration
- `git diff` — shows the line-by-line differences between your working files and
  the last commit (the changes you haven't staged yet).
- `git log --oneline` — shows the commit history in a compact form, one line per
  commit (short ID + message).

## Part 6 — Branches
1. List all branches: `git branch`
2. Create a branch: `git branch feature-script`
3. Switch to it: `git switch feature-script`
4. Create and switch in one command: `git switch -c dev`
5. Switch back: `git switch feature-script`
6. Verify current branch: `git branch` (the `*` marks the current one)

## Part 7 — Bash script on a branch
Contents of `install.sh`:
```bash
#!/bin/bash
echo "Starting installation..."
sudo apt-get update
sudo apt-get install -y tree
echo "Installation complete!"
```
- Make it executable: `chmod +x install.sh`
- Stage and commit: `git add install.sh` then `git commit -m "Add install script"`
- Check history on the branch: `git log --oneline`

## Part 8 — Merge
1. Switch back to main: `git switch main`
2. **Is `install.sh` present?** No — it was committed on the `feature-script`
   branch, and main doesn't have that commit yet, so the file doesn't exist here.
3. Merge the branch: `git merge feature-script`
4. **What changed?** `install.sh` now appears on main after the merge.
5. **Commit history observation:** main's history now includes the
   "Add install script" commit. Since main hadn't changed since the branch was
   created, it was a fast-forward merge, so the history stays in a straight line.
6. Delete the merged branch: `git branch -d feature-script`

## Part 9 — Push to GitHub
- Link local repo to GitHub: `git remote add origin git@github.com:amaury-mtti/my-first-repo.git`
- Push commits: `git push -u origin main`
- **After refreshing GitHub:** all my files and commits appear online.

## Part 10 — Delete and clone
1. Navigate out: `cd ..`
2. Delete the local folder: `rm -rf my-first-repo`
   (Windows PowerShell: `Remove-Item -Recurse -Force my-first-repo`)
3. Clone from GitHub: `git clone git@github.com:amaury-mtti/my-first-repo.git`
4. Verify: `cd my-first-repo` then `ls` — the files are back, downloaded with
   their full history.

## Part 11 — Full workflow from scratch
- Delete local folder: `rm -rf my-first-repo`
- Delete the repo on GitHub: Settings → Danger Zone → Delete this repository
- New project: `mkdir bash-installer` → `cd bash-installer` → `git init`
- Create and commit README: `git add README.md` then `git commit -m "Add README"`
- Feature branch: `git switch -c feature-install`
- Add the install script, then: `git add install.sh` and
  `git commit -m "Add install script"`
- Merge: `git switch main` then `git merge feature-install`
- Delete the branch: `git branch -d feature-install`
- Push: `git remote add origin <url>` then `git push -u origin main`

---

## Reflection questions

**1. Why is version control useful?**
Version control records the full history of a project. It lets me see exactly
what changed and when, undo mistakes by returning to an earlier version, work on
new features without breaking the working code, and collaborate with others
without overwriting each other's work. It also acts as a backup of the whole
project and its history.

**2. What is the difference between staging and committing?**
Staging (`git add`) chooses *which* changes will go into the next snapshot by
placing them in the staging area. Committing (`git commit`) permanently saves
that staged snapshot to the project history with a descriptive message. Staging
first means I can commit only some of my changes at a time instead of everything
at once.

**3. When should you make a commit?**
Whenever I've finished a small, complete, and logical piece of work — for
example a single feature, a bug fix, or one clear change. Frequent, focused
commits with clear messages are much better than one huge commit, because they
make the history easier to read and easier to undo if something goes wrong.

**4. What is the difference between `git init` and `git clone`?**
`git init` starts a brand-new, empty Git repository inside a folder on my own
machine. `git clone` copies an *existing* repository — with all of its files and
full history — from a remote source like GitHub onto my machine.

**5. Why should you write good commit messages?**
Good commit messages explain *what* changed and *why*. This makes the history
readable for me and my teammates, helps a lot when debugging (using `git log`
or `git blame`), and is essential for professional teamwork. A vague message
like "fix" tells no one anything a few months later.

**6. What is the purpose of using branches?**
Branches let me work on something — a new feature, an experiment, or a bug fix —
in isolation, without affecting the stable `main` code. I can develop and test
freely on the branch and only merge it into main once it's ready and working.

**7. When would you create a new branch instead of working on main?**
For any non-trivial work: a new feature, an experiment I might throw away, a bug
fix, or anything shared with teammates. Keeping that work on its own branch
means `main` always stays stable and functional, which is especially important
when several people work on the same project.
