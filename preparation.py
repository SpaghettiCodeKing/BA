import os
import shutil
import random

def choose_50():

      to_pick_from = r"E:\uni\BA\data\input\topickfrom"
      to_write_to = r"E:\uni\BA\data\input\latin"

      all_files = [f for f in os.listdir(to_pick_from) if os.path.isfile(os.path.join(to_pick_from, f))]
      selected_files = random.sample(all_files, 50)

      for file_name in selected_files:
        source_file_path = os.path.join(to_pick_from, file_name)
        destination_file_path = os.path.join(to_write_to, file_name)
        shutil.move(source_file_path, destination_file_path)


def get_matching_pictures():
      to_pick_from = r"E:\uni\BA\data\input\topickfrom"
      txt = r"E:\uni\BA\data\input\latin"
      output = r"E:\uni\BA\data\input\img"
      
      txt_files = {os.path.splitext(f)[0] for f in os.listdir(txt) if os.path.isfile(os.path.join(txt, f)) and f.endswith('.txt')}
      
      for png_file in os.listdir(to_pick_from):
        if png_file.endswith('.jpg'):
            png_file_base = os.path.splitext(png_file)[0]
            if png_file_base in txt_files:
                # Copy the matching png file to the destination folder
                source_file_path = os.path.join(to_pick_from, png_file)
                destination_file_path = os.path.join(output, png_file)
                shutil.move(source_file_path, destination_file_path)