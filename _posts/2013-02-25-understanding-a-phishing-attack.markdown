---
layout: post
title: Understanding a phishing attack
---

# {{ page.title }}
<p class="meta">25 February 2013 &#8211; Bangalore</p>

I opened my mailbox today and found a lot of messages from friends saying that they got a twitter DM (Direct Message) from me, with a phishing link. I opened twitter and looked at sent messages and found a lot of them but none of them were sent by me. I was sure that my twitter accont was compromised.

## Understanding the phishing attack

One of the tinyurl used in one of the DMs was `http://bit.ly/YQPCXA`. I've wanted to find what it is doing.

    $ curl -I  http://bit.ly/YQPCXA 
    HTTP/1.1 301 Moved
    Server: nginx
    Date: Mon, 25 Feb 2013 02:30:25 GMT
    Content-Type: text/html; charset=utf-8
    Connection: keep-alive
    Set-Cookie: _bit=512accc1-00036-074ec-3d1cf10a;domain=.bit.ly;expires=Sat Aug 24 02:30:25 2013;path=/; HttpOnly
    Cache-control: private; max-age=90
    Location: http://surl.dk/bvi?fpma
    MIME-Version: 1.0
    Content-Length: 115

That is a redirect to `http://surl.dk/bvi?fpma`. Followed it again.

    $ curl -I http://surl.dk/bvi?fpma
    HTTP/1.1 302 Moved Temporarily
    Date: Mon, 25 Feb 2013 02:30:31 GMT
    Server: Apache mod_fcgid/2.3.6
    X-Powered-By: PHP/5.3.18
    Location: http://trvitter.com/r3
    Content-Type: text/html

Still another redirect. followed it too.

    $ curl -I http://trvitter.com/r3
    HTTP/1.1 301 Moved Permanently
    Date: Sun, 24 Feb 2013 20:24:39 GMT
    Server: Apache/2.2.15 (CentOS)
    Location: http://trvitter.com/r3/
    Connection: close
    Content-Type: text/html; charset=iso-8859-1

`trvitter.com`? This looks like a fishing attack. Notice that the domain name looks similar to `twitter.com'.

    $ curl -i http://trvitter.com/r3/
    HTTP/1.1 200 OK
    Date: Sun, 24 Feb 2013 20:26:22 GMT
    Server: Apache/2.2.15 (CentOS)
    Last-Modified: Sun, 24 Feb 2013 20:26:22 GMT
    ETag: W/"ffcd2-4d-4d68239c2c180"
    Accept-Ranges: bytes
    Content-Length: 77
    Connection: close
    Content-Type: text/html; charset=UTF-8

    <meta http-equiv="refresh" content="0; URL=/g/verify/?&account_secure_login">

Another redirect, this time using a `meta` tag. Followed that too.

    $ curl -i 'http://trvitter.com/g/verify/?&account_secure_login'
    ...
    <!DOCTYPE html>
    <html>
      <head>
        ...
        <title>Sign in to Twitter</title>
        ...

Got it! This is a fake twitter login. Looks like the following when opened in a browser.

<img src="/files/2013/fake-twitter-login.png" alt="Fake twitter page" style="width: 100%" />

My account would have been compromized after I have clicked one of such phishing links and gave my twitter credentials to a malicious cracker.

## How to secure Twitter account after phishing attack

**Step 1: Change your password.**

Use the [advice of xkcd][1] to pick a strong password.

[1]: http://xkcd.com/936/

**Step 2: Delete all messages sent from your account.**

This'll prevent people from compromising their accounts by clicking the phishing link.

The twitter website doesn't allow a way to delete multiple DMs at once. I found that
[www.dmcleaner.com](http://www.dmcleaner.com/) is very useful for this task. You'll have authorize
it via Twitter to use it.

**Step 3: Revoke access to all unwanted apps that are authorized by you.**

You can find them on `Apps` tab on Twitter settings page.

See the Twitter Help Center article ["My Account Has Been Compromised"][2] for more tips about securing Twitter account.

[2]: https://support.twitter.com/articles/31796-my-account-has-been-compromised

After you secure your account, make sure you [report the phishing link(s) to Google][3]. Google Chrome and Firefox uses that database to warn users when they try to visit those web pages.

[3]: http://www.google.com/safebrowsing/report_phish/
