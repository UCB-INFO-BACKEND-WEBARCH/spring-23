# Github

## What  is Github?
GitHub is a web-based platform that uses Git as its back-end for version control. _It allows developers to collaborate on a project by storing and organizing files, tracking changes to files over time, and sharing code and feedback._

## Fundamentals/Features of Github

1. `Repositories`: A place to store and organize files, including code, documentation, and images.

2. `Version control`: The ability to track changes to files over time and revert to earlier versions if necessary.

3. `Branching`: The ability to create a separate copy of a repository to work on without affecting the main version of the code.

4. `Merging`: The process of bringing changes from one branch into another branch.

5. `Pull requests`: A way to propose changes to a repository and have them reviewed and approved by others before they are merged.

6. `Issues`: A way to track bugs, enhancements, or tasks that need to be done in a project.

7. `Collaboration`: The ability to work on a project with others and share code, feedback, and ideas.

8. `Forking`: A way to create a copy of a repository under your own account, so that you can make changes without affecting the original repository.

## Why should we use Github?

In the real-world, you rarely work on problems alone. No matter if you are in a workplace environment or building a personal project, there is a good chance that someone will be working on it with you.

Imagine you are working with a project partner and the two of you are supposed to build a small application for a banking system using Python.What do you think is the best possible way to work together?

- Sit down together each day and just work together on one machine?
- Send your Python files as zips to each other back and forth via email or slack etc?
- Call each other and tell the changes you made so that the other person can make the same changes in their code?

As you can imagine, none of the above methods are productive or convinient (read sensical). This is where Github/Git comes in.

Github allows you to create a repository, which you can think as the main replica of your work project in the cloud. You and your project partner can then make a copy of that repository (this is called cloning) and then make your own changes to the code, that too on your own machine - <b>WOW!</b>

## Working with Github

Everytime one of you makes a change, the code change is also reflected on the other user's code as you share the same common repository.

In case there are conflicts in what you and your partner wrote, for example, if due to confusion, you ended up making the same class file. In this scenario, Git is smart enough to know that you worked on the same thing and it raises something called a `Merge Conflict`.

The user that is pushing the same code/conflicted code later is then required to make changes to the code so that it is no longer in clonflict.

An overview of how Github works is as follow:

1. A developer creates a new repository on GitHub to store the code for their project.

2. They then clone the repository to their local machine, which creates a copy of the repository on their computer.

3. The developer makes changes to the files in the repository on their local machine, such as adding new code or fixing bugs.

4. They then commit the changes to their local repository, which saves a snapshot of the changes.

5. The developer then pushes the changes to the GitHub repository, which updates the online version of the repository with the latest changes.

6. Other developers can then see the changes and clone the repository to their own machines. They can also submit pull requests to suggest changes to the repository.

7. The original developer can review and approve the pull requests, and then merge the changes into the main branch of the repository.

8. Collaborators can also create their own branches of the repository, and make changes and submit pull requests, this way the original developer can review and merge the changes.

9. Github also allows to create issues, which are a way to track bugs, enhancements, or tasks that need to be done in a project.

## Getting Handson with Github

