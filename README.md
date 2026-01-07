# For information, in case of problem : 

## Python version :
- 3.9.13

## Modules : 
- numpy
- matplotlib
- scipy
- pygame
- customtkinter

The pyproject.toml is set for python 3.9.13, but it is due to a dumb mistake I made at the begining of the project and 3.13.9 should work too.

I just cannot test it as my computer refuse to cooperate with different version of python

It sould work fine as it is, but it's a shame it's not in the latest version possible.








# Final project for CMB M2 students (2024/2025) <!-- omit in toc -->

This is the template repository for the 2024-2025 CMB Advanced Programming class.

- [1. Task](#1-task)
  - [1.1. What is expected](#11-what-is-expected)
  - [1.2. Suggestion on how to proceed](#12-suggestion-on-how-to-proceed)
- [2. Expected state of the result](#2-expected-state-of-the-result)
  - [2.1. You should be able "pip install" the code from scratch](#21-you-should-be-able-pip-install-the-code-from-scratch)
  - [2.2. You should be able to run the code from the terminal](#22-you-should-be-able-to-run-the-code-from-the-terminal)
  - [2.3. The code has to have docstrings](#23-the-code-has-to-have-docstrings)
  - [2.4. The code has to have type hinting](#24-the-code-has-to-have-type-hinting)
- [3. Small report](#3-small-report)
- [4. Installing and testing](#4-installing-and-testing)

## 1. Task

### 1.1. What is expected

Using the current template, you have to write the code for the different classes `Flyer`, `Bird`, `Predator`, `Flock`.

The classes `Bird` and `Predator` have to be implemented as inheriting from the class `Flyer`.

The class `Bird` should be implemented following the rules of the classic Boid version that we saw during the class.
Moreover, the instances of the class `Bird` should be trying to avoid instances of the class `Predator`.

The class `Predator` should be implemented as flyers that are attracted to `Bird`.

To begin with I would suggest putting ~100 birds and ~2 predators.

### 1.2. Suggestion on how to proceed

In order to make the project a little bit less daunting I would suggest to proceed the following way:

1) Implement the `Flyer` and `Bird` classes
2) Make sure that you can display **one** bird in the window with the command `run-boid`
   1) For that you will need to adapt the function `run_test` in `_runner.py` so that the triangles follow the bird direction
   2) You will also need to take into consideration the borders of the screen, you can for example invert the direction of a bird when it comes to a border
3) Implement the `Flock` class so that you can display multiple birds in window with the command `run-boid`
4) Implement the different `Bird` rules so that they behave as expected
5) Implement the `Predator` class and update the `Flock` class accordingly
6) Make sure that the command `run-boid` works properly
7) **Make sure that when you install your library from scratch in a new environment it does work!!**

## 2. Expected state of the result

### 2.1. You should be able "pip install" the code from scratch

Your final submitted product should be installable from a brand new environment just by running following command from the root of the folder of the project:

```shell
pip install .
```

### 2.2. You should be able to run the code from the terminal

Once installed, the code should be called the following way:

```shell
run-boid
```

Note that once installed the `run-boid` command is already defined by the template.
When running the `run-boid` command the function `run` from the `_runner.py` file is called, it is therefore the function that you will have to modify for your code to be properly running.

### 2.3. The code has to have docstrings

Moreover, each function of your code should have consistent docstrings with the abstract of the function, the more detailed description, the argument types and what they do and finally the return types and what they do.

### 2.4. The code has to have type hinting

Finally the code has to have type hinting.

## 3. Small report

You are also expected to write a small report that highlights two or three blocks of your choice.
In the line of code highlight I would like to see:

1) why you have choosen to highlight that specific block of code (for example: you found it difficult to implement, you are happy with the way you implemented it, you your solution is unique, ...)
2) a line by line explanation of the code
3) if there is things that you would have liked to do better

The report should also explain the limitations of your code and what would be the next step of your implementation and how you think you would proceed.

## 4. Installing and testing

First, you need create a new repository **with your name** that uses this template on the `CMB-advanced-programming` organisation as a **private repository**.

You can then clone your newly created repository locally and start working on it.

To test whether you have done things correctly you should be able to run the following command from the root folder of the project:

```shell
pip install .
```

Then run the following command from a terminal in the correct environment:

```shell
run-test
```

Then you should be able to see the window with the triangle moving randomly.
