# Part 1 — Improve your shell experience

Notes and answers for the shell/bash exercise. Environment: macOS (default
shell is **zsh**), so the zsh path is used throughout. Bash equivalents are
noted where they differ.

## Key concepts
- **Shell vs Terminal** — the terminal is the app/window; the shell (bash, zsh,
  sh) is the program running inside it that reads and executes my commands.
- **Environment variables** — named values the shell holds in memory that
  programs can read, e.g. `$SHELL` (login shell) or `$PATH` (where commands are
  looked up). Read one with `echo $NAME`.
- **Scripts** — a text file of shell commands run all at once instead of typed
  one by one.
- **Package managers** — tools that install/update software (Homebrew `brew` on
  macOS, `apt` on Debian/Ubuntu).

## Step 1.1 — Which shell am I using?
Display the login shell assigned to my account:
```bash
echo $SHELL
```
Check the shell actually running right now (may differ from the login shell):
```bash
ps -p $$
```
Output on this machine: `/bin/zsh` — the Z Shell, default on modern macOS.
(Other common values: `/bin/bash` = Bourne Again Shell; `/bin/sh` = minimal
POSIX shell.)

## Step 1.2 — Install a shell framework
On zsh, install **Oh My Zsh** (the Oh My Bash equivalent for zsh):
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
*(Bash users would instead install Oh My Bash:*
`bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"`*)*

Choose a theme by editing the config file:
```bash
nano ~/.zshrc          # bash: ~/.bashrc
```
Set the theme line, then save (`Ctrl+O`, Enter) and exit (`Ctrl+X`):
```bash
ZSH_THEME="agnoster"   # Oh My Bash uses: OSH_THEME="font"
```
Apply the change and verify the framework is active:
```bash
source ~/.zshrc
```

### What's the purpose of the `source` command?
`source ~/.zshrc` re-runs the config file **in the current shell**, so changes
(theme, plugins, aliases) take effect immediately without closing and reopening
the terminal. A normal script runs in a separate sub-shell and its changes
disappear when it ends; `source` runs the file in *this* shell instead, so the
changes stay.

## Step 1.3 — Enable the Git plugin
1. Open the config file:
   ```bash
   nano ~/.zshrc        # bash: ~/.bashrc or ~/.bash_profile
   ```
2. Find the line starting with `plugins=(` and make sure `git` is listed:
   ```bash
   plugins=(git)
   ```
   (If other plugins are already there, add git with a space: `plugins=(git ...)`.)
3. Save (`Ctrl+O`, Enter) and exit (`Ctrl+X`).
4. Reload the configuration:
   ```bash
   source ~/.zshrc
   ```

### Verify the Git aliases work
The git plugin adds short aliases. Test the one for `git status`:
```bash
gst
```
It should behave exactly like `git status`. Other common aliases: `gp` (push),
`gl` (pull), `glog` (pretty log). List all git aliases the plugin added:
```bash
alias | grep git
```