import subprocess
import git_dict

def return_output(command):
	return subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=git_dict.data["project_full_path"]).stdout

def get_all_branches():
	raw_output = return_output("git branch -a")

def get_commit_diff():
	#https://stackoverflow.com/questions/20433867/git-ahead-behind-info-between-master-and-branch
	local_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..master"
	remote_output_command = "git rev-list --left-right --count " + git_dict.data['branches']['current'] + "..origin/master"

	local_raw_output = return_output(local_output_command)
	remote_raw_output = return_output(remote_output_command)

	print('local = ' + str(local_raw_output) + '\n\nremote = ' + str(remote_raw_output))

get_commit_diff()

def get_file_status():
	raw_output = return_output("git status")
