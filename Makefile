
build: includes
	jekyll build

includes:
	cd _includes && make

server: includes
	jekyll serve

push:
	rsync -avzc _site/* anandology.com:/var/www/anandology.com/ 
