---
layout: post
title: How to write a new web framework
---

# {{ page.title }}
<p class="meta">28 March 2012 &#8211; Bangalore</p>

I want to write a small web app today.

Don't you think using a web framework is an overkill for a hello world app? I 
think a simple wsgi app will be good enough.

{% highlight python %}
def application(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']
{% endhighlight %}

I may want to handle 2 URLs, won't it be better if I have a class instead of a function.
    
{% highlight python %}
class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello world!\n"
{% endhighlight %}

Now let me add a way to delegate stuff based on URLs.

{% highlight python %}
    def __iter__(self):
        path = self.environ['PATH_INFO']
        if path == "/":
            return self.GET_index()
        elif path == "/hello":
            return self.GET_hello()
        else:
            return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Welcome!\n"

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello world!\n"
    
    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Not Found\n"
{% endhighlight %}
        
Neat, isn't it?

Why should I hardcode URLs? Won't it be better to abstract that out?

{% highlight python %}
    urls = [
        ("/", "index"),
        ("/hello", "hello")
    ]
    def __iter__(self):
        path_info = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for path, name in self.urls:
            if path == path_info:
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func()
        return self.notfound()
{% endhighlight %}
            
Looks good, but something is missing. How about adding ability to parameterize 
the URLs? All it takes is a regex match. Then I can do urls like `/hello/foo`!

{% highlight python %}
    urls = [
        ("/", "index"),
        ("/hello/(.*)", "hello")
    ]

    def __iter__(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()

    def GET_hello(self, name):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello %s!\n" % name
{% endhighlight %}

The `__iter__` method is really doing delegation. Don't you think we should move it into a separate method?

{% highlight python %}
    def __iter__(self):
        return self.delegate()
            
    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()
{% endhighlight %}

You know what? I think now there is lot of code that has nothing to do with my app at all. May be it is a good idea to move it into a base class.

{% highlight python %}
class wsgiapp:
    """Base class for my wsgi application."""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        
    def __iter__(self):
        return self.delegate()
            
    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()
        
class application(wsgiapp):
    urls = [
        ("/", "index"),
        ("/hello/(.*)", "index")
    ]

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Welcome!\n"
    
    def GET_hello(self, name):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello %s!\n" % name
{% endhighlight %}

Much better now. Don't you think?

Hey, wait a minute! Do you notice the duplication? The `self.start` method 
is called almost in the same way in both `GET_` methods. How about keeping the 
status and headers in the `wsgiapp` and provide a `header` function to add any 
new headers, if required?

{% highlight python %}
class wsgiapp:
    """Base class for my wsgi application."""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = "200 OK"
        self._headers = []
            
    def header(self, name, value):
        self._headers.append((name, value))
            
    def __iter__(self):
        x = self.delegate()
        self.start(self.status, self._headers)
            
        # return value can be a string or a list. we should be able to 
        # return an iter in both the cases.
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)
    
    ...

class application(wsgiapp):
    urls = [
        ("/", "index"),
        ("/hello/(.*)", "index")
    ]

    def GET_index(self):
        self.header("content-type": "text/plain")
        return "Welcome!\n"
    
    def GET_hello(self, name):
        self.header("content-type": "text/plain")
        return "Hello %s!\n" % name

{% endhighlight %}

Looking good. Isn't it?

I introduced an error by mistake and the server started giving a blank 
response. Believe me, it was too hard to spot the mistake. Let me add a check 
for it.

{% highlight python %}
    def __iter__(self):
        try:
            x = self.delegate()
            self.start(self.status, self._headers)
        except:
            headers = [("Content-Type": "text/plain")]
            self.start("500 Internal Error", headers)
            x = "Internal Error:\n\n" + traceback.format_exc()
            
        # return value can be a string or a list. we should be able to 
        # return an iter in both the cases.
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)
{% endhighlight %}                

Oh my god! It looks like I've invented a new web framework. 

Here is the complete code:

{% highlight python %}
import re
import traceback
    
class wsgiapp:
    """The most beatiful micro web framwork.
        
    How to use:
        
        class application(wsgiapp):
            urls = [
                ("/(.*)", "index"),
            ]
            def GET_hello(self, name):
                self.header("Content-Type", "text/plain")
                return "Hello, %s!" % name
    """
        
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = "200 OK"
        self._headers = []
            
    def header(self, name, value):
        self._headers.append((name, value))
            
    def __iter__(self):
        try:
            x = self.delegate()
            self.start(self.status, self._headers)
        except:
            headers = [("Content-Type", "text/plain")]
            self.start("500 Internal Error", headers)
            x = "Internal Error:\n\n" + traceback.format_exc()
            
        # return value can be a string or a list. we should be able to 
        # return an iter in both the cases.
        if isinstance(x, str):
            return iter([x])
        else:
            return iter(x)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups() 
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
                    
        return self.notfound()
{% endhighlight %}