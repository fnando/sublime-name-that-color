import sublime, sublime_plugin
import json
import io
from . import utils

with io.open("colors.json", "r", encoding="utf8") as json_file:
  colors = json.load(json_file)

class NameThatColorCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in self.view.sel():
      word_region = self.view.word(selection)
      word = self.view.substr(word_region)

      if not utils.is_color(word):
        continue

      color = utils.expand_color(word)

      if not color in colors:
        self.view.show_popup(
          "Name That Color: #%s doesn't have a name." % (color),
          location=-1,
          max_width=1000
        )

        continue

      name = colors[color]

      def on_navigate(href):
        sublime.set_clipboard(href)
        self.view.window().status_message("Name That Color: name copied to clipboard.")
        self.view.hide_popup()

      template = """
        <br>
        &nbsp;&nbsp;<strong>#%s</strong> is called <strong>%s</strong>.&nbsp;&nbsp;
        <br>
        &nbsp;&nbsp;<a href='%s'>Copy name</a>
        <br>
        &nbsp;
      """

      self.view.show_popup(
        template % (color, name, name),
        location=-1,
        max_width=1000,
        on_navigate=on_navigate
      )
