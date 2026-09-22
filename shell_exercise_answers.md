# Shell & Bash Scripting Exercise — Answers

**Environment:** macOS · shell = zsh · Python 3.13.7
**Repo:** object-programming (public) · script delivered: `env_install.sh`

---

## Key concepts

- **Shell vs Terminal** — the *terminal* is the application/window (macOS
  Terminal). The *shell* is the program running inside it (zsh, bash, sh) that
  reads my typed commands and executes them. Terminal = the window; shell = the
  engine doing the work.
- **Environment variables** — named values the shell keeps in memory that
  programs can read, e.g. `$SHELL` (my login shell), `$PATH` (where commands are
  searched for), `$OSTYPE` (the operating system). I read one with `echo $NAME`.
- **Scripts** — a text file containing a list of shell commands, run all at once
  instead of typing them one by one (e.g. `env_install.sh`).
- **Package managers** — tools that install, update, and remove software
  automatically. macOS uses **Homebrew** (`brew`); Debian/Ubuntu use `apt`.

---

## Part 1 — Improve your shell experience

### 1.1 — Which shell am I using?
```bash
echo $SHELL      # login shell assigned to my account
ps -p $$         # the shell actually running right now
```
Result: **`/bin/zsh`** — the Z Shell, the default on modern macOS.
(Other possibilities: `/bin/bash` = Bourne Again Shell; `/bin/sh` = minimal
POSIX shell.)

### 1.2 — Install a shell framework
Because I'm on zsh, I installed **Oh My Zsh**:
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
I chose a theme by editing `~/.zshrc` (`ZSH_THEME="robbyrussell"`) and applied it
with `source ~/.zshrc`. The framework is verified as active because the prompt
changed to the themed style and shows the current git branch.

**What is the purpose of the `source` command?**
`source ~/.zshrc` re-runs the config file **in the current shell**, so changes
(theme, plugins, aliases) take effect immediately without closing and reopening
the terminal. A normal script runs in a separate child shell and its changes
disappear when it ends; `source` runs the lines in *this* shell instead, so the
changes actually stick.

### 1.3 — Enable the Git plugin
The config file for zsh is `~/.zshrc`. I opened it, found the plugins line, and
made sure `git` was listed:
```bash
plugins=(git)
```
Then reloaded with `source ~/.zshrc`.

**Verify aliases work** — inside my repo:
```bash
gst        # behaves exactly like: git status
```
Other aliases the plugin provides: `gl` (pull), `gp` (push), `ga` (add),
`gc` (commit), `glog` (compact log). Full list: `alias | grep git`.

---

## Part 2 — Check your Python installation
```bash
python --version     # zsh: command not found  (normal on macOS)
python3 --version    # Python 3.13.7
```
On macOS the modern Python is available as **`python3`**, not `python`.
**Installed version: Python 3.13.7.** Always use `python3` explicitly, because on
systems that have both, plain `python` may point to the old, unsupported
Python 2.

---

## Part 3 — Write your first automation script

The script `env_install.sh` sets up a Python dev environment and adapts to the
operating system. Structure: a shebang line, functions defined at the top, a
`main` function running them in order, and conditional branches based on the
detected OS.

**The six features:**
1. **Pretty printing** — a function using `printf` that wraps a message
   (`"$1"`) in blank lines for readable output.
2. **OS detection** — reads `$OSTYPE` (`darwin*` = macOS, `linux-gnu*` = Linux)
   and stores the result so the right package manager is used.
3. **Python check** — `command -v python3` tests if Python exists; if missing it
   installs it (brew on macOS, apt on Linux); if present it prints the version.
4. **pip verification** — displays `pip3 --version` to confirm pip works.
5. **Jupyter install** — branches by OS (brew on macOS, pip on Linux), because
   the install command differs per system.
6. **macOS health check** — runs `brew doctor` only when on macOS, to catch
   Homebrew problems early.

Created and made executable, then run:
```bash
touch env_install.sh
chmod +x env_install.sh     # without this the system refuses to run it directly
./env_install.sh
```
Delivered to GitHub:
```bash
git add env_install.sh
git commit -m "Add env_install automation script"
git push
```

---

## Part 4 — Execute and verify

**4.1 — Run the script:** `./env_install.sh` → ran through every feature and
ended with `==> Setup complete!` with no errors.

**4.2 — Verification checklist**

- [x] **Shell prompt reflects the framework** — Oh My Zsh themed prompt is
  active (`echo $ZSH` shows the `.oh-my-zsh` path).
- [x] **Git aliases respond** — `gst` returns the same output as `git status`.
- [x] **Python returns 3.x** — `python3 --version` → Python 3.13.7.
- [x] **pip shows a version** — `pip3 --version` returns the pip version tied to
  Python 3.13.
- [x] **Jupyter can be launched** — `jupyter --version` lists the components, and
  `jupyter notebook` opens it in the browser (stop with Ctrl+C).
- [x] **macOS: `brew doctor`** — reports no serious issues (warnings are fine;
  only "Error:" lines would be real problems).

---

*Note to self: confirm pip/jupyter lines actually returned versions on my
machine, and double-check the GitHub repo is set to Public for delivery.*
