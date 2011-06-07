(defun stdout (str)
  (with 'sys ((self 'write sys.stdout) str)))

(stdout "this is just a test\n")
