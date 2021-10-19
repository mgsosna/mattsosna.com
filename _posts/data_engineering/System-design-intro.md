---
layout: post
title: Fundamentals of system design
author: matt_sosna
---

Software is complex and involves many components. These components are generally best split apart into distinct components - this makes it easier to modify one piece without disrupting the rest, and it makes it easier to understand the entire ecosystem. There are some fundamentals of system design that you'll want to be aware of.

Start with a very basic system: a client, a server, and a database. The client sends a request to the server, which formats it into a SQL query that is run on the database. The server then sends the response back to the client.

From here, there's a lot more we can build. Let's get started!

## Overall architecture

### Monolith vs. microservices
Microservices is hot, but it's not always the best approach. Some advantages of monolith:
* Overall system complexity is lower. If you don't have _that_ much code, it can be better to keep things simple rather than getting some super complex distributed system design.

### Load balancing
When you duplicate your system, you'll need to route requests to the backups.

### Backups
Primary-secondary architecture (basically a "main" and a "backup"). Especially for database servers.

## Caching
### CDN: Content delivery networks

### Redis
* LRU Cache
* Basically, something sitting in front of the database to reduce load on it. But you need to think a little carefully about how to design this; if every request is a cache miss, then you're just doubling the number of requests being processed rather than actually reducing load on the system.


### Databases: SQL vs. NoSQL
NoSQL is gaining in popularity, but SQL can be fine, too. e.g. horizontal or vertical sharding to separate servers.
