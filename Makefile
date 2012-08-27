
build: includes
	jekyll

includes:
	cd _includes && make

server: includes
	jekyll --server 8080

push:
	rsync -avzc _site/* anandology.com:/var/www/anandology.com/ 
