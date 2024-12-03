# Leetcode Python

This is a repository for my Leetcode solutions in Python. I am using this as a way to automate the boilerplate creation for any leetcode problem.

This repository is inspired by [Leetcode-Rust](https://github.com/aylei/leetcode-rust/tree/master)

# Pre-requisites

Please use Poetry to install the dependencies. You can install Poetry using the following command:

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Then install the dependencies using the following command:

```shell
poetry install
```

# Setup

1. Initialize the template submission file for a problem with ID {id}

```shell
python main.py

# Output
# Welcome to leetcode-python system.
#
# Please enter a frontend problem id,
# or "random" to generate a random one,
# or "solve $i" to move problem to solution/,
#
# 123  # Enter the problem ID
```

You can also use `random` or `all` to generate random problems or initialize all problems respectively.

2. Run the tests

```shell
python test.py
```

To filter tests by problem ID, use the following command:

```shell
python test.py --id 123
```

3. Solve the problem

To solve the problem, you can use the following command:

```shell
poetry run start

# Output
# Welcome to leetcode-python system.
#
# Please enter a frontend problem id,
# or "random" to generate a random one,
# or "solve $i" to move problem to solution/,
#
# solve 123  # Enter the problem ID
```
