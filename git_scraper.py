import subprocess
import re
import time

import git_dict

#testing
import json

def get_project_full_path():
	git_dict.data['project_full_path'] = str(subprocess.run('pwd', shell=True, stdout=subprocess.PIPE).stdout).replace("b\'","").replace("\\n\'","")

def return_output(command):
	return str(subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=git_dict.data["project_full_path"]).stdout)

def get_all_branches():
	raw_output = return_output("git branch -a")

	git_dict.data['branches']['current'] = re.search("\* ([a-zA-Z_0-9\-]*)", raw_output).group(1)
	git_dict.data['branches']['local'] = re.findall("\s(?! remotes) ([a-zA-Z_0-9\-]*)", raw_output)
	git_dict.data['branches']['remote'] = re.findall("remotes/*([^\\\\]*)", raw_output)

def get_commit_diff():
	local_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..master"
	remote_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..origin/master"

	local_raw_output = return_output(local_output_command)
	remote_raw_output = return_output(remote_output_command)
	
	git_dict.data['commit_diff']['local_master'] = re.findall("(\d)", local_raw_output)
	git_dict.data['commit_diff']['remote_master'] = re.findall("(\d)", remote_raw_output)

#This is really broken- git status changes depending on whether there are unstaged, untracked, or staged file, which break the regex I had set for when all three are present
def get_file_status():
	raw_output = return_output("git status -s")

	staged = re.findall(r"\SM\s*([a-z-_A-Z.]*)", raw_output)
	if staged is not None:
		git_dict.data['files']['staged'] = staged

	unstaged = re.findall(r"\sM\s*([a-z-_A-Z.]*)", raw_output)
	if unstaged is not None:
		git_dict.data['files']['unstaged'] = unstaged
	
	untracked = re.findall(r"\?\?\s*([a-z-_A-Z.]*)", raw_output)
	if untracked is not None:
		git_dict.data['files']['untracked'] = untracked

def run():
	get_project_full_path()
	while(True):
		get_all_branches()
		get_commit_diff()
		get_file_status()
		print(json.dumps(git_dict.data, indent=2))
		time.sleep(5)
