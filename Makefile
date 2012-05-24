
build:
	jekyll

server:
	jekyll --server 8080

push:
	rsync -avzc _site/* anandology.com:/var/www/anandology.com/ 
