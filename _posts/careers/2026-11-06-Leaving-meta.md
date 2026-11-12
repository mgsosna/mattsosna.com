---
layout: post
title: Lessons in technical leadership from five years in Big Tech
author: matt_sosna
tags: careers
---

This week, I left Meta after five incredible years. I entered in 2021 as an IC4 struggling with imposter syndrome, wondering if I was even cut out for Big Tech software engineering. I ended my time as a tech lead directing the engineering roadmap for a high-stakes area where mistakes carried real-world consequences.

Both Meta and the entire field of software engineering have changed dramatically in the last five years. As AI capabilities continue to accelerate, the value of pure code execution has collapsed. Engineering in the AI era is increasingly about thinking critically, forming a coherent vision, and communicating it clearly.

In the last year, I've been struck by how similar the shift from AI is to the mentality shift needed to grow from IC5 to IC6: moving from projects you can execute _just yourself_ to those requiring _coordinating multiple people_, often in areas outside your core expertise. This blog post covers some key lessons I learned on leading without a formal title and guiding a team when I didn't have all the answers.

## Responsibilities

| **Level** | **Responsibility** | **Can you...** | **Example** |
| --- | --- | --- | --- |
| IC3 | Execution with very low ambiguity | ...perform the technical implementation of well-scoped work? | Follow instructions to implement a set of signals |
| IC4 | Some ambiguity, more difficult execution | ...carry out a larger set of instructions when not each step is clearly laid out? | Given a problem, determine which signals to build and then build them. |
| IC5 | End-to-end execution with minimal oversight | ...identify a good way to solve a problem, then drive the solution to completion? | Identify a problem, convince others it's worth pursuing, then solve it. |
| IC6 | Determine (alongside PM, Operations, etc.) the problems an entire team should pursue and guidance on how to solve them | ...understand and navigate competing priorities, given limited resources? ...provide useful advice to any engineer on your team, even if you don't know all the details? | Prevent the team from being hamstrung by a new privacy requirement that necessitates an infra migration |
| IC7+| IC6 but for dozens or hundreds of engineers | ...forecast where the org needs to be in a year, given company priorities, and get the org there? | Leverage the best infra practices the tech industry is using lately |
{:.mbtablestyle}

The scope transition from IC5 -> IC6 is going from projects you can do _just yourself_ to those requiring _multiple people_. A rough rule of thumb from the book _Staff Engineer_ is that with every level increase, you're expected to deliver **3x the impact.** This is incredibly hard to do without coordinating others to row in the same direction. And it's hard to do _that_ without understanding what others' motivations are, how to structure a project so that everyone has clear ownership and accountability, etc.

## Advice
### You don't need to know everything to be helpful
When you're an IC4, your scope is small enough that you can gain deep-in-the-weeds understanding in a narrow area, and you can just focus on yourself. But as you grow, being a good teammate and eventually leader requires you to be able to provide feedback to others' work, even when that work is outside your core expertise.

It can feel intimidating trying to provide feedback on proposals or PRs when the author knows more about the details than you do. The key insight I had was that **you're not expected to know everything, but you should have high-level opinions applicable to any situation.** Some examples of opinions you should have:
* What are the key metrics the org cares about right now? Does this project contribute to those metrics or something else (e.g., Reliability)?
* When is it ok to incur tech debt to move quickly?
* When should you use/improve an existing system versus build something new?

Specific infra knowledge is helpful for determining how to implement a solution to a particular problem, but it's often more important to ensure that we're pursuing the right problem in the first place.

### Provide feedback with curiosity
Another insight I had was to **provide feedback with curiosity.** My first impression when I started providing feedback on PRs and proposals was that my feedback needed to be structured like, "This is wrong, do it this other way." But this requires a level of confidence that only comes from having a deep understanding of a topic, and others' work tends to be on topics I'm less familiar with. (If I understand something extremely well, chances are it's because it was a project the team worked on previously and finished, so we're now doing something else anyway.)

It's far easier to remove the assumption that I'm supposed to know everything and instead just ask questions.
* Even if I think I know a system or problem well, my understanding could be outdated and the author is using some new knowledge.
* If it turns out my confusion is warranted, it flags an issue in the proposal/PR in a non-confrontational way that the author is more likely to respond well to anyway.

### Assume good intent

### Overcommunicate credit and thanks
* Be generous with credit. The cost of someone getting more credit than they deserve is so much less than someone not getting the credit they deserve.

### Follow the data
* We can have a lot of good ideas, but do they actually work? Product mindset.
