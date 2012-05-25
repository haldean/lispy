def main():
  from lispy.parser import parser
  from lispy.translate import translate
  import sys

  p = parser()
  if len(sys.argv) > 1:
    text = ' '.join(sys.argv[1:])
  else:
    text = sys.stdin.read()

  tree = translate(p.parse(text))
  if tree:
    print tree[-1]

if __name__ == '__main__':
  main()
