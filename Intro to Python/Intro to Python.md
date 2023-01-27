# Intro to Python

## Memory storage in computers

Before we start learning Python, we need to understand a few basics of how your systems (Laptops/Desktops/Handhelds) work, especially in terms of data processing and storage.
Under the hood, your devices have different kinds of storage. For simplicity, we can classify them into two parts: `Primary Storage`, `Secondary Storage`.

Each device has something call a `CPU` which is the shortform for `Central Processing Unit`. As the name clearly suggests, this is brain of a system, central to all processing. This is where your programs get executed and processed.

You must have also heard about `RAMs`, also called `Random Access Memory`. Then we have `Hard Disks` or `Memory Drives`.

The CPU, as you can imagine, talks to different data stores in order to push and pull data. Each push and pull takes time and energy. Your RAM chips are much closer and in sync with your CPU and hence these push and pull happen very quickly. So your CPU tries to interact with the RAM as much as it can. This is why RAMs are called primary storage devices.

However, if you check your device configurations now, your RAM will be somewhere around 8-32 GB on average, which your Memory Drives (HDDs/SSDs/mix) can be anywhere from 256 GB - 2 TB. Hence, whenever your RAM is full or if the CPU wants to store something large, it can not always be accomodated into the RAM. That is when it decides to interact with these external drives, or secondary storage devices.

Why do we need to know this? You will be desiging code and API that might require things like getting data from files in the storage, or multi-threading and parallel execution and it is important to know how the CPU works in order to write optimized programs.


## Let's talk about programming languages

Your CPU can only understand 0s and 1s. Everything else is gibberish! This is where things become interesting. In the early days, computer codes were actually written using 0s and 1s. They used to have punch cards and other mechanims that just provided their CPUs with voltages. Things have thankfully progressed from there!

Today, we can write code in almost plain english (Hello Python!) and the CPU is still able to understand that code and execute it and even return information to us that is not in 0s and 1s either!

We can classify the programming languages in three categories:
- Machine Language
- Assembly Language
- High-Level Language

This is because we have mechanism that convert the code you write into 0s and 1s - `Interpreter` and `Compiler`.

Both of them help convert a High-Level Language to a Machine Readable Code. Compilers convert the entire file into Machine code at once while Interpreters go line by line.

## Finally, time to talk about Python

Python is a `loosely-typed`, `high-level`, `interpreted` language. Too many terms all together, let's break it down.

1. `Loosely Type`: We don't have to specify data types for each variable in Python. The Interpreter interprets what data type it should be and then uses that to move forward.
2. `High-Level`: Like I said, Python is the closest you can get to write in English. 0s and 1s, where you at?
3. `Interpreted`: Python is interpreted line-by-line and is not compiled like C++ etc.

### Variables and Operators
### Conditionals
### Loops and Iterators
### Functions
### Classes and Objects in Python