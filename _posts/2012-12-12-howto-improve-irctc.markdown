---
layout: post
title: How to improve IRCTC
---

# {{ page.title }}
<p class="meta">12 December 2012 &#8211; Bangalore</p>

[www.irctc.co.in][] is the only available option for people
to book train tickets online in India. Even though there are other good
websites like [cleartrip.com](http://www.cleartrip.com/), they are not allowed
to book tickets until 12 noon. 

The www.irctc.co.in website is poorly engineered and can't handle the load it
recieves, esp. around 10:00AM when the tatkal tickets start. The sites stops
responsding in the middle of ticket booking and it dones't allow the user to
press browser back button and retry.

## The numbers

Lets try to see how many requests [www.irctc.co.in][] gets per second.

There are about 5000 trains in India. Assuming 20 coaches per train and 100 seats per
coach, it is 10 million people travelling per day. Assuming all of them are
booking tickets online, there are about 10M reservations/day or 115
reservations/second. These numbers are on the higher side and the actual
numbers will be far less than this.

Assuming 4 page views per reservation, it is about 500 requests/second.

## How to improve irctc.co.in

Here are my suggestions to improve the performance and stability of irctc
website without modifying too much of the existing setup.

### 1. Serve static resources using a different webserver

It takes very very long time to load even the static resources like images, css
and javascript. They are not main part of the app and can be moved out to a new
webserver. 

It'll also be helpful to make the homepage a static resource and let
it be served like other static resources.

I suggest using [Nginx][]. Nginx is light weight webserver and it is very
efficient in serving static files. 

### 2. Make searching for trains independent of ticket booking

Booking the ticket is very small part of the whole process. Most of the time is
spent in finding which train to take. This can be handled completely
independently. The information about trains and stations is small enough to
keep in memory completely.

Since this data is not very big, most of this can be packed into javascript and
station autocomplete and searching for trains can be completely implemented in
Javascript. That will reduce the load on the server substantially.

### 3. Cache the availability info in memory

Cache the seat availability info in memory.

The seat availability information changes so fast that it is fine to show
slightly stale info. By the time, the user fills in the passenger details, the
availabilty will change anyway.

To make sure the availability info is not too stale, run a background job to
update it frequenty or update it whenever a ticket is booked.

This will make sure that searching for trains and their availability will not
hit the reservation system.

## I can help!

There are many other improvements that can be done to make sure the website
works well under heavy load.

I've lot of experience in building and scaling high traffic websites and I'll
be very glad to offer my help to IRCTC to improve the website. 

[Nginx]: https://en.wikipedia.org/wiki/Nginx
[www.irctc.co.in]: https://www.irctc.co.in/


