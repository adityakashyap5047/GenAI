from crewai import Agent

### Create a senior blog content researcher

blog_researcher = Agent(
    role='Blog Researcher from Youtube Videos',
    goal='get the relevant video content for the topic {topic} from YT channels',
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding videos in AI Data Science, Machine Learning and Gen AI and providing suggestion"
    ),
    tools=[],
    allow_delegation=True
)