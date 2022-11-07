import argparse
import glob
import json
import subprocess
import shutil
import os 
from pathlib import Path
from inspect import getsourcefile
from os.path import abspath
from sys import platform

def run_cli(exe, path, cwd):
	print(f"starting {path}")
	subprocess.run([exe, path], cwd=cwd)

def getArgs():
	parser = argparse.ArgumentParser(description='AWF workflow for TDA/DVM.')
	parser.add_argument("-i", "--inputDir", help="path to input directory")
	parser.add_argument("-p", "--dvi_path", help="path to dvi file")
	parser.add_argument("-o", "--outputDir", help="path to output directory")
	args = parser.parse_args()
	return args

def findFiles(inputDir):
	dvi_filePath = glob.glob(f"{inputDir}/*.dvi")[0]
	csv_filePath = glob.glob(f"{inputDir}/*.csv")[0]
	DvmWindowsPath = glob.glob(f"{inputDir}/DvmWindows.exe")[0]
	DvmLinuxPath = glob.glob(f"{inputDir}/DvmLinux.exe")[0]
	return dvi_filePath, csv_filePath, DvmWindowsPath, DvmLinuxPath

def writeFile(args, data):
	with open(f"{args.outputDir}/output.txt", "w") as f: 
		f.write(data) 

def copy_file_to_directory(file_path, directory_path):
	print('copy_file_to_directory', file_path, directory_path)
	if not os.path.exists(directory_path):
		Path(directory_path).mkdir(parents=True, exist_ok=True)
	shutil.copy(file_path, directory_path)
	# subprocess.run(['cp', file_path, directory_path])

def main():
	args = getArgs()
	
	working_directory = Path(args.inputDir)
	
	dvi_filePath, csv_filePath, DvmWindowsPath, DvmLinuxPath = findFiles(working_directory)
	# copy the files into path (this is redundant nescessary)
	# for example r'0deg\21Mps\'
	
	# check OS
	# return the path of dvm exe on the target project directory
	if platform == "win32":
		dvm_exe = DvmWindowsPath
	elif platform == "linux" or platform == "linux2":
	  	dvm_exe = DvmLinuxPath
	else:
		print('OS not surported')
		return

	temp_dvi_directory = os.path.join(working_directory, args.dvi_path)
	
	copy_file_to_directory(dvi_filePath, temp_dvi_directory)
	copy_file_to_directory(csv_filePath, temp_dvi_directory)
	
	
	# dvm_exe = 'OasysDVM_linux_LMXPrimer.exe'
	
	# curr_dir_path = os.path.dirname(abspath(getsourcefile(lambda:0)))
	
	# print('current files directory ', curr_dir_path)
	# current files directory  C:\Users\yun.sung\awf-1\awf_worker\runs\tda-dvm-awf-1.0.3

	# dvm_path = os.path.join(curr_dir_path, dvm_exe)
	
	# copy dvm into path
	# copy_file_to_directory(dvm_path, working_directory)
	# copy_file_to_directory C:\Users\yun.sung\awf-1\awf_worker\runs\tda-dvm-awf-1.0.3\requirements.txt C:\Users\yun.sung\awf-1\awf_worker\dumps/run_5860/input

	dvi_file_name = os.path.basename(dvi_filePath)
	dvi_file_partial_path = os.path.join(args.dvi_path, dvi_file_name)
	# -10deg\10Mps\C9_-10deg_10Mps.dvi
		
	print('dvm_exe', dvm_exe, 'dvi_file_partial_path', dvi_file_partial_path, 'working_directory', working_directory)
	
	# run dvm
	run_cli(dvm_exe, os.path.join(working_directory, dvi_file_partial_path), working_directory)
	
	# temp_dvm_path = os.path.join(working_directory, dvm_exe)
	
	# writeFile(args, data)
	

if __name__ == "__main__":
	main()	
