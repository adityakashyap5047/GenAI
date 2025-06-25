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

### Writing Task
writing_task = Task(
    description=(
        "get the info from the youtube channel on the topic {topic}."
    ),
    expected_output='Summarize the info from the youtube channel video on the topic {topic} in a compelling blog post.',
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,  ###if True then both tasks will run in parallel
    output_file='blog_post.md'
)