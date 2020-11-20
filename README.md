# Name That Color for Sublime Text

This package shows the color name.

Sources:

- http://chir.ag/projects/name-that-color/
- https://encycolorpedia.com
- https://github.com/jonathantneal/color-names
- https://github.com/Margaret2/pantone-colors
- https://github.com/meodai/color-names
- https://sipapp.io
- https://www.htmlcsscolor.com/

## Installation

### Setup Package Control Repository

1. Follow the instructions from https://sublime.fnando.com.
2. Open the command pallete, run “Package Control: Install Package“, then search for “Name That Color“.

### Git Clone

Clone this repository into the Sublime Text “Packages” directory, which is located where ever the “Preferences” -> “Browse Packages” option in sublime takes you.

## Usage

The default binding is `super+k, super+n`.

![Name That Color in action](https://raw.github.com/fnando/sublime-name-that-color/main/images/found-color.png)

![Name That Color in action](https://raw.github.com/fnando/sublime-name-that-color/main/images/nearest-color.png)

![Name That Color: comparing colors](https://raw.github.com/fnando/sublime-name-that-color/main/images/compare-colors.png)

You can change it by defining a new shortcut binding like the following:

```json
{ "keys": ["ctrl+n"], "command": "name_that_color" }
```

## License

Copyright (c) 2019 Nando Vieira

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
