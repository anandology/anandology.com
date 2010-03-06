---
layout: post
title: JavaScript templating with web.py
---

# {{ page.title }}
<p class="meta">05 Mar 2010 &#8211; Visakhapatnam</p>


I've been looking for a good JavaScript templating library for so long. I was using a variant of [JavaScript Micro-Templating][1] for my work and I wasn't happy with it. Most often, I ended up in duplication because of writing a Python template and a JavaScript template for doing the same thing. 

I started exploring to see if it is possible to extend [Templetor][2], the web.py templating engine, to solve this issue. To my surprise, it turned out to be very nice.

[1]: http://ejohn.org/blog/javascript-micro-templating/
[2]: http://webpy.org/docs/0.3/templetor

I added a new construct `jsdef` to Templetor. It defines a template function and also generates an equivalent JavaScript function.

For example:

{% highlight html %}
$jsdef hello(name)
    Hello, $name!
    
$hello("world")
{% endhighlight %}
    
will generate:

{% highlight html %}
<script type="text/javascript">
function hello(name){
    var self = [], loop;
    self.push("Hello, "); self.push(websafe(name)); self.push("!\n");
    self.push("\n");
    return self.join("");
}
</script>
Hello, world!
{% endhighlight %}

The `jsdef` block does two things here. It defines a template function that can be used while rendering the template and generates an equivalent JavaScript function that can be used at the client.

There are some caveats though. This is just an attempt to drive JavaScript templating from Python. But that won't magically happen because Python is not JavaScript.

It is important to remember that not all functionality in Python is supported. Features like multiple assignments, list slicing, list comprehensions won't work here. If you are using a python function inside the jsdef block, you need to provide the equivalent in JavaScript too. Some builtin functions of Python and other utilities used by the generated code are provided along with this extension.

Code is at <http://github.com/anandology/notebook/tree/master/2010/03/jsdef/>.
