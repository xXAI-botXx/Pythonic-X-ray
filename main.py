import code_analyzer as ca
import os

def main(FILE_NAME, PATH):
    for cur_root, cur_dirs, cur_files in os.walk(PATH):
        if FILE_NAME in cur_files:
            ca.analyse_code(os.path.join(cur_root, FILE_NAME), name="Mask R-CNN Instance Segmentation", should_print=True, should_save=True, save_path="./")
            break
    
    
if __name__ == "__main__":
    # CHANGE THESE 2 VARS
    FILE_NAME = "maskrcnn_toolkit.py"
    PATH = "../torch-mask-rcnn-instance-segmentation"
    main(FILE_NAME, PATH)