Let's say you I to start working on Assignment 1 for this course. Let's use the Github Classrooms [link](https://classroom.github.com/a/hzGwUYMy) that creates a repo for us.

Once you have your repo ready, you should see three options on how you can start working with it. ![](./assets/Repo%20Init.png)
- Create a new repo in your computer
- Push data from an existing folder from your computer to this repository
- Import code from another Git contract tool

You might notice a long URL in the first two options after the word `origin`. This is nothing but the URL where your repo lives at. THink of this as the URL you share for a Google Doc with people. The way they can use that URL to open a doc and make changes to it, they can use this Github origin URL in a very similar manner (by `pushing` and `pulling` changes from it).

Given that I am trying to start the assignment and that I have nothing set up yet, I will use the first option. In case I already had some of my code ready and I wanted to use that, I would have used the second option.

So I now create a new folder wherever I want on my computer, open up the terminal and navigate to the same path and then use the commands from the first option above.

```
echo "# assign1-sp2023-rishabhmthakur2" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/UCB-INFO-BACKEND-WEBARCH/assign1-sp2023-rishabhmthakur2.git
git push -u origin main
```

The first line and the origin URL will be different for each of you!

![](./assets/First%20Commit.png)

Once you do that, your repo page will now look something like this 

![](./assets/Changed%20Repo.png)

Okay, so let's break down what happened by talking about a few Git basics.

## Branches

In Git, _a branch is a pointer to a specific commit in the repository_. It allows developers to work on multiple versions of the codebase simultaneously without interfering with each other. Each branch has its own set of commits and can be updated independently of other branches.

When you create a new branch, it starts with the same code as the branch you created it from (often master). As you make commits, the branch pointer moves forward to the new commits, while the other branches stays where they are.

The default branch in Git is called master. It is considered the "main" branch and is often used for production-ready code. Developers can create new branches for new features or bug fixes, and when the code is tested and ready, it can be merged back into the master branch.

Branches are useful for:

- Working on multiple features at the same time
- Isolating changes
- Collaborating with other team members
- Testing different versions of the codebase

It is possible to merge multiple branches together using `git merge` command. Also, `git branch` command can be used to list all branches, create new branches or delete branches.

## Commits and Staging

In Git, a commit is a snapshot of the changes to a repository at a specific point in time. When you make changes to a file or set of files, you can use the `git commit` command to save those changes as a new commit in the repository's history.

A commit contains the following information:

- A unique identifier (SHA) that can be used to refer to the commit.
- The author and date of the commit.
- A message that describes the changes made in the commit.

```
git commit -m <message>
```

The staging area, also known as the `index,` is a temporary holding area for changes that are ready to be committed. When you make changes to a file, those changes are not automatically included in the next commit. Instead, you need to use the `git add` command to move the changes from your working directory into the staging area. Once the changes are in the staging area, you can use the `git commit` command to create a new commit with those changes.

The process of committing changes in Git typically involves three steps:

Make changes to files in your working directory
Use "git add" to move the changes to the staging area.
Use "git commit" to create a new commit with the changes in the staging area.
This process allows you to review the changes you've made and make sure that you only include the changes you want in each commit, rather than committing all the changes in your working directory at once.

## Git Pull/Fetch

`git pull` is a command that retrieves changes from a remote repository and merges them with the local repository.

`git fetch` is a command that retrieves changes from a remote repository, but it does not merge them with the local repository. Instead, it stores the changes in a separate branch called `origin/branch-name`, allowing the user to review the changes and merge them manually.

The `git merge` command, which merges the changes with the local repository.

In summary, git pull is a convenience command that combines git fetch and git merge, while git fetch only retrieves changes from a remote repository.

## Git Push

`git push` is a command that sends commits from the local repository to a remote repository. It is used to upload changes made on the local repository to a remote repository

```
git push <remote> <branch>
```

Where `remote` is the name of the remote repository you want to push to, and `branch` is the name of the branch you want to push. For example, to push changes to the master branch of a remote repository named origin, the command would be:

```
git push origin master
```

_It is important to note that before pushing to a remote repository, it is best practice to pull the latest changes from the remote repository to avoid conflicts._

## Merging and Conflics

A `merge conflict` in Git occurs when two branches have made changes to the same lines in a file, and Git is unable to automatically resolve those changes. This happens when you try to merge one branch into another and Git determines that the changes cannot be automatically merged.

When a merge conflict occurs, Git will mark the conflicting lines in the file with special symbols, such as <<<<<&#8203;sum = a + b&#8203;, and =======, to indicate which changes are conflicting.

```
<<<<<&#8203;sum = a + b&#8203;, and =======
```

To resolve a merge conflict, you need to manually edit the conflicting files and decide which changes to keep and which to discard. You can use a text editor or a merge tool to make these changes. Once you have resolved the conflicts, you will need to add the modified files and commit the changes to complete the merge.

Here are the general steps to resolve merge conflicts:

1. Identify the conflicting files: Git will show you which files have conflicts when you try to merge.

2. Open the conflicting files and look for the lines marked with <<<<<&#8203;oaicite:{"index":1,"invalid_reason":"Malformed citation <<, >>>>>>>"}&#8203;, and =======. These lines indicate the conflicting changes.

3. Decide which changes to keep and which to discard. You can use the <<<<<&#8203;oaicite:{"index":2,"invalid_reason":"Malformed citation <<and>>>>>>>"}&#8203; symbols to determine which changes came from which branch.

4. Once you have made your decisions, remove the conflict markers (<<<<<&#8203;oaicite:{"index":3,"invalid_reason":"Malformed citation <<, >>>>>>>"}&#8203;, and =======) and any unwanted changes.

5. Save the file and repeat the process for any other conflicting files.

6. Once you have resolved all the conflicts, you need to add the modified files and commit the changes.

7. Run git merge --continue to complete the merge process.

It is also possible to use Git merge tools, such as GitKraken, SourceTree, etc, that will make the process of resolving merge conflicts more intuitive and user-friendly.

So what happened earlier when we copied the commands from Github and pasted them in our computer?

```
echo "# assign1-sp2023-rishabhmthakur2" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/UCB-INFO-BACKEND-WEBARCH/assign1-sp2023-rishabhmthakur2.git
git push -u origin main
```

1. The first line creates a new file called `Readme.md` and pushes the string into it.
2. `git init`: This initializes your current folder to work with Github.
3. `git add`: This adds the Readme file that you just created to the list of files (taging area) that need to be added to your repo. This is currently local to your computer and you are trying to send it to the remote repo.
4. `git commit` - Commits these files and creates a snapshot of the repo that can now be reflected on the main repo.
4. `git branch -M main`: This sets the branch that you will be working with to `main`
5. `git remote add origin ...`: This sets up the origin URL for your repo. This is how it knows which repo it should sync with.
6. `git push`: Pushes the committed changes to the repo.
