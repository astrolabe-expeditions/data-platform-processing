# Data platform processing

## What is Astrolabe Expeditions?

[Astrolabe Expeditions](https://www.astrolabe-expeditions.org/) is an non-profit association that develops participatory science programmes with
laboratories to enable citizens to actively contribute to scientific research.

Citizens' expeditions are set up to collect large-scale scientific data and involve citizens in understanding and preserving the ocean.

## Local development with docker

You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux.

Clone the repository
```sh
git clone git@github.com:astrolabe-expeditions/data-plateform-processing.git
```

Switch to the repo folder
```sh
cd data-plateform-processing
```

Copy the example env file and make the required configuration changes in the .env file
```sh
cp .env.example .env
```

Build everything
```sh
docker compose up --build
```

You can now access the server at [http://localhost:8080](http://localhost:8080)

## How to contribute?

We are eager for contributions and very happy when we receive them! It can be code, of course, but it can also take other forms. The workflow is explained in [the contributing guide](https://github.com/astrolabe-expeditions/data-plateform-processing/blob/main/docs/CONTRIBUTING.md).