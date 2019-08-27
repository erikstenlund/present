import sys

def Serve():
    pass

def Compile():
    pass

def PrintHelp():
    pass

def Main():
    command = sys.argv[1]
    commands = {
        'compile' : Compile,
        'serve' : Serve
    }

    if command in commands:
        commands[command]()
    else:
        PrintHelp()
    

if __name__ == "__main__":
    Main()