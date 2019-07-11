---
layout: post
title: Python is Infinitely Beautiful!
---

# {{ page.title }}
<p class="meta">11 July 2019 &#8211; Bangalore</p>

Infinity can be quite elegantly handled in Python!

Let me demonstrate it by solving the string and week primes problem mentioned in [Infinite work is less work][1] by Damian Conway. 

## The Problem

Write a script to generate first 10 strong and weak prime numbers.

A prime `p[n]` is "strong" if it's larger than the average of its two neighbouring primes (i.e. `p[n] > (p[n-1]+p[n+1])/2`). A prime is "weak" if it's smaller than the average of its two neighbours.

## The Solution

To find first `n` strong primes, we don't know how many primes we may have to look at. Wound't it be easier if we first generate infinite primes and then look at as many that are required? Belive me, it is not hard to generate infinite primes in Python!

Let me convince you by generating infinite integers first.

```
def integers(start=1):
    """Generates infinite integers from a starting number.
    """
    while True:
        yield start
        start += 1
```

What to print all of them? Please don't try the following. It'll go on printing...

```
for i in integers():
    print(i)
```

Well, we need a smarter way to look into this infinite sequence. How about taking at first few elements? 

```
def take(n, seq):
    return (x for x, _ in zip(seq, range(n)))
```

How about taking 10 integers? 

```
>>> list(take(10, integers()))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

The `take` function returns a generator, we need to convert that into a list to see all those values.

Ready to generate primes now?

```
def primes():
    return (n for n in integers(start=2) if is_prime(n))
```

That's all! Don't beleive? Take first 10 primes and see!

```
>>> list(take(10, primes()))
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

Finding strong/week primes is tricky. We need to know the prime before and the prime after. How about we take triplets of consecutive primes? 

```
def triplets(seq):
    """Returns the consecutive triplets from the given sequence.

        >>> for a, b, c in triplets([1, 2, 3, 4, 5]):
        ...     print(a, b, c)
        ...
        1 2 3
        2 3 4
        3 4 5
    """
    seq = iter(seq)
    a = next(seq)
    b = next(seq)
    c = next(seq)
    while True:
        yield a, b, c
        a, b, c = b, c, next(seq)
``` 

Isn't that easy? With `triplets` in place, finding strong and week primes a cake walk. 

```
strong_primes = (b for a, b, c in triplets(primes()) if b+b > a+c)
week_primes = (b for a, b, c in triplets(primes()) if b+b < a+c)
```

And remember, we still have infinite of these.

Since we just need first 10 of them, let's take 10 and print them.

```
print("STRONG\tWEEK")
for sp, wp in take(n, zip(strong_primes, week_primes)):
    print("{:6d}\t{:4d}".format(wp, sp))
```

And here we go!

```
STRONG  WEEK
     3    11
     7    17
    13    29
    19    37
    23    41
    31    59
    43    67
    47    71
    61    79
    73    97
```

Liked it? Here is the [full program][gist]!

[1]: http://blogs.perl.org/users/damian_conway/2019/07/infinite-work-is-less-work.html
[gist]: https://gist.github.com/anandology/90c4a7dadbb650cd7d5c4645b94e5b30