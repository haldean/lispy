def main():
  import parser
  import sys
  import translate

  p = parser.parser()
  text = ' '.join(sys.argv[1:])
  tree = translate.translate(p.parse(text))

  if tree:
    print tree[-1]

if __name__ == '__main__':
  main()
