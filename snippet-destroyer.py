# Load in our dependencies
from __future__ import print_function
import glob
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
SUBLIME_SNIPPET_EXT = '.sublime-snippet'
TM_SNIPPET_EXT = '.tmSnippet'


# Define our plugin helpers
def find_resources(resource_glob):
    # If we have Sublime's find_resources, then use it
    if hasattr(sublime, 'find_resources'):
        return sublime.find_resources(resource_glob)
    # Otherwise, we are on Sublime Text 2 which uses directories
    #   so let's search them via `resource_glob`
    else:
        packages_glob = os.path.join(sublime.packages_path(), '**', resource_glob)
        return glob.glob(packages_glob)


def is_destroyed_snippet(filepath):
    """
    Determine is a file is a destroyed snippet or not

    :param str filepath: Absolute path to our file
    :return: Indicator if the file is a destroyed snippet (true if it is, false otherwise)
    :rtype: bool
    """
    # If the override file doesn't exist, then it's not overridden
    if not os.path.exists(filepath):
        return False

    # If the file is empty, then it's definitely destroyed
    if os.path.getsize(filepath) == 0:
        return True

    # Otherwise, if it's a snippet and its content are our empty content, then it's destroy
    # DEV: In Sublime Text 2, `.sublime-snippet` must be non-empty where as ST3 only requires `.tmSnippet`
    if filepath.endswith(SUBLIME_SNIPPET_EXT) or filepath.endswith(TM_SNIPPET_EXT):
        with open(filepath, 'r') as file:
            if file.read() == EMPTY_TM_SNIPPET:
                return True

    # Otherwise, it's not a destroyed snippet
    return False


def noop(*args, **kwargs):
    pass


# Define our plugin
class SnippetDestroyerDeleteAllCommand(sublime_plugin.ApplicationCommand):
    def get_snippets(self):
        """Collect all .sublime-snippet, .sublime-completions, and .tmSnippet files in Packages folder"""
        # Find relative paths to snippets (e.g. 'Packages/HTML/html.sublime-snippet')
        sublime_snippet_glob = '*.sublime-snippet'
        sublime_completions_glob = '*.sublime-completions'
        tm_snippet_glob = '*.tmSnippet'
        relative_snippets = (find_resources(sublime_snippet_glob) +
                             find_resources(sublime_completions_glob) +
                             find_resources(tm_snippet_glob))

        # Resolve full file path
        # /home/todd/.config/sublime-text-3/Packages + .. + Packages/HTML/html.sublime-snippet
        absolute_snippets = [
            os.path.join(sublime.packages_path(), os.path.join('..', relative_snippet))
            for relative_snippet in relative_snippets
        ]

        # Filter out snippets that are destroyed
        absolute_snippets = [filepath for filepath in absolute_snippets if not is_destroyed_snippet(filepath)]

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
            for filepath in snippets:
                # Determine override content for the snippet
                # DEV: We need to use XML for snippets to avoid XML and snippet content complaints
                content = ''
                if filepath.endswith(SUBLIME_SNIPPET_EXT) or filepath.endswith(TM_SNIPPET_EXT):
                    content = EMPTY_TM_SNIPPET

                # If there is no directory, then create it
                dirpath = os.path.dirname(filepath)
                if not os.path.isdir(dirpath):
                    os.makedirs(dirpath)

                # Output our new file (takes care of overrides for `Default` packages)
                #   e.g. `fun` -> `function` for JavaScript
                with open(filepath, 'w') as file:
                    file.write(content)
            sublime.active_window().show_quick_panel(
                ['%d snippets were destroyed.' % len(snippets)], noop)
