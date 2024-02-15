import sys, getopt

from server import Server

def main(argv):
  visualize = False

  try:
    opts, args = getopt.getopt(argv,"vh",["visualize", "help"])
  except getopt.GetoptError:
    print ('Optionerror')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-v", "--visualize"):
        visualize = True
    elif opt in ("-h", "--help"):
        print ('Visualize Data\nmain.py -v')
        sys.exit()

  # print("Visualize: ", visualize)
  server = Server(visualize=visualize)
  server.start()
if __name__ == "__main__":
   main(sys.argv[1:])

