import sublime
import sublime_plugin


class HooksListener(sublime_plugin.ApplicationCommand):
    def run(self):
        print 'hai'
