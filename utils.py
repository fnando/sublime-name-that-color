import struct
import re

def strip(color):
  return color.strip(" ").lstrip("#")

def is_color(color):
  color = strip(color)
  pattern = re.compile(r"^([0-9a-f]{3}|[0-9a-f]{6})$", re.IGNORECASE)
  return pattern.match(color) != None

def hex2rgb(color):
  return struct.unpack("BBB", expand_color(color).decode("hex"))

def expand_color(color):
  color = strip(color.upper())
  pattern = re.compile(r"^[0-9a-f]{3}$", re.IGNORECASE)

  if not pattern.match(color):
    return color

  return re.sub(r"^(.)(.)(.)$", r"\1\1\2\2\3\3", color)

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


