alias bc:=build-container
alias up:=container-up

build-container:
    docker build -t ragavan .

container-up:
    docker compose up

lint:
    -pylint --recursive y .
