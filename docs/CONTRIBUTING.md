# How to contribute to the Data Platform?

Thank you for your interest in contributing to the platform! There are many ways to
contribute, and we appreciate all of them.

## Bug Reports

While bugs are unfortunate, they're a reality in software. We can't fix what we
don't know about, so please report liberally. If you're not sure if something is
a bug or not, feel free to file a bug anyway.

Opening an issue is as easy as following
[this link](https://github.com/astrolabe-expeditions/data-platform/issues/new) and filling out the
fields. Here are some things you can write about your bug:

- A short summary
- What did you try, step by step?
- What did you expect?
- What did happen instead?
- What is the version of the data platform?

## Pull Requests

### Workflow

Pull requests are the primary mechanism we use to change d. GitHub itself has
some [great documentation ](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models)
on using the Pull Request feature. We use the 'fork and pull' model described
there.

#### Step 1: Fork

Fork the project on GitHub and check out your copy locally:

```
$ git clone git@github.com:astrolabe-expeditions/data-platform.git
$ cd data-platform
$ git remote add fork git@github.com:username/data-platform.git
```

#### Step 2: Branch

Create a branch and start hacking:

```
$ git checkout -b my-branch -t origin/master
```

#### Step 3: Code

Well, I think you know how to do that. Just be sure to follow the coding
guidelines from the JS community.

We are using [eslint](https://eslint.org/) to lint code and [prettier](https://prettier.io/) to format it.

#### Step 4: Test

We don't have any tests at the moment. It's a long-term goal, so don't hesitate to add to it.

#### Step 5: Commit

Writing
[good commit messages](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
is important. A commit message should describe what changed and why. We also try to follow the naming
convention from [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

#### Step 6: Rebase

Use `git pull --rebase`, or `git rebase` (but not `git merge`), to sync your
work from time to time:

```
$ git pull origin master --rebase
```

#### Step 7: Push

```
$ git push fork my-branch
```

Go to https://github.com/astrolabe-expeditions/data-platform and select your branch. Click the
'Pull Request' button and fill out the form.

Pull requests are usually reviewed within a few days. If there are comments to
address, apply your changes in a separate commit and push that to your branch.

## Writing documentation

Documentation improvements are very welcome. We try to keep a good documentation
in the `docs/` folder. But, you know, we are developers, we can forget to
document important stuff that look obvious to us. And documentation can always
be improved.
