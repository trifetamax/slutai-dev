#!/bin/bash

# Get the list of commits sorted by GIT_COMMITTER_DATE
sorted_commits=$(git log --all --pretty=format:"%H" | xargs -I {} git show -s --format="%ct %H" {} | sort -n | awk '{print $2}')

# Build the rebase sequence and save it to a temporary file
temp_file=$(mktemp)
for commit in $sorted_commits; do
    echo "pick $commit $(git log -1 --pretty=%B $commit | tr -d '\n')" >> "$temp_file"
done

# Perform the rebase and resolve conflicts automatically
GIT_SEQUENCE_EDITOR="cat $temp_file >" git rebase --root -i || {
    echo "Rebase failed. Resolving conflicts..."
    while ! git rebase --continue; do
        # Keep the current version of conflicting files
        git status | grep "both modified" | awk '{print $NF}' | xargs git checkout --theirs --quiet
        git status | grep "both deleted" | awk '{print $NF}' | xargs git rm --quiet
        git add .
    done
}

# Clean up the temporary file
rm -f "$temp_file"

# Force push the changes to the remote
git push origin --force

