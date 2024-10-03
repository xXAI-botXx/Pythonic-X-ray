import code_analyzer as ca
import os

def main(FILE_NAME, PATH):
    for cur_root, cur_dirs, cur_files in os.walk(PATH):
        if FILE_NAME in cur_files:
            ca.analyse_code(os.path.join(cur_root, FILE_NAME), True, True)
            break
    
    
if __name__ == "__main__":
    # CHANGE THESE 2 VARS
    FILE_NAME = "heapsort.py"
    PATH = "./"
    main(FILE_NAME, PATH)

