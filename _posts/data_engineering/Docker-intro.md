---
layout: post
title: Docker for beginners
author: matt_sosna
---

Docker is a containerization service. It's like creating an isolated environment. Different from VM, though, because share resources.

Check out the post I wrote on ways of sharing projects.


Download Docker. Then do this:

{% include header-bash.html %}
```bash
docker pull ubuntu
```

This pulls the Ubuntu image. Ubuntu is a flavor of the operating system Linux. Linux is nice for a lot of programming stuff (especially servers) because it's lightweight (?) compared to Windows and MacOS, and it's open-source.

Now we can view our images.

{% include header-bash.html %}
```bash
docker images

# REPOSITORY    TAG     IMAGE ID        CREATED      SIZE
# ubuntu        latest  8e428cff54c8    2 days ago  72.9MB
```

Then try running:

{% include header-bash.html %}
```bash
docker run ubuntu
```

This starts a *container* of your image. The image is like a template, and the container is like an isolated instance of that image. However, you'll see that nothing happens. Well, we can go to our containers and see this:

{% include header-bash.html %}
```bash
docker ps
```
No running containers. How about all containers we've ever had?

{% include header-bash.html %}
```bash
docker ps -a
```

This shows a container of our Ubuntu image that closed. This is because a container is only alive so long as the processes *within it* are alive. All we did with our `docker run ubuntu` was create a container with the operating system, but we didn't specify any processes to run... so Docker opened the container, saw there was nothing running, and then immediately closed it.

Let's keep it alive by telling it to open `bash` (the Terminal), and that we should link our Terminal to the Terminal in the container with `-it`. `-i` means we can write messages to the container Terminal (i.e. our STDIN is linked), and `-t` means we can receive messages from the container (i.e. our STDOUT is linked).

{% include header-bash.html %}
```bash
docker run -it ubuntu bash
```

```bash
docker run -t ubuntu date
```
This prints out the date, then immediately closes the container.
