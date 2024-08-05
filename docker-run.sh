#!/bin/bash
user="mygo"
name="mygo-api"
port=3150

docker build \
    $@ -t $user/$name:latest . || exit
[ "$(docker ps | grep $name)" ] && docker kill $name
[ "$(docker ps -a | grep $name)" ] && docker rm $name

docker run \
	-itd \
	-u $(id -u):$(id -g) \
    -p $port:3000 \
	--name $name \
	$user/$name:latest