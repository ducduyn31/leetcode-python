# Leetcode Python

This is a repository for my Leetcode solutions in Python. I am using this as a way to learn Python and improve my problem-solving skills. I will be adding solutions as I solve them.

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
poetry run start

# Output
# Welcome to leetcode-python system.
#
# Please enter a frontend problem id,
# or "random" to generate a random one,
# or "solve $i" to move problem to solution/,
# or "all" to initialize all problems
#
# 123  # Enter the problem ID
```

You can also use `random` or `all` to generate random problems or initialize all problems respectively.

2. Run the tests

```shell
poetry run test
```

To filter tests by problem ID, use the following command:

```shell
poetry run test -- -k test_{id}
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
# or "all" to initialize all problems
#
# solve 123  # Enter the problem ID
```
