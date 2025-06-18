# CTF Challenge Template

## Web PHP Apache Template

This template is for a simple **web** challenge, that features a simple **PHP web application** behind an **Apache server**.

Please note that with the current setup:
- The challenge's **PHP web application code** should be placed under `src/html/`.
- The challenge's **flag** should be placed under `src/flag.txt`. (you may load it in your PHP code using `$flag = file_get_contents('../flag.txt', true);`)
- You should edit the Challenge's metadata at `challenge.yml`
- The source PHP code of the web application will be provided to the player as a zip (without the flag.txt file).

The other parts of the challenge (e.g. the Docker, the Apache) are already configured.

## Testing with docker
You can build the challenge using the `make` command. If done correctly, this will generate 2 files:
- a docker image file at `dist/docker-challenge.tar`
- a source code zip file `dist/web-app-code.zip`

### Testing with a local Docker
You can use docker to test your challenge.

1. Build the docker image on docker, by running in the instant's terminal `cat ./dist/docker-challenge.tar | docker build - -t test_challenge`
2. Create a container from the test image `docker run --name testing -p 8080:80 test_challenge`
3. Open the web application on your browser at http://127.0.0.1:8080/
4. (optional) Delete the container and the image after testing `docker rm testing` and `docker rmi test_challenge`


### Testing with Play with Docker
You can use [Play with Docker](https://labs.play-with-docker.com/) to test your challenge.

1. (Once) Create an account at [docker hub](https://hub.docker.com/signup)
2. Log into [Play with Docker](https://labs.play-with-docker.com/)
3. Create a new Instance
4. Move the docker image on the instance's server, by running on your terminal inside the challenge's directory `scp dist/docker-challenge.tar xyz@direct.labs.play-with-docker.com:~/docker-challenge.tar` (replace the `xyz` with your instance info) (you can use `ssh xyz@direct.labs.play-with-docker.com` to connect and run commands)
5. Build the docker image on docker, by running in the instant's terminal `cat ./docker-challenge.tar | docker build - -t test_challenge`
6. Create a container from the test image `docker run -p 8080:80 test_challenge`
7. Open the web application on the browser by clicking the exposed port at the top of the Play with Docker website instance panel
