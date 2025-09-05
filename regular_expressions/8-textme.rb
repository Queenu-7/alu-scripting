#!/usr/bin/env ruby
log = ARGV[0]

matches = log.scan(/from:(.*?)\] \[to:(.*?)\] \[flags:(.*?)\]/)

# matches is an array of arrays; we just need the first match
if matches.any?
  sender, receiver, flags = matches[0]
  puts "#{sender},#{receiver},#{flags}"
end
