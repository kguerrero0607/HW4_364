# SI 364 - F18 - HW4

### DEADLINE: November 27, 2018 at 11:59 pm

**You should read all of the below before beginning to ensure you set yourself up well and submit the assignment correctly.**

## Overview

You've been provided some scaffolding code. On top of the provided code, you'll need to add a number of things to make this application work fully, each marked by `TODO 364` inside the `app.py` file.

Each `TODO` listed for you is intended to be a small-to-medium size task. In general, you can go through the file top to bottom to address each one, but we've included suggestions in the comments about any time it makes sense to work on a TODO that comes later in the file first.

Your overall objective is to complete building an application that will allow you to search for gifs via [the Giphy api](https://developers.giphy.com/), store all searches performed on the app, and allow users to register accounts and log in to save their own personal collections of gifs.

![Ron Swanson from Parks and Recreation, dancing](https://media.giphy.com/media/iOz3p2txHIo4U/giphy.gif)

For example, a logged in user could save several different gif collections with different names -- *Excited Gifs*, *Happy birthday gifs*, whatever they want.

You will be:

* Associating data with a user's login using database relationships (and migrations)
* Building and using many-to-many relationships
* Practicing using SQLAlchemy for database queries and dealing with query results
* Building functions for the `get_or_create` operation that work with a database structure that includes many-to-many relationships
* Making back-end code work with existing templates

## Instructions

* First, check out the **to submit** instructions so you know how to begin work on this!
* Check out `app.py`, scan through it, read the comments, and complete the `TODO 364` todo items one by one.
* Identify anything in the `TODO` comments you are confused about so you can ask questions ASAP.
* Make sure to debug along the way!
* Then ensure you have everything committed properly and pushed to your new GitHub repo to submit the link properly to Canvas.

## To submit (read ALL the below before beginning)

**Don't fork this one.** Download the link as a .zip file. Unzip the file so you have all the provided, included files in a directory on your computer.

Follow the instructions inside `giphy_api_key.py`. *Then*, create a git repository inside that directory on your computer and commit all the files to your git repository.

Then, just as you did for the midterm assignment, create a GitHub repository for HW4 on your account called `HW4_364`.

Push *all* of the code files, including any additional files you add and all included files, to this GitHub repository.

Submit the link to your GitHub repository on the Canvas assignment for HW4. It should take the form of: `https://github.com/YOURGITHUBUSERNAME/HW4_364`
