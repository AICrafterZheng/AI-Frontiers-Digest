constraints_and_example = """
    Constraints:
    1. Please give headline and list down the 3 key points as bullet points. I'm particularly interested in key points and any significant technological advancements or implications discussed.
    2. If there are any fund raising details, please include the amount, the investors and valuation. If no fund raising info, just don't mention it."
    3. Please DON't include the words "Headline" and "Key points" in the output.
    4. I'm going to post this on my social media account, please make it concise and engaging.
    5. Don't include any duplicate info. Thank you!
    6. Please don't include links.
    7. Please don't repeat the hash tags.
    8. Please don't repeat the same text.
    
    Example output:
    Apple Introduces Private Cloud Compute for Enhanced AI Privacy.
    • Apple has unveiled Private Cloud Compute (PCC), a cloud intelligence system designed to enhance the privacy of AI processing in the cloud. The system ensures user data sent to PCC isn't accessible to anyone, not even Apple, extending the security and privacy of Apple devices into the cloud.
    • The PCC system is built with custom Apple silicon and a secure operating system. It is designed to fulfill user requests using complex machine learning models while maintaining privacy. The system maintains user data on PCC nodes only until the response is returned and does not retain any data afterward.
    • To ensure the integrity of the system, Apple is making software images of every production build of PCC publicly available for scrutiny by the security research community. The company will also release a PCC Virtual Research Environment and a subset of the security-critical PCC source code to aid research.
"""
INITIAL_SUMMARIZE_SYSTEM_PROMPT = """
You are a tech journalist writing a summary of a tech article. You will be provided with a tech article and you need to summarize it in a concise and engaging manner that can be posted on social media like Twitter.
"""

INITIAL_SUMMARIZE_USER_PROMPT = """Your task is to carefully read a source text and the summary of the text.
{constraints_and_example}
<SOURCE_TEXT>
{tagged_text}
</SOURCE_TEXT>
"""

# Reflection
REFLECTION_SUMMARIZE_SYSTEM_PROMPT = """You are a tech journalist writing a summary of a tech article. You will be provided with a source text and its summary, and your goal is to improve the summary to make it engaging manner to post on social media like Twitter."""
REFLECTION_SUMMARIZE_USER_PROMPT = """Your task is to carefully read a source text and the summary of the text, and then improve the summary, and then give constructive criticism and helpful suggestions for improving the summary.
<SOURCE_TEXT>
{tagged_text}
</SOURCE_TEXT>

The summary of the indicated part, delimited below by <SUMMARY> and </SUMMARY>, is as follows:
<SUMMARY>
{summary}
</SUMMARY>

When writing suggestions, pay attention to whether there are ways to improve the summary's:\n\
(i) accuracy (by correcting errors of addition, missummary, omission, or unsummaried text),\n\
(ii) fluency (by applying grammar, spelling and punctuation rules, and ensuring there are no unnecessary repetitions),\n\
(iii) style (by ensuring the summaries is in a enaging mananer of social media post),\n\
(iv) terminology (by ensuring terminology use is consistent and reflects the source text domain;).\n\
{constraints_and_example}
Write a list of specific, helpful and constructive suggestions for improving the summary.
Each suggestion should address one specific part of the summary.
Output only the suggestions and nothing else.
"""

