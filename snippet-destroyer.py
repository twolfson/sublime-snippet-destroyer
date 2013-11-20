import glob
import os
import sublime
import sublime_plugin


class SnippetDestroyerDeleteAllCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # Find all of our snippets
        package_dir = sublime.packages_path()
        tm_snippet_glob = os.path.join(package_dir, '**/*.tmSnippet')
        sublime_snippet_glob = os.path.join(package_dir, '**/*.sublime-snippet')
        snippets = glob.glob(sublime_snippet_glob) + glob.glob(tm_snippet_glob)

        # If there were no snippets found, let the user know

        # Otherwise, prompt the user about actions to take (no as default)
