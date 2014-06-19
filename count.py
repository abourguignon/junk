import sys

# Defaults
result_list_size = 20
depth = 2

# Handle args
if len(sys.argv) > 1:
    path = str(sys.argv[1])
else:
    raise Exception('No path given')

if len(sys.argv) > 2:
    try:
        result_list_size = int(sys.argv[2])
    except Exception as e:
        raise Exception('Second argument (result list size / default %s) must be an int (%s)' % (result_list_size, e))

if len(sys.argv) > 3:
    try:
        depth = int(sys.argv[3])
    except Exception as e:
        raise Exception('Third argument (depth / default %s) must be an int (%s)' % (depth, e))

# Count
f = open(path, 'r')

count = {}
max_size = 0
for e in f.readlines():
    # Only take the `depth` first words into account
    cmd = ' '.join(e.split(' ')[:depth]).rstrip()
    count[cmd] = count[cmd] + 1 if cmd in count else 1

sorted_truncated_count = sorted(count, key=count.get, reverse=True)[:result_list_size]

# Output
# Determine max size for output padding
max_cmd_length = len(max(sorted_truncated_count, key=len))
print "Your %s top used commands (depth %s)\n" % (result_list_size, depth)
for cmd in sorted_truncated_count:
    padding = (max_cmd_length - len(cmd)) * ' '
    print '%s %s %s' % (cmd, padding, count[cmd])
