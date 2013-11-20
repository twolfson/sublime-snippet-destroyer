# sublime-snippet-destroyer

Destroy all [Sublime Text][] completions and snippets.

[Sublime Text]: http://sublimetext.com/

Have you ever been humming along, using `Tab` to fill out previously used variables, then *bam* you autocomplete to a snippet? Your flow is broken and frustrated at no easy way to remove the default snippets.

Well, suffer no more! `sublime-snippet-destroyer` seeks and destroys all completions and snippets.

> `sublime-snippet-destroyer` does not aim to allow for restoration of snippets. If we started doing that, then we should make a full-fledged snippet manager.

Currently, we are only supporting Sublime Text 2.

## Usage
`sublime-snippet-destroyer` provides a new command to the command pallete **"Destroy all snippets!!"**

When this is ran, it finds all `.sublime-snippet` + `.sublime-completions` + `.tmSnippet` files in your [Sublime Text][] Packages directory.

If no snippets are found, you will be informed as such.

If snippets are found, you will be prompted to confirm in their deletion. If you approve, they will be removed from disk.

There is currently one section we cannot erase which is any plugin with a `on_query_completions` method (e.g. `CSS` and `HTML`). These are baked in to `EventListener` commands and cannot be scrubbed easily. As a result, you must delete these files manually.

## Donating
Support this project and [others by twolfson][gittip] via [gittip][].

[gittip]: https://www.gittip.com/twolfson/

## Unlicense
As of Nov 20 2013, Todd Wolfson has released this repository and its contents to the public domain.

It has been released under the [UNLICENSE][].

[UNLICENSE]: ../UNLICENSE
