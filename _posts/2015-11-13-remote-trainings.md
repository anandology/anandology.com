---
layout: post
title: Improving the experience of remote trainings 
---

# {{ page.title }}
<p class="meta">13 November 2015 &#8211; Visakhapatnam</p>

I've been doing tech trainings (mostly Python) from quite some time, but it is only recently that I got a chance to explore remote trainings. 

In the traditional remote training setup, the instructor presents via WebEx/Skype/Hangout and the participants watch it. This experience is closer to watching a video than an in-person class-room training. 

I've been very keen to see if it is possible to bring the experience of remote trainings closer to the in-person class-room trainings. To understand what it takes to reach there, lets see the differences between them.

1. In class-room trainings, the participants keep watching what the instructor is doing in the big screen and use their laptop for writing their code. In remote trainings, there is only one laptop, which acts both as a screen and device for writing code.
 
2. In class-room trainings, the instructor uses his laptop for presenting and can go around the class and peep into the laptops of the participants to see what they are doing.

3. In class-room trainings, it is very easy for the instructor to have one-to-one conversation with participants and help them if they are stuck with something.

4. In class-room trainings, the participants can talk to each other and help among themselves.

The #1 very easy to solve. Ask the participants to keep 2 computers or one computer with 2 screens. One screen will show what the instructor is doing and the other one is free for writing code.

The #2 is also solvable. All we need is a way for the instructor to see the code the participants are writing. [JupyterHub][] is a wonderful tool to achieve this. It provides an [Jupyter][] (Ipython) notebook for every participant. The missing piece is to provide a way for the instructor to view that.

For one of my trainings, I wrote [a script][Makefile] to export the notebooks to HTML periodically (every couple of seconds) and opened the exported HTML of all participants in different browser tabs. That worked pretty well.

For this to work, the instructor should also have 2 computers, one for presenting and another for watching the code of the participants.

The #3 is a bit tricky. Usually the instructor shares his entire screen, so even chats with individual participants are visible to everyone. Since #2 requires the instructor to keep 2 computers, he can login to the training session from both the computers and dedicate one for presenting and use the other for watching what others are doing and also for communicating with them. 

It is would be even more awesome if there is a way to discuss directly from the jupyter notebook of the participants, or something like [github commit comments][1].

The #4 is would be nice, but I don't think it is really that important. Also, if instructor can discuss with the participants, the participants can also use the same platform for discussing among themselves, but it is not as simple as looking at the screen of the person sitting next to you. 

In one of my recent remote training, just fixing #2 made huge positive impact and the participants were a lot happier. I'm pretty confident that addressing the remaining issues will make the remote trainings a lot closer to in-person trainings.

With this experience, I'm even thinking of doing my [advanced python course][advpy] remotely. Drop me a note if you are interested.

If you have any experience with remote trainings or suggestions to improve mine, I would be very interested to know.

[JupyterHub]: https://github.com/jupyter/jupyterhub
[Jupyter]: http://jupyter.org/
[Makefile]: https://gist.github.com/anandology/6c27e81fcf12f7891aa9
[1]: https://github.com/blog/42-commit-comments
[advpy]: http://anandology.com/trainings/advanced-python.html