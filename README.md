# Nltosql Crew

Welcome to the Nltosql Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, create and activate a virtual environment using uv and install the
dependencies defined in `pyproject.toml`:

```bash
uv venv        # create a .venv folder
source .venv/bin/activate
uv sync        # install packages from pyproject/uv.lock
```

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

Copy `.env.example` to `.env` and set the values for your environment:

```bash
cp .env.example .env
```

- Modify `src/nltosql/config/agents.yaml` to define your agents
- Modify `src/nltosql/config/tasks.yaml` to define your tasks
- Modify `src/nltosql/crew.py` to add your own logic, tools and specific args
- Modify `src/nltosql/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the nlToSql Crew, assembling the agents and assigning them tasks as defined in your configuration.

If you prefer to use the web interface, start the Flask server:

```bash
flask --app src.app run
```

This example, unmodified, will create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The nlToSql Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Nltosql Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
