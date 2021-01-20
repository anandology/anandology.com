---
layout: post
title: Deploying a Static Website to IPFS
---

# {{ page.title }}
<p class="meta">21 Jan 2021 &#8211; Bangalore</p>

This is a quick tutorial to deploy your static website to [IPFS](https://ipfs.org/) from a unix machine (Linux/Mac).

Make sure you have installed [IPFS Desktop][1] or [IPFS command-line][2] installed to follow this.

Brave browser [recently added support for IPFS][3], that allows users to access `ipfs://...` urls, making it easier to access the content on IPFS.

[1]: https://docs.ipfs.io/install/ipfs-desktop/
[2]: https://docs.ipfs.io/install/command-line/
[3]: https://brave.com/ipfs-support/

## Introduction to IPFS

[IPFS](https://ipfs.org/) is a content-addressed distributed file system. When we add a file to IPFS, it is identified by it's unique hash.

Let's try to create a simple text file and add it to IPFS to understand how it works.

```
$ echo 'Hello, IPFS!' > hello.txt

$ ipfs add hello.txt
added QmWd9cavD8UGZQcqYBVhZqs2Jure5W9cgxR7S6TC4StfZe hello.txt
```

Once added the file can be accessed from any node with IPFS using the hash.

```
$ ipfs cat QmWd9cavD8UGZQcqYBVhZqs2Jure5W9cgxR7S6TC4StfZe
Hello, IPFS!
```

You can also access it from Brave browser by visiting the link [ipfs://QmWd9cavD8UGZQcqYBVhZqs2Jure5W9cgxR7S6TC4StfZe](ipfs://QmWd9cavD8UGZQcqYBVhZqs2Jure5W9cgxR7S6TC4StfZe)

## Adding a Static Website

Adding a static website to ipfs requires adding multiple HTML pages and all the assets referred from those pages.

In addition to supporting adding files, IPFS also support adding directories, which are just a mapping from name to hash of each file present in that directory. The `ipfs` command provides a way to add all files in a directory recursively.

To add a static website, go to the root of that directory (that would be `_site`, if you are building it using Jekyll) and run the followig command:

```
$ ipfs add -w -r *
added QmPJQoxjBgzPT4SA3nyypBfqeNGiKMmUJYZYnZMk4XKJaL css/style.css
added Qmces2AdZ2xX32oQ2jHFeU6ACxrAYLsTHEx19iYTNC2Ey1 index.html
...
added QmZsFP3yabWTT3nhMPuMV4sJS16vVkvwQG3U17fWiC7tio
```

The `-w` option wraps all the files specified by `*` as a directory. It is tempting to think that `ipfs add -r .` will also do the same thing, but it doesn't. It prefixes the current directory name to all filenames, breaking the links when you visit the website in IPFS.

Please note the hash printed in the last line of the output, that is the address of your website in IPFS.

Your website is now live at [ipfs://QmZsFP3yabWTT3nhMPuMV4sJS16vVkvwQG3U17fWiC7tio](ipfs://QmZsFP3yabWTT3nhMPuMV4sJS16vVkvwQG3U17fWiC7tio) (replace the text after `ipfs://` with the hash you got from the above step).

## DNSLink

While we technically added the website to IPFS, it is hard to remember and share the link with that hash. IPFS supports readable names by [DNSLink][], an approach that uses DNS TXT records for resolving the names.

You need to the following a TXT record for your domain.

```
HOSTNAME: _dnslink.<your-domain>
VALUE: dnslink=/ipfs/<hash-from-prev-step>
```

Once the TXT record is added you should be able to verify it using `dig` (replace anandology.com with your domain).

```
$ dig +short -t TXT _dnslink.anandology.com
"dnslink=/ipfs/QmZsFP3yabWTT3nhMPuMV4sJS16vVkvwQG3U17fWiC7tio"
```

That's all! Your website is now live at `ipns://<your-domain>` (please note that the schema is `ipns` and not `ipfs`).

You can also che    ck this website on ipfs at [ipns://anandology.com](ipns://anandology.com).

