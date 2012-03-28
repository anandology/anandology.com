
build:
	jekyll

server:
	jekyll --server 8080

push:
	rsync -avz _site/* anandology.com:/var/www/anandology.com/ 
