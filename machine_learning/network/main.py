from argparse import ArgumentParser
from os import listdir

DEFAULT_CHECKPOINTS_DIR = 'checkpoint/checkpoint_files'

arg_parser = ArgumentParser()
arg_parser.add_argument('-t', '--test', help="test or application mode", required=True, default="y")
arg_parser.add_argument('-l', '--ldir', help="list checkpoints", default="n")


while True:
    try:
        if arg_parser['test'] == "y":
            pass
        elif arg_parser['test'] == "n":
            if arg_parser['ldir'] == "y":
                
                checkpoints = listdir(DEFAULT_CHECKPOINTS_DIR)

                for count, item in enumerate(checkpoints):
                    print(f"[{count}] {item}")

                

            int_amount = int(input("int: "))
            
    except Exception as E:
        raise E
    