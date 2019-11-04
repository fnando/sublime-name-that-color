import io
import json
import os
import re
import struct
import urllib.parse
import urllib.request

dir_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(dir_path, "colors.json")

with io.open(json_file_path, "r", encoding="utf8") as json_file:
  colors = json.load(json_file)

def strip(color):
  return color.strip(" ").lstrip("#")

def is_color(color):
  color = strip(color)
  pattern = re.compile(r"^([0-9a-f]{3}|[0-9a-f]{6})$", re.IGNORECASE)
  return pattern.match(color) != None

def hex2rgb(color):
  return struct.unpack("BBB", expand_color(color).decode("hex"))

def color_name(color):
  if color in colors:
    return colors[color]

    url = "https://encycolorpedia.com/paints/schemes"
    data = bytes(json.dumps({"hex": color}), "utf8")

    headers = {
      "Content-type": "application/json",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
    }
    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)

    if response.status != 200:
      return None

    json_string = res.read()
    json_data = json.loads(json_string)

    [name, _] = re.split(r"\s+\/", data["match"]["name"])

    return name

def expand_color(color):
  color = strip(color.upper())
  pattern = re.compile(r"^[0-9a-f]{3}$", re.IGNORECASE)

  if not pattern.match(color):
    return color

  return re.sub(r"^(.)(.)(.)$", r"\1\1\2\2\3\3", color)

def retrieve_name(color):
  pass

if __name__ == "__main__":
  import unittest

  class Tests(unittest.TestCase):
    def test_is_color(self):
      self.assertTrue(is_color("f00"))
      self.assertTrue(is_color("#f00"))
      self.assertTrue(is_color("#F00"))
      self.assertTrue(is_color("#ff0033"))
      self.assertTrue(is_color("#FF0033"))
      self.assertTrue(is_color("ff0033"))

    def test_expand_color(self):
      self.assertEqual(expand_color("f00"), "FF0000")
      self.assertEqual(expand_color("#f00"), "FF0000")
      self.assertEqual(expand_color("F00"), "FF0000")
      self.assertEqual(expand_color("#F00"), "FF0000")

    def test_he2rgb(self):
      self.assertEqual(hex2rgb("fff"), (255, 255, 255))
      self.assertEqual(hex2rgb("ffffff"), (255, 255, 255))

  unittest.main()


