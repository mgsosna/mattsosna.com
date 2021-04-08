---
layout: post
title: Three ways to share your app
author: matt_sosna
---

I've been coding for eight years in R and Python, and it wasn't until *just months ago* that I was able to answer a question I've had this whole time: "How do I share my project with someone?"


Commonality in Docker & Heroku: needing to know Flask. Honestly, learning Flask was a gamechanger for me. 

## GitHub
Technical requirements of user: high
* They need to actually install all the stuff. If you're using a DB, they need to install Postgres or MySQL, then start it up, etc.
* If it's more than a little complicated, need lots of documentation

## Docker
Technical requirements of user: medium
* They don't necessarily need to install all the components. But they at least need to have Docker on their computer, and then they have to pull the image and run a container. Probably easier with the right instructions
  - I guess Docker Compose would help here...

## Heroku
Technical requirements of user: none
