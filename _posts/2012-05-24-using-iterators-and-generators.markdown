---
layout: post
title: Using iterators and generators in multi-threaded applications
tags: [python]
---

# {{ page.title }}
<p class="meta">24 May 2012 &#8211; Bangalore</p>

Python iterators and generators have almost the same behavior, but
there are subtle differences, especially when the iterator/generator
is used in a multi-threaded application.

Here is an example to demonstrate that behavior.

{% highlight python %}
import threading

def count():
    i = 0
    while True:
        i += 1
        yield i

class Counter:
    def __init__(self):
        self.i = 0

    def __iter__(self):
        return self

    def next(self):
        self.i += 1
        return self.i

def loop(func, n):
    """Runs the given function n times in a loop.
    """
    for i in range(n):
        func()

def run(f, repeats=1000, nthreads=10):
    """Starts multiple threads to execute the given function multiple
    times in each thread.
    """
    # create threads
    threads = [threading.Thread(target=loop, args=(f, repeats)) 
               for i in range(nthreads)]

    # start threads
    for t in threads:
        t.start()

    # wait for threads to finish
    for t in threads:
        t.join()

def main():
    c1 = count()
    c2 = Counter()

    # call c1.next 100K times in 2 different threads
    run(c1.next, repeats=100000, nthreads=2)
    print "c1", c1.next()

    # call c2.next 100K times in 2 different threads
    run(c2.next, repeats=100000, nthreads=2)
    print "c2", c2.next()

if __name__ == "__main__":
    main()

{% endhighlight %}

And here is the output.

{% highlight text %}
Exception in thread Thread-2:
Traceback (most recent call last):
  File "/System/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/threading.py", line 522, in __bootstrap_inner
    self.run()
  File "/System/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/threading.py", line 477, in run
    self.__target(*self.__args, **self.__kwargs)
  File "count.py", line 22, in loop
    func()
ValueError: generator already executing

c1 112106
c2 158368
{% endhighlight %}
    
The generator case failed because [generators can be shared between
threads, but they cannot be resumed from two threads at the same
time][1]. It means two threads try to call `next` method on the
generator at the same time, it will raise an exception.

In the iterator case, it only creates a [race condition][] as multiple
threads are trying to update `self.i` at the same time. That is the
reason for seeing wrong output, and it will change everytime we run
the program.This can be easily fixed by protecting that of code using
a lock.

{% highlight python %}
class Counter:
    def __init__(self):
        self.i = 0
        # create a lock
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        # acquire/release the lock when updating self.i
        with self.lock:
            self.i += 1
            return self.i
{% endhighlight %}

If we run the program now, we'll get the excpected value for c2.

    $ python count.py
    ...
    c2 200001

The similar approach won't work for generators as we don't have
control over the calling of `next` method. Whatever changes we make to
the generator function, multiple threads can still call the `next`
method at the same time.

The only way to fix it is by wrapping it in an iterator and have a
lock that allows only one thread to call `next` method of the
generator.

{% highlight python %}
class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        with self.lock:
            return self.it.next()
{% endhighlight %}
    
Now you can take any iterator or generator and make it thread-safe by
wrapping it with `threadsafe_iter`.

{% highlight python %}

# thread unsafe generator
c1 = count()

# now it is thread-safe
c1 = threadsafe_iter(c1)

{% endhighlight %}

This can be made still easier by writing a decorator.

{% highlight python %}
def threadsafe_generator(f):
    """A decorator that takes a generator function and makes it thread-safe.
    """
    def g(*a, **kw):
        return threadsafe_iter(f(*a, **kw))
    return g
{% endhighlight %}

Now we can use this decorator to make any generator thread-safe.

{% highlight python %}
@threadsafe_generator
def count():
    i = 0
    while True:
        i += 1
        yield i
{% endhighlight %}

[1]: http://mail.python.org/pipermail/python-list/2006-March/1037217.html
[race condition]: https://en.wikipedia.org/wiki/Race_condition
