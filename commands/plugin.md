---
description: Manage Claude plugin marketplaces and install plugins from GitHub repos
---

You are executing a plugin management command. Parse the arguments and execute the correct action.

## marketplace add <repo>
Clone the marketplace repo and register it locally.
- Run: `git clone https://github.com/<repo>.git <HOME>\.claude\marketplaces\<repo-name>`
- If already exists, run `git -C <HOME>\.claude\marketplaces\<repo-name> pull` instead
- Print: "Marketplace <repo-name> registered at <HOME>\.claude\marketplaces\<repo-name>"

## marketplace update
Update all registered marketplaces.
- For each directory in <HOME>\.claude\marketplaces\, run `git -C <dir> pull`
- Print each update result

## install <plugin>@<marketplace>
Install a plugin from a registered marketplace into Claude's skills.
- Find the marketplace at <HOME>\.claude\marketplaces\<marketplace>
- Find the plugin at plugins\<plugin>\
- Copy skill.md to <HOME>\.claude\skills\<plugin>\skill.md (create dir if needed)
- If a setup script exists (setup.ps1 or setup.py), run it
- Copy any .py files from the plugin directory to <HOME>\.claude\skills\<plugin>\
- Print: "Plugin <plugin> installed from <marketplace>. Skill available as /<plugin>"

## list
List all registered marketplaces and installed plugins.
- List directories in <HOME>\.claude\marketplaces\
- List directories in <HOME>\.claude\skills\
