from termcolor import cprint

def write_to_file(msg, err=False, warn=False, out=False):
  if err:
    color = 'red'
    filename = "stderr.log"
  elif warn:
    color = 'yellow'
    filename = 'stdwarn.log'
  elif out:
    color = 'magenta'
    filename = 'stdout.log'

  cprint(msg, color, attrs=['bold'])
  f = open('logs/' + filename, "a")
  f.write(msg + '\n')
  f.close()
