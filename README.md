# health-ai-talk
Code for our talk at the [Out of Pocket Healthcare AI Hackathon](https://www.outofpocket.health/ai-hackathon)

## Setup
Install [portaudio](https://formulae.brew.sh/formula/portaudio) which is needed for some of the audio processing.

The repo uses [pdm](https://pdm-project.org/en/latest/#installation). After installing pdm, run:
```
pdm install
```

Create a `.env` file with `OPENAI_API_KEY` and optionally an `ELEVEN_API_KEY`
```
OPENAI_API_KEY="sk-***"
ELEVEN_API_KEY="***"
```

## Running
The main entrypoint is a [typer](https://typer.tiangolo.com/) CLI

See available commands with:
```
pdm cli --help
```

For example, to ask for a single response, run:
```
pdm cli ask "What's up?"
```
