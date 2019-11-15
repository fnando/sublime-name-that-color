import sublime, sublime_plugin, cgi, webbrowser
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
      found_color = utils.nearest_color(color)
      window.status_message("Name That Color: done.")

      def on_navigate(what):
        if what == "compare":
          webbrowser.open("https://codepen.io/fnando/full/zYYMvgj?colors=%s,%s" % (color, found_color["hex"]))
          return

        if what == "color":
          value = "#%s" % found_color["hex"]
        else:
          value = found_color[what]

        sublime.set_clipboard(value)
        window.status_message("Name That Color: {what} copied to clipboard.".format(what = what))
        view.hide_popup()

      if found_color["exact_match"]:
        template = """
          <br>
          &nbsp;&nbsp;<strong>#{hex}</strong> is called <strong>{escaped_name}</strong>.&nbsp;&nbsp;
          <br><br>
          &nbsp;&nbsp;<a href='name'>Copy name</a> | <a href='color'>Copy color</a>
          <br>
          &nbsp;
        """
      else:
        template = """
          <br>
          &nbsp;&nbsp;<strong>#{wanted_color}</strong> doesn't have a name.&nbsp;&nbsp;
          <br><br>
          &nbsp;&nbsp;The nearest color is <strong>{escaped_name}</strong> - #<strong>{hex}</strong>.&nbsp;&nbsp;
          <br><br>
          &nbsp;&nbsp;<a href='name'>Copy name</a> | <a href='color'>Copy color</a> | <a href='compare'>Compare</a>&nbsp;&nbsp;
          <br>
          &nbsp;
        """

      view.show_popup(
        template.format(wanted_color=color, hex=found_color["hex"], escaped_name=cgi.escape(found_color["name"])),
        location=-1,
        max_width=1000,
        on_navigate=on_navigate
      )
