# Data platform processing

## What is Astrolabe Expeditions?

[Astrolabe Expeditions](https://www.astrolabe-expeditions.org/) is an non-profit association that develops participatory science programmes with
laboratories to enable citizens to actively contribute to scientific research.

Citizens' expeditions are set up to collect large-scale scientific data and involve citizens in understanding and preserving the ocean.

## Installation

```
npm install -g serverless
```

```
pip install -r requirements.txt
```


## Testing with serverless offline

In order to test your function locally before deployment in a serverless function, you can install our python offline testing library with:

```bash
pip install -r requirements-dev.txt
```

Launch your function locally:

```bash
python src/demo.py
```

Test your local function using `curl`:

```bash
curl localhost:8080
```

## How to contribute?

We are eager for contributions and very happy when we receive them! It can be code, of course, but it can also take other forms. The workflow is explained in [the contributing guide](https://github.com/astrolabe-expeditions/data-platform/blob/dev/docs/CONTRIBUTING.md).