from crewai import Agent
from tools import yt_tool

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

### Create a senior blog content researcher

blog_researcher = Agent(
    role='Blog Researcher from Youtube Videos',
    goal='get the relevant video content for the topic {topic} from YT channels',
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding videos in AI Data Science, Machine Learning and Gen AI and providing suggestion"
    ),
    tools=[yt_tool],
    allow_delegation=True ### Pass to share the task to other agents
)

### Create a senior blog writer with YT tool
blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from YT channels',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an acessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False
)