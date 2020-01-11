import subprocess
import git_dict

def return_output(command):
	return subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=git_dict.data["project_full_path"]).stdout

def get_all_branches():
	raw_output = return_output("git branch -av")


#def get_commit_diff():
	# https://stackoverflow.com/questions/20433867/git-ahead-behind-info-between-master-and-branch ?? git rev-list <current_branch>..master  (and origin/master for remote) ??

#def get_file_status():
	raw_output = return_output("git status")
