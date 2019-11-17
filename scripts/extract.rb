# frozen_string_literal: true

require "bundler/inline"

gemfile do
  gem "aitch"
  gem "nokogiri"
  gem "pry-meta"
end

require "aitch"
require "nokogiri"
require "csv"

def titleize(string)
  string
    .split(/\s+/)
    .flatten
    .map(&:capitalize)
    .join(" ")
    .gsub(/-(.)/) {|match| "-#{match[1].upcase}" }
end

def scrub(string)
  titleize(string.gsub(/(\(.*?\))/i, "")).strip
end

def get(url)
  id = Digest::MD5.hexdigest(url)
  cache_path = File.expand_path("#{__dir__}/../cache/#{id}.cache")

  return File.read(cache_path) if File.file?(cache_path)

  response = Aitch.get(url)
  content = response.body

  File.open(cache_path, "w") do |io|
    io << content
  end

  content
end

class HtmlCSSColor
  def self.call(colors)
    ("A".."Z").each_with_object(colors) do |letter, buffer|
      html_string = get("https://www.htmlcsscolor.com/color-names-rgb-values/#{letter}")
      html = Nokogiri::HTML(html_string)

      html.css("#cntMain_lstMain tbody > tr > td:nth-child(2) > a").each do |link|
        buffer[link["href"].split("/").last] = link.text
      end
    end
  end
end

class NameThatColor
  def self.call(colors)
    js_string = get("http://chir.ag/projects/ntc/ntc.js")

    js_string.scan(/\["(.*?)", "(.*?)"\]/m).each do |(color, name)|
      next if name.include?("Invalid Color")

      colors[color] = name
    end

    colors
  end
end

class Meodai
  def self.call(colors)
    csv_string = get("https://raw.githubusercontent.com/meodai/color-names/master/src/colornames.csv")

    CSV.parse(csv_string, headers: true) do |row|
      colors[row["hex"][1..-1].upcase] = row["name"]
    end

    colors
  end
end

class Jonathantneal
  def self.call(colors)
    json_string = get("https://raw.githubusercontent.com/jonathantneal/color-names/master/color-names.json")

    JSON.parse(json_string).each_with_object(colors) do |(hex, name), buffer|
      buffer[hex[1..-1].upcase] = name
    end
  end
end

class Margaret2
  def self.call(colors)
    json_string = get("https://raw.githubusercontent.com/Margaret2/pantone-colors/master/pantone-numbers.json")

    JSON.parse(json_string).each_with_object(colors) do |(_code, info)|
      next unless info["hex"] =~ /^[A-F0-9]{6}$/i

      colors[info["hex"].upcase] = info["name"].split("-").join(" ")
    end
  end
end

class Encycolorpedia
  def self.call(colors)
    html_string = get("https://encycolorpedia.com/named")
    html = Nokogiri::HTML(html_string)

    html.css("li > a[style]").each_with_object(colors) do |link, buffer|
      name, color = link.inner_html.split("<br>")
      buffer[color[1..-1].upcase] = name
    end
  end
end

class Sip
  COLORS_FILE = "/Applications/Sip.app/Contents/Resources/ColorList.json"

  def self.call(colors)
    config_file = File.expand_path(COLORS_FILE)

    return config_file unless File.file?(config_file)

    json_string = File.read(config_file)

    JSON.parse(json_string).each_with_object(colors) do |(color, name)|
      colors[color] = name
    end
  end
end

class Extract
  def self.call
    colors = [
      HtmlCSSColor,
      NameThatColor,
      Meodai,
      Jonathantneal,
      Margaret2,
      Encycolorpedia,
      Sip
    ].each_with_object({}) do |fetcher, buffer|
      fetcher.call(buffer)
    end

    colors = colors
             .sort_by {|color, _name| color }
             .map {|(color, name)| build_json(color, name) }

    File.open(File.expand_path("#{__dir__}/../colors.json"), "w") do |io|
      io << JSON.pretty_generate(colors)
    end
  end

  def self.build_json(color, name)
    [color, name]
  end

  def self.rgb_to_int(rgb)
    rgb[0] << 16 | rgb[1] << 8 | rgb[2]
  end

  def self.hex2rgb(color)
    [
      color[0..1],
      color[2..3],
      color[4..5]
    ].map {|component| component.to_s.to_i(16) }
  end
end

Extract.call
