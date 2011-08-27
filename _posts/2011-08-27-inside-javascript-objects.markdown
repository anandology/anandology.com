---
layout: post
title: Inside Javascript Objects
---

# {{ page.title }}
<p class="meta">17 Aug 2011 &#8211; Bangalore</p>

Javascript is an interesting programming language. Unlike traditional programming languages, it has a prototype-based object system.

Here is my attempt to explain the nut and bolts of Javascript language and how its objects work.

<style type="text/css">
    .note {
        margin: 10px 0px;
        padding: 10px;
        background: #ffffcc;
        border: 1px solid #ccccaa;
    }
</style>

<!--

Table of Contents:

* Objects
* Functions
* Prototype
* new operator
* instanceof operator
* Implementing Classical Inheritance in Javascript
* Implementing Python like Classes in Javascript
-->

## Objects

There are many ways to create an object, the simplest form is this:

    p = {x:1, y:2};
    
The properties of the object are accessed using the `.` notation and new properties can be added at runtime.

    a = p.x;     // 1
    b = p.y;     // 2
    p.z = p.x + p.y; // p.z is 3

Even the primitive objects like numbers work exactly in the same way.

    x = 1;
    x.newprop = "hello";

## Functions

Functions are special objects which are callable.

    function square(x) { return x*x; }
    square(4); // returns 16
    
The body of the function has access to two magic variables: `this` and `arguments`. 

A function is always executed in the context of an object, accessible as
variable `this`. The list of arguments passed to the function is accessible as
variable `arguments`. 

The value of `this` variable depends on how the function is called. When a
function `f` is called as called as `a.f()`, the object `a` becomes the `this`
variable. When called directly as `f()`, the top-level object becomes the `this`
variable.

<div class="note">
    Javascript has a top-level object, that maintains the global variables.
    In the context of web browser, the top-level object is the <code>window</code> object.
</div>

The function object has an `apply` method. Calling `square(2)` is equivalent
to calling:

    square.apply(null, [2])

The first argument is the `this` object and the second one is the list of
arguments. When `null` is specified as first argument, the system uses the
top-level object as `this`.

An example to demonstrate `this`:

    function square_method() {
        return this.value * this.value;
    }
    
    var n = {"value": 2};
    n.square = square_method;
    
    n.square(); // returns 4
    square_method.apply(n, []); // returns 4

    var sq = n.square;
    sq(); // produces error as this.value is undefined. 

And another simple example to demonstrate `arguments`:

    function count() {
        return arguments.length;
    }
    
    count();        // 0
    count(1, 2, 3); // 3
    count(4, 5);    // 2

## Prototype    

There is another way to create objects, using the `new` operator.

    function Point(x, y) {
        this.x = x;
        this.y = y;
    }
    var p = new Point(3, 4);
    
The `new` operator creates a new object and passes it as `this` object to the
`Point` function.

Every function has a special property `prototype` and all the properties of
the prototype object are accessible to the objects created using that function.
    
    Point.prototype.name = "Point"; // Adding a name property to prototype
    p.name; // returns "Point"

If we add a name property to `p`, it effects only that object and not the
prototype.

    p.name = "p";
    Point.prototype.name; // will still be "Point"
    
The prototype object is typically used for adding methods.

    Point.prototype.magnitude = function() {
        return Math.sqrt(this.x*this.x + this.y*this.y);
    }
    
    p.magnitude(); // returns 5
    
Some Javascript engines add a special property `__proto__` to each object, which points to it's function prototype.

    p.__proto__ == Point.prototype; // true

Here is a diagram showing 2 Point objects.

    p1
    +-----------+
    | x         |---> 1
    +-----------+                   
    | y         |---> 2             
    +-----------+                   
    | __proto__ |--------------+--> Point.prototype
    +-----------+              |    +--------------+
                               |    | name         | --> "Point"
                               |    +--------------+
    p2                         |    | magnitude    | --> function() {...}
    +-----------+              |    +--------------+
    | x         |---> 5        |
    +-----------+              |
    | y         |---> 7        |
    +-----------+              |
    | __proto__ |--------------+
    +-----------+

Now lets try something ambitious, implementing the functionality of new operator. (Works only in JS engines where `__proto__` is supported.)

    function new_operator(func, args) {
        var obj = {};
        obj.__proto__ = func.prototype;
        func.apply(obj, args);
        return obj;
    }
    
    var p1 = new_operator(Point, [1, 2]);
    p1 instanceof Point; // true
    p1.x; // 1
    p1.y; // 2
    
Even the prototype object is not any special. Function prototype can be changed too.
    
    function F() {}
    F.prototype = {"x": 1};
    f = new F();
    f.x; // 1

We know that when a property is accessed, it is first looked up in the object,
failing there, the prototype is looked up. What happens if the property is not
found even there? 

Yes, you guessed it right, it is recursive. The prototype of the prototype is looked up.

Lets try an example:

    function F() {
        this.f = "F";
    }
    
    function G() {
        this.g = "G";
    }
    G.prototype.h = "H";
    
    // Here is the magic. Prototype of F is an instance of G.
    F.prototype = new G(); 
    
    x = new F();
    
    x.f; // "F"
    x.g; // "G"
    
    x instanceof G; // true
    x instanceof F; // true

We have now implemented object inheritance in Javascript!

    x                  +-> F.prototype        +-> G.prototype
    +-----------+      |  +-----------+       |  +-----------+        
    | f         |->"F" |  | g         |-> "G" |  | h         |-> "H" 
    +-----------+      |  +-----------+       |  +-----------+        
    | __proto__ |------+  | __proto__ |-------+  | __proto__ |-> some-other-object
    +-----------+         +-----------+          +-----------+        
                         

## The instanceof operator

