import glob
import os
import sublime
import sublime_plugin


def noop(*args, **kwargs):
    pass


class SnippetDestroyerDeleteAllCommand(sublime_plugin.ApplicationCommand):
    def get_snippets(self):
        """Collect all .sublime-snippet, .sublime-completions, and .tmSnippet files in Packages folder"""
        package_dir = sublime.packages_path()
        sublime_snippet_glob = os.path.join(package_dir, '**/*.sublime-snippet')
        sublime_completions_glob = os.path.join(package_dir, '**/*.sublime-completions')
        tm_snippet_glob = os.path.join(package_dir, '**/*.tmSnippet')
        snippets = (glob.glob(sublime_snippet_glob) +
                    glob.glob(sublime_completions_glob) +
                    glob.glob(tm_snippet_glob))
        return snippets

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
                # If the file is a tmSnippet, remove it (prevents XML complaints)
                if filepath.endswith('.tmSnippet'):
                    os.unlink(filepath)
                # Otherwise, replace it with a blank file (takes care of overrides for `Default` packages)
                #   e.g. `fun` -> `function` for JavaScript
                else:
                    with open(filepath, 'w'):
                        pass
            sublime.active_window().show_quick_panel(
                ['%d snippets were destroyed.' % len(snippets)], noop)
