#!/bin/bash

# Generate the reversed commit order for rebase
reversed_commits=$(git log --reverse --pretty=format:"pick %h %s")

# Perform the rebase with reversed commits
GIT_SEQUENCE_EDITOR="sed -i '1,$!d;1i$(echo "$reversed_commits" | sed 's/[\/&]/\\&/g')" git rebase --root -i

# Force push the updated history
git push origin --force