FINAL_SUMMARIZE_SYSTEM_PROMPT = """You are a tech journalist writing a summary of a tech article."""
FINAL_SUMMARIZE_USER_PROMPT = """
Your task is to carefully read, then improve a summary, taking into
account a set of expert suggestions and constructive criticisms. Below, the source text, initial summary, and expert suggestions are provided.

The source text is below, delimited by XML tags <SOURCE_TEXT> and </SOURCE_TEXT>, and the part that has been summarized
is delimited by <SUMMARIZE_THIS> and </SUMMARIZE_THIS> within the source text. You can use the rest of the source text
as context, but need to provide a summary only of the part indicated by <SUMMARIZE_THIS> and </SUMMARIZE_THIS>.

<SOURCE_TEXT>
{tagged_text}
</SOURCE_TEXT>

The summary of the indicated part, delimited below by <SUMMARIZE_THIS> and </SUMMARIZE_THIS>, is as follows:
<SUMMARIZE_THIS>
{summary}
</SUMMARIZE_THIS>

The expert summarys of the indicated part, delimited below by <EXPERT_SUGGESTIONS> and </EXPERT_SUGGESTIONS>, is as follows:
<EXPERT_SUGGESTIONS>
{reflection}
</EXPERT_SUGGESTIONS>

Taking into account the expert suggestions rewrite the summary to improve it, paying attention
to whether there are ways to improve the summary's
(i) accuracy (by correcting errors of addition, missummary, omission, or unsummaried text),\n\
(ii) fluency (by applying grammar, spelling and punctuation rules, and ensuring there are no unnecessary repetitions),\n\
(iii) style (by ensuring the summaries is in a enaging mananer of social media post),\n\
(iv) terminology (by ensuring terminology use is consistent and reflects the source text domain;).\n\

{constraints_and_example}
Output only the new summary of the indicated part and nothing else. Don't include your thoughts or reflections.
"""

EXTRACT_CONTENT_SYS_PROMPT= "You are a helpful assistant that extracts the content from the jina reader that is relevant to the topic of the url"

EXTRACT_CONTENT_USER_PROMPT = """
You are tasked with extracting text content related to a specific topic from a given URL content returned by jina reader. The content may contain a mix of information, including image URLs and text. Your goal is to identify and extract only the text that is relevant to the provided topic.

First, you will be given the content from jina reader:

<jina_reader_content>
{JINA_READER_CONTENT}
</jina_reader_content>

Your task is to extract text content related to the following topic:

<topic>
{TOPIC}
</topic>

Follow these steps to complete the task:

1. Carefully read through the entire Jina Reader content.

2. Identify sections or paragraphs that are relevant to the given topic. Consider keywords, phrases, and context that relate to the topic.

3. Extract only the text content that is directly related to the topic. Ignore any image URLs, advertisements, or unrelated text.

4. If you find relevant content, format it as follows:
   - Remove any HTML tags or formatting
   - Separate distinct ideas or paragraphs with line breaks
   - Preserve the original wording and order of the extracted text
   - Remove any duplicate text
   - Don't include your thoughts or reflections

5. Present the extracted text inside <extracted_content> tags.

6. If you cannot find any content related to the given topic, respond with "No relevant content found" inside the <extracted_content> tags.

Remember to focus only on the text content and ignore any images or non-textual elements. Ensure that the extracted content is directly relevant to the given topic.

Begin your response with the extracted content:
"""

SUMMARIZE_COMMENTS_SYSTEM_PROMPT = """You are a tech journalist writing a summary of comments from Hacker News."""

SUMMARIZE_COMMENTS_USER_PROMPT = """
You are tasked with summarizing comments from Hacker News. Your goal is to provide a concise and informative summary that captures the main points and sentiment of the discussion. Follow these instructions carefully:

1. You will be given a set of Hacker News comments to summarize:

<hn_comments>
{HN_COMMENTS}
</hn_comments>

2. To create your summary, follow these steps:
   a. Read through all the comments carefully.
   b. Identify the main topics, themes, and points of discussion.
   c. Note any significant agreements or disagreements among commenters.
   d. Recognize the overall sentiment of the discussion.
   e. Highlight any unique insights or particularly valuable contributions.

3. Your summary should:
   - Be objective and unbiased.
   - Accurately represent the proportion of different viewpoints expressed.
   - Avoid focusing too much on any single comment unless it's particularly influential to the discussion.
   - Use neutral language to describe the discussion.
   - Not include your own opinions or additional information not present in the comments.

4. Format your summary as follows:
   - Use complete sentences.
   - Use bullet points or numbering.

5. Output your summary within <summary> tags.

Remember, your goal is to provide a balanced, informative overview of the discussion that someone could quickly read to understand the key points and tone of the conversation."""