# Load in our dependencies
from __future__ import print_function
import os
import sublime
import sublime_plugin


# Define our constants
EMPTY_TM_SNIPPET = '\n'.join([
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
    '<plist version="1.0">',
    '<dict>',
    '</dict>',
    '</plist>',
])


# Define our plugin
def noop(*args, **kwargs):
    pass


class SnippetDestroyerDeleteAllCommand(sublime_plugin.ApplicationCommand):
    def get_snippets(self):
        """Collect all .sublime-snippet, .sublime-completions, and .tmSnippet files in Packages folder"""
        # Find relative paths to snippets (e.g. 'Packages/HTML/html.sublime-snippet')
        sublime_snippet_glob = '*.sublime-snippet'
        sublime_completions_glob = '*.sublime-completions'
        tm_snippet_glob = '*.tmSnippet'
        relative_snippets = (sublime.find_resources(sublime_snippet_glob) +
                             sublime.find_resources(sublime_completions_glob) +
                             sublime.find_resources(tm_snippet_glob))

        # Resolve full file path
        # /home/todd/.config/sublime-text-3/Packages + .. + Packages/HTML/html.sublime-snippet
        absolute_snippets = [
            os.path.join(sublime.packages_path(), os.path.join('..', relative_snippet))
            for relative_snippet in relative_snippets
        ]

        # Return our snippets
        return absolute_snippets

    def run(self):
        """Destroy every .sublime-snippet, .sublime-completions, and .tmSnippet file in Packages folder"""
        # Find all of our snippets
        snippets = self.get_snippets()

        # If there were no snippets found, let the user know
        active_window = sublime.active_window()
        if not snippets:
            active_window.show_quick_panel(['No snippets were found.'], noop)
        # Otherwise, prompt the user about actions to take (no as default)
        else:
            active_window.show_quick_panel(
                ['%d snippets were found. Do you want to:' % len(snippets),
                    'Keep them.', 'Destroy them.'],
                self.handle_decision)

    def handle_decision(self, index):
        """Decide to destroy or keep the snippet files"""
        # If we decided to destroy
        if index == 2:
            snippets = self.get_snippets()
            for relative_filepath in snippets:
                # Determine override content for the snippet
                # DEV: We need ot use XML for `.tmSnippet` to avoid XML and snippet complaints
                content = ''
                if relative_filepath.endswith('.tmSnippet'):
                    content = EMPTY_TM_SNIPPET

                # If there is no directory, then create it
                full_dirpath = os.path.dirname(full_filepath)
                if not os.path.isdir(full_dirpath):
                    os.mkdir(full_dirpath)

                # Output our new file (takes care of overrides for `Default` packages)
                #   e.g. `fun` -> `function` for JavaScript
                with open(full_filepath, 'w') as file:
                    file.write(content)
            sublime.active_window().show_quick_panel(
                ['%d snippets were destroyed.' % len(snippets)], noop)