Quoting [Mozilla docs][mdn-instanceof]:

<div class="note">
    The <code>instanceof</code> operator tests whether an object has in its prototype chain the prototype property of a constructor.
    <br/>
    <br/>
    Syntax: <code>object instanceof constructor</code>
</div>

In simple words, it lets you find if an object is instance of a function.

Using the examples from the previous section:

    var p = new Point(3, 4);
    p instanceof Point; // true
    p instanceof Object; // true
    
    x = new F();
    x instanceof G; // true
    x instanceof F; // true
    x instanceof Object; // true

One more example to understand it better.

    function F() {}
    function G() {}
    
    f = new F();
    f instanceof F; // true
    f instanceof G; // false
    
    G.prototype = F.prototype; 
    f instanceof G; // true
    f instanceof F; // true

So, `obj instanceof func` just checks whether or not the `func.prototype` occurs anywhere in the prototype chain of the object `obj`. 

Now lets try to implement the `instanceof` operator as a function. Again, this only works in the JS engines which support `__proto__`.

    function  my_instanceof(object, constructor) {
        if (object === Object.prototype)
            return false;
        return (object.__proto__ === constructor.prototype 
            || my_instanceof(object.__proto__, constructor));
    }
    
There are slight deviations in the behavior of `instanceof` and `my_instanceof` for primitive objects like numbers.

    my_instanceof(1, Number);   // true
    my_instanceof(1, Object);   // true
    
    1 instanceof Number;    // false
    1 instanceof Object;    // false
    
I'm not sure why it has this behavior.

## Implementing Classical Inheritance

Now lets try to create classes similar to the traditional programming languages like Java and Ruby. Here is what we should achieve:

<!--
    var Point = Class({
        init: function(x, y) {
            this.x = x;
            this.y = y;
        },
        magnitude: function() {
            return Math.sqrt(this.x*this.x + this.y*this.y);
        },
        // Finds distance to another point.
        distance: function(p) {
            var dx = this.x - p.x;
            var dy = this.y - p.y;
            return Math.sqrt(dx*dx + dy*dy);
        }
    });
    
    var p = new Point(3, 4);
    p instanceof Point; // should be true 
    p.magnitude(); // should be 5
-->

    var Animal = Class({
        init: function(name) {
            this.name = name;
        },
        eat: function() {
            return this.name + " is eating";
        }
    });
    
    var a = new Animal("dog");
    a.eat();    // "dog is eating"    

Here is the first attempt.

    // Version 1 of Class implementation.
    function Class(members) {
        var F = function() {
            if (members.init) {
                members.init.apply(this, arguments);
            }
        };
        F.prototype = members;
        return F;
    }
    
We created a new function with prototype set to the provided `members` and it calls the `init` function.

So far so good. Now we can create classes with much ease, but what about inheritance? Lets say, we want to extend `Animal` class and create `Bird` class.

Lets borrow [some ideas][prototypal] from [Douglas Crockford][crockford]. 

    function object(o) {
        function F() {}
        F.prototype = o;
        return new F();
    }

<div class="note">
"The object function untangles JavaScript's constructor pattern, achieving true
prototypal inheritance. It takes an old object as a parameter and returns an
empty new object that inherits from the old one."
</div>

Here is what it does:

    y = object(x);
    
     y                x
    +-----------+    +-----+
    | __proto__ |--->| ... |
    +-----------+    +-----+

With this utility, we can add an `extend` function our Class:

    // Version 2 of Class implementation
    function Class(members) {
        var F = function() {
            if (members.init) {
                members.init.apply(this, arguments);
            }
        };
        F.prototype = members;
        
        F.extend = function(members) {
            // Creating new object using the prototype of F
            var new_members = object(F.prototype);
            
            // and adding members to it.
            for (var name in members) {
                new_members[name] = members[name];
            }
            return Class(new_members);
        };
        
        return F;
    }
    
Lets try an example:

    var Bird = Animal.extend({
        fly: function() {
            return this.name + " is flying";
        }
    });

    var b = new Bird("sparrow");
    b.fly();    // sparrow is flying
    b.eat();    // sparrow is eating

    b instanceof Bird;      // true
    b instanceof Animal;    // true
    
Here is how it looks:

    b                +--> Bird.prototype  +--> Animal.prototype 
    +-----------+    |   +-----------+    |   +-----+
    | name      |    |   | fly       |    |   | ... |
    +-----------+    |   +-----------+    |   +-----+
    | __proto__ |----+   | __proto__ |----+   
    +-----------+        +-----------+

## Further Reading

There are a lot of interesting resources about implementing prototype-based inheritance. Here are a few:

* [Prototypal Inheritance in JavaScript - Douglas Crockford][prototypal]
* [Simple JavaScript Inheritance - John Resig](http://ejohn.org/blog/simple-javascript-inheritance/)
* [JavaScript parasitic inheritance, power constructors and instanceof.](http://higher-order.blogspot.com/2008/02/javascript-parasitic-inheritance-super.html)

  [prototypal]: http://javascript.crockford.com/prototypal.html
  [crockford]: http://www.crockford.com/
  [mdn-instanceof]: https://developer.mozilla.org/en/JavaScript/Reference/Operators/Special_Operators/instanceof_Operator
  
<!--

jsFoo Talk:

Title:

Inside Javascript

Objective:

Understand the nuts and bolts of Javascript language and its object system. This talk is *not* about DOM or browsers.

Description:

Javascript has prototype based object system, which is not straight-forward
for people trained in mainstream programming languages. This talk presents
in-depth insights about the Javascript language and its object model. 

Topics covered:

* Objects
* Functions
* Prototype
* The `new` Operator
* The `instanceof` Operator
* Implementing Classical Inheritance in Javascript

-->