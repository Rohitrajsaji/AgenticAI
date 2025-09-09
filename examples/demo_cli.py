import click
from agentic_ai.agent import Agent
from agentic_ai.config import AgentConfig


@click.command()
@click.argument("goal", nargs=-1)
@click.option("--model", default="gpt-4o-mini")
@click.option("--max-steps", default=8)
def main(goal, model, max_steps):
    goal_text = " ".join(goal).strip()
    agent = Agent(AgentConfig(model=model, max_steps=max_steps))
    answer = agent.run(goal_text)
    click.echo("\n=== Final Answer ===\n")
    click.echo(answer)


if __name__ == "__main__":
    main()
