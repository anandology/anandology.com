---
layout: post
title: Designing RESTful APIs
---

# {{ page.title }}
<p class="meta">03 May 2018 &#8211; Visakhapatnam</p>

APIs are all around. Everyone talks about RESTful APIs, but what does "RESTful" really mean?

Let us try to understand that using a simple example. Let us build an Address Book API.

# Address Book API - the naive version

What are all the actions that you may want to do with an address book API?

- list all entries in the address book
- add a new entry
- update an entry
- delete an entry
- search for an entry

For simplicity, lets assume each contact in the address book has only name and phone number. 

The naive way to design the API is to come up with one url for every action that you want to have. So, you end up having the following endpoints.
	
	/list
	/add
	/update
	/delete
	/search

We also need to worry about the request and response formats for each of those end points. 

To delete or update an entry, we need to specify which entry to update. How do we identify an entry? Let us assume that each entry has a unique id.

So, the endpoint need to take the id, name and phone number as inputs.

	/update?id=4&name=foobar&phone=1234567890

And that responds back with:

	{"status": "updated"}

What if we give an invalid phone number? It should fail with an error, right?

	{"status": "failed", "error": "Invalid phone number"}	

This approach may look alright, but let us see how to design the same API in a RESTful way and compare both at the end.

# Address Book API - the RESTful version

To design a restful API, we don't start looking at actions, but at resources. Resources are just the topics/objects that you are dealing in the system.

Here we just have two types of resources, addressbook and contact. Since we are always working with the addresssbook and there is only one, we can ignore that for now.

So we only have one resource type, "contact". What REST suggests is to model the URLs around the resources. So you just have two URL endpoints. One endpoint for representing all contacts and another for each individual contact.

	/contacts
	/contacts/$id

You might be wondering how to handle all those actions listed earlier. The RESTful way to handle that is to use HTTP methods for actions. 

`GET /contacts` - list all the contacts<br>
`POST /contacts` - create a new contact<br>
`PUT /contacts/$id` - update a contact<br>
`DELETE /contacts/$id` - delete a contact

What about search? You don't really need a new one for search, just list the contacts but ask it to filter the results.

`GET /contacts?name=foo` - list all the **matching** contacts 

Not only that, these HTTP methods have very clear semantics. 

GET is always safe, which means GET request is not supposed have any side-effect.

 PUT and DELETE are idempotent, which means making multiple identical requests will have the same side-effect of making a single requets.

So, when desining RESTful APIs: 

* GET is used for reading any resource
* PUT is used to replace a resource (both create and update)
* DELETE is used to delete a resource
* POST is used to create a resource and often overloaded for other actions

Now let us look at error handling. HTTP alredy has status codes. RESTful APIs try to reuse the same instead of reinventing a new way to deal with errors.

`200 OK` - all is well<br>
`201 Created` - The resource you asked the server to create has been created<br>
`400 Bad Request` - the server could not understand the request from the client<br>
`404 Not Found` - The resource is not found<br>
`500 Internal Server Error` - something totally went wrong with the server, not your fault

What to support both JSON and XML data types. HTTP is there to help you again. RESTful APIs use the value of request header `Accept` to decide which format to use in the response. Pass `application/json` as value of `Accept` header to receive response as JSON and pass `text/xml` for xml.

In short, "RESTful" just means using HTTP effectively!

---

If you like this post, you may want to checkout my upcoming workshop on [Designing RESTful APIs][1].

[1]: https://rootconf.in/2018-designing-restful-apis/