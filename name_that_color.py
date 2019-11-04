import sublime, sublime_plugin
from . import utils

class NameThatColorCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in self.view.sel():
      view = self.view
      window = view.window()
      word_region = view.word(selection)
      word = view.substr(word_region)

      if not utils.is_color(word):
        continue

      window.status_message("Name That Color: fetching color name…")
      color = utils.expand_color(word)
      name = utils.color_name(color)

      if name is None:
        view.show_popup(
          "Name That Color: #%s doesn't have a name." % (color),
          location=-1,
          max_width=1000
        )

        continue

      def on_navigate(href):
        sublime.set_clipboard(href)
        window.status_message("Name That Color: name copied to clipboard.")
        view.hide_popup()

      template = """
        <br>
        &nbsp;&nbsp;<strong>#%s</strong> is called <strong>%s</strong>.&nbsp;&nbsp;
        <br>
        &nbsp;&nbsp;<a href='%s'>Copy name</a>
        <br>
        &nbsp;
      """

      view.show_popup(
        template % (color, name, name),
        location=-1,
        max_width=1000,
        on_navigate=on_navigate
      )
