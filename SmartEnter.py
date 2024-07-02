import sublime
import sublime_plugin


def is_space_or_tab(c):
	return c in '\t '


class SmartEnterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# run the enter command as normal to get default behaviour, then fix up the lines
		self.view.run_command('insert', {"characters":"\n"})

		for region in self.view.sel():
			current_line = self.view.line(region.begin())
			prev_line = self.view.line(current_line.begin()-1)

			current_contents = self.view.substr(current_line)
			prev_contents = self.view.substr(prev_line)

			ws_start = region.begin()-current_line.begin()
			del_count = 0

			while ws_start < len(current_contents) and is_space_or_tab(current_contents[ws_start]):
				ws_start += 1

			self.view.erase(edit, sublime.Region(region.begin(), ws_start+current_line.begin()))

			ws_end = 0
			while ws_end < len(prev_contents) and is_space_or_tab(prev_contents[len(prev_contents)-ws_end-1]):
				ws_end += 1

			self.view.erase(edit, sublime.Region(prev_line.end()-ws_end, prev_line.end()))

