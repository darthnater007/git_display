import subprocess
import re

import git_dict

#testing
import json

def return_output(command):
	return subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=git_dict.data["project_full_path"]).stdout

def get_all_branches():
	raw_output = str(return_output("git branch -a"))

	git_dict.data['branches']['current'] = re.search("\* ([a-zA-Z_0-9\-]*)", raw_output).group(1)
	git_dict.data['branches']['local'] = re.findall("\s(?! remotes) ([a-zA-Z_0-9\-]*)", raw_output)
	git_dict.data['branches']['remote'] = re.findall("remotes/*([^\\\\]*)", raw_output)

def get_commit_diff():
	local_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..master"
	remote_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..origin/master"

	local_raw_output = str(return_output(local_output_command))
	remote_raw_output = str(return_output(remote_output_command))
	
	git_dict.data['commit_diff']['local_master'] = re.findall("(\d)", local_raw_output)
	git_dict.data['commit_diff']['remote_master'] = re.findall("(\d)", remote_raw_output)

def strip_status_extras(output):
	output = output.replace("\\n  (use \"git reset HEAD <file>...\" to unstage)\\n","")
	output = output.replace("\\n  (use \"git add <file>...\" to update what will be committed)\\n  (use \"git checkout -- <file>...\" to discard changes in working directory)\\n","")
	output = output.replace("\\n  (use \"git add <file>...\" to include in what will be committed)\\n","")
	
	return output

def parse_files(file_string):
	return re.findall("modified:\s*(\w*.\w*)", file_string)

def get_file_status():
	raw_output = strip_status_extras(str(return_output("git status")))

	git_dict.data['files']['staged'] = parse_files(re.search("committed:(.*)Changes", raw_output).group(1))
	git_dict.data['files']['unstaged'] = parse_files(re.search("commit:(.*)Untracked", raw_output).group(1))
	git_dict.data['files']['untracked'] =  re.findall(r"\\t(\w*.\w*)", re.search("Untracked files:(.*)", raw_output).group(1))