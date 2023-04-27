import argparse
from pathlib import Path
import subprocess

# Initiates the argument parser
parser = argparse.ArgumentParser(description="Concatenate mp3 files into a single one")
parser.add_argument("input_folder", help="Folder where the mp3 files are located.")
parser.add_argument('-o', '--output', type=str, help='Name of the output file', default=None)
args = parser.parse_args()

# Defines the folder location
input_folder = Path(args.input_folder)
output_folder = input_folder / "output"
output_folder.mkdir(parents=True, exist_ok=True)
if args.output:
    output_file = input_folder / f"output/{args.output}.mp3"
else:
    output_file = input_folder / "output/output.mp3"

# Lists all the mp3 files in the folder
mp3_files = [f for f in input_folder.iterdir() if f.suffix == ".mp3"]
file_list = input_folder / "file_list.txt"
with open(file_list, "w", encoding="utf-8") as f:
    for mp3_file in mp3_files:
        f.write(f"file '{mp3_file}'\n")

print("Starting concatenation...")
ffmpeg_command = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(file_list), '-c', 'copy', str(output_file)]
subprocess.run(ffmpeg_command)
