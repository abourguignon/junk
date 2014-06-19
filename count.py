import sys
from optparse import OptionParser

# Args
parser = OptionParser(description="Dummy command line stats tool")
parser.add_option("-f", "--file", type="string", dest="filename", help="the command line history file")
parser.add_option("-d", "--depth", type="int", dest="depth", default=2, help="depth of commands parsing")
parser.add_option("-l", "--length", type="int", dest="output_length", default=10, help="output length")

try:
    options, args = parser.parse_args()
except:
    exit(-1)

# Count
f = open(options.filename, 'r')

count = {}
max_size = 0
for e in f.readlines():
    # Only take the `depth` first words into account
    cmd = ' '.join(e.split(' ')[:options.depth]).rstrip()
    count[cmd] = count[cmd] + 1 if cmd in count else 1

sorted_truncated_count = sorted(count, key=count.get, reverse=True)[:options.output_length]

# Output
# Determine max size for output padding
max_cmd_length = len(max(sorted_truncated_count, key=len))
print "Your %s top used commands (depth %s)\n" % (options.output_length, options.depth)
for cmd in sorted_truncated_count:
    padding = (max_cmd_length - len(cmd)) * ' '
    print '%s %s %s' % (cmd, padding, count[cmd])
