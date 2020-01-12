import subprocess
import re

import git_dict

#testing
import json

def return_output(command):
	return subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=git_dict.data["project_full_path"]).stdout

def get_all_branches():
	raw_output = str(return_output("git branch -a"))
	print(raw_output)
	git_dict.data['branches']['current'] = re.search("\* ([a-zA-Z_0-9\-]*)", raw_output).group(1)
	git_dict.data['branches']['local'] = re.findall("\s(?! remotes) ([a-zA-Z_0-9\-]*)", raw_output)
	git_dict.data['branches']['remote'] = re.findall("remotes/*([^\\\\]*)", raw_output)


def get_commit_diff():
	#https://stackoverflow.com/questions/20433867/git-ahead-behind-info-between-master-and-branch
	local_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..master"
	remote_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..origin/master"

	local_raw_output = str(return_output(local_output_command))
	remote_raw_output = str(return_output(remote_output_command))

	print(local_raw_output)

def get_file_status():
	raw_output = return_output("git status")



#test
get_all_branches()
get_commit_diff()
print('\n' + json.dumps(git_dict.data, indent=4))