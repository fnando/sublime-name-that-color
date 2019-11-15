import io, json, os, re

dir_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(dir_path, "colors.json")

with io.open(json_file_path, "r", encoding="utf8") as json_file:
  colors = json.load(json_file)

def is_color(color):
  color = strip(color)
  pattern = re.compile(r"^([0-9a-f]{3}|[0-9a-f]{6})$", re.IGNORECASE)
  return pattern.match(color) != None

def strip(color):
  return color.strip(" ").lstrip("#")

def hex2rgb(color):
  color = expand_color(color)
  return (int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16))

def expand_color(color):
  color = strip(color.upper())
  pattern = re.compile(r"^[0-9a-f]{3}$", re.IGNORECASE)

  if not pattern.match(color):
    return color

  return re.sub(r"^(.)(.)(.)$", r"\1\1\2\2\3\3", color)

def nearest_color(color):
  min_diff = None
  found_color = None
  color = expand_color(color)
  r1, g1, b1 = hex2rgb(color)

  for info in colors:
    r2, g2, b2 = hex2rgb(info[0])

    diff = abs(r1 - r2) * 256 + abs(g1 - g2) * 256 + abs(b1 - b2) * 256

    if min_diff is None or diff < min_diff:
      min_diff = diff
      found_color = info

  return {
    "hex": found_color[0],
    "exact_match": found_color[0] == color,
    "name": found_color[1]
  }

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

    def test_hex2rgb(self):
      self.assertEqual(hex2rgb("abc"), (170, 187, 204))
      self.assertEqual(hex2rgb("aabbcc"), (170, 187, 204))

    def test_nearest_color(self):
      self.assertEqual(nearest_color("#f00"), {"exact_match": True, "hex": "FF0000", "name": "Red"})
      self.assertEqual(nearest_color("#ff0000"), {"exact_match": True, "hex": "FF0000", "name": "Red"})
      self.assertEqual(nearest_color("#000012"), {"exact_match": False, "hex": "000011", "name": "Benthic Black"})

  unittest.main()
