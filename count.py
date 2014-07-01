import sys
from optparse import OptionParser
from collections import Counter

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

commands = []
for e in f.readlines():
    # Only take the `depth` first words into account
    cmd = ' '.join(e.split(' ')[:options.depth]).rstrip()
    commands.append(cmd)

commands_count = Counter(commands).most_common(options.output_length)

# Output
# Determine max size for output padding
max_cmd_length = max([len(t[0]) for t in commands_count])
print "Your %s top used commands (depth %s)\n" % (options.output_length, options.depth)
for cmd, count in commands_count:
    padding = (max_cmd_length - len(cmd)) * ' '
    print '%s %s %s' % (cmd, padding, count)
