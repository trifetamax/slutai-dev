#!/bin/bash

# Get the list of commits sorted by GIT_COMMITTER_DATE
sorted_commits=$(git log --all --pretty=format:"%H" | xargs -I {} git show -s --format="%ct %H" {} | sort -n | awk '{print $2}')

# Build the rebase sequence and save it to a temporary file
temp_file=$(mktemp)
for commit in $sorted_commits; do
    echo "pick $commit $(git log -1 --pretty=%B $commit | tr -d '\n')" >> "$temp_file"
done

# Perform the rebase and auto-create new commits with the same message on conflicts
GIT_SEQUENCE_EDITOR="cat $temp_file >" git rebase --root -i || {
    echo "Rebase failed. Auto-resolving conflicts..."
    while ! git rebase --continue; do
        # Automatically stage all changes
        git status | grep "both modified" | awk '{print $NF}' | xargs git checkout --theirs --quiet
        git status | grep "both deleted" | awk '{print $NF}' | xargs git rm --quiet
        git add .

        # Get the commit message of the current commit
        commit_message=$(git log -1 --pretty=%B)

        # Create a new commit with the same message
        git commit --no-edit --amend -m "$commit_message" --quiet
    done
}

# Clean up the temporary file
rm -f "$temp_file"

# Force push the changes to the remote
git push origin --force

