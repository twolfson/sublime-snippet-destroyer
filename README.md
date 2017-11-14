# sublime-snippet-destroyer

Destroy all [Sublime Text][] completions and snippets.

[Sublime Text]: http://sublimetext.com/

Have you ever been humming along, using `Tab` to fill out previously used variables, then *bam* you autocomplete to a snippet? Your flow is broken and frustrated at no easy way to remove the default snippets.

Well, suffer no more! `sublime-snippet-destroyer` seeks and destroys all completions and snippets.

> `sublime-snippet-destroyer` does not aim to allow for restoration of snippets. If we started doing that, then we should make a full-fledged snippet manager.

## Getting Started
### Installation
This package is available under `snippet-destroyer` inside of [Package Control][pkg-control], a [Sublime Text][subl] plugin that allows for easy management of other plugins.

[pkg-control]: http://wbond.net/sublime_packages/package_control

If you prefer the manual route, you can install the script via the following command in the Sublime Text terminal (``ctrl+` ``) which utilizes `git clone`.

```python
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/twolfson/sublime-snippet-destroyer', 'snippet-destroyer'], 'working_dir': path})
```

Packages can be uninstalled via "Package Control: Remove Package" via the command pallete, `ctrl+shift+p` on Windows/Linux, `command+shift+p` on Mac.

## Usage
`sublime-snippet-destroyer` provides a new command to the command pallete **"Destroy all snippets!!"**

When this is ran, it finds all `.sublime-snippet` + `.sublime-completions` + `.tmSnippet` files in your [Sublime Text][] Packages directory.

If no snippets are found, you will be informed as such.

If snippets are found, you will be prompted to confirm in their deletion. If you approve, they will be removed from disk.

There is currently one section we cannot erase which is any plugin with a `on_query_completions` method (e.g. `CSS` and `HTML`). These are baked in to `EventListener` commands and cannot be scrubbed easily. As a result, you must delete these files manually.

## Donating
Support this project and [others by twolfson][twolfson-projects] via [donations][twolfson-support-me].

<http://twolfson.com/support-me>

[twolfson-projects]: http://twolfson.com/projects
[twolfson-support-me]: http://twolfson.com/support-me

## Unlicense
As of Nov 20 2013, Todd Wolfson has released this repository and its contents to the public domain.

It has been released under the [UNLICENSE][].

[UNLICENSE]: UNLICENSE
