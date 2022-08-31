# Fundamentals for working with git

Here are some of the most basic git commands for working with git. For some
more advanced commands (git diff, git merge, git mergetool, ...), please
consult the [official website](https://git-scm.com). 


## Download git repository

The url can be found on the web version of the Gitlab / Gitub repository. A
tipycal form for Gitlab is: https://gitlab.unamur.be/<username>/<repo>.git
```bash
git clone "https://gitlab.unamur.be/sijacque/andante.git"
```

## Download a newer version from the cloud

```bash
git pull
```

## Add changes to files

0. See status of modifications
```bash
git status
```

1. Modify files

2. Add modified files / new files to git modifications
```bash
git add file1 file2 file3
```

3. Assemble all modifications into a commit
```bash
git commit -m "Update message"
```

4. Send all commits to the remote repository
```bash
git push
```
    
## Change branch

To change to another branch (for example, the branch probabilistic):
```bash
git checkout <branch_name>
```

Change to a new branch:
```bash
git checkout -b <branch_name>
```

## Restore file to its previous state
```bash
git restore <file_name>
```
