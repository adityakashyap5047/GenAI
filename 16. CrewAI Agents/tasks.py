from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

### Research Task
research_task = Task(
    description=(
        "Identify the video {topic}."
        "Get detailed information about the video from the channel."
    ),
    expected_output='A comprehensive 3 paragraph long report based on the {topic} of video content.',
    tools=[yt_tool],
    agent=blog_researcher
)

