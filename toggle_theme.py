import sublime, sublime_plugin

class ToggleThemeCommand(sublime_plugin.ApplicationCommand):
	def get_themes(self):
		settings = sublime.load_settings("Preferences.sublime-settings")
		return settings.get("themes", [])

	def get_current_theme(self):
		settings = sublime.load_settings("Preferences.sublime-settings")
		return dict(theme=settings.get("theme"), scheme=settings.get("color_scheme"), name="Current")

	def set_current_theme(self, theme):
		settings = sublime.load_settings("Preferences.sublime-settings")
		settings.set("theme", theme["theme"])
		settings.set("color_scheme", theme["scheme"])
		sublime.save_settings("Preferences.sublime-settings")

	def get_next_theme(self):
		themes = self.get_themes()
		current = self.get_current_theme()

		if len(themes) == 0:
			return None

		index = -1
		for i in range(len(themes)):
			if themes[i]["theme"] == current["theme"] and themes[i]["scheme"] == current["scheme"]:
				index = i
				break

		return themes[(index + 1) % len(themes)]
		

	def run(self):
		next_theme = self.get_next_theme()
		if next_theme is not None:
			self.set_current_theme(next_theme)

	def is_enabled(self):
		return self.get_next_theme() is not None

	def description(self):
		next_theme = self.get_next_theme()
		if next_theme is None:
			return "Toggle Theme"
		else:
			return "Switch to %s theme" % next_theme["name"]
