# Blockchain Sonar's Reminder

This is workspace branch of Blockchain Sonar's Reminder multi project repository based on [orphan](https://git-scm.com/docs/git-checkout#Documentation/git-checkout.txt---orphanltnew-branchgt) branches.

Branches (sub-projects):

* `docs` - Documentation
* `backend` - Sources of API service
* `frontend` - Sources of Web application

## Get Started

1. Clone the repository
	```shell
	git clone git@github.com:blockchain-sonar/reminder.git blockchain-sonar.reminder
	```
1. Enter into cloned directory
	```shell
	cd blockchain-sonar.reminder
	```
1. Initialize [worktree](https://git-scm.com/docs/git-worktree) by execute following commands
	```shell
	for BRANCH in backend docs frontend; do git worktree add "${BRANCH}" "${BRANCH}"; done
	```
1. Open VSCode Workspace
	```shell
	code "Blockchain Sonar Reminder.code-workspace"
	```
