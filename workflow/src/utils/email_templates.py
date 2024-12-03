from prefect import task
from datetime import datetime
from urllib.parse import quote

def _format_content(title: str, text: str) -> str:
    """Format text content with proper HTML structure"""
    if not text:
        return ""
    
    # Split by bullet points (both • and -)
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        # remove quotes in the beginning and end
        line = line.strip().strip('"').strip('(').strip(')').strip("'")
        if line.startswith('-') or line.startswith('•'):
            # replace first '-' with '•'
            line = '•' + line[1:]
        formatted_lines.append(f"<li>{line}</li>")
    
    # Wrap bullet points in ul tags
    html = ""
    in_list = False
    
    for line in formatted_lines:
        if line.startswith('<li>') and not in_list:
            html += "<ul class='digest-list'>"
            in_list = True
        elif not line.startswith('<li>') and in_list:
            html += "</ul>"
            in_list = False
        html += line
    if in_list:
        html += "</ul>"
    formatted_html = f""" 
            <div class="story-content">
                <h3>{title}</h3>
                <div class="content-section">{html}</div>
            </div>
    """
    return formatted_html

def _format_story_meta(story) -> str:
    url = story.url if story.url.startswith('http') else f'https://{story.url}'
    hn_url = story.hn_url if story.hn_url.startswith('http') else f'https://{story.hn_url}'
    safe_url = quote(url, safe=':/?=&')
    safe_hn_url = quote(hn_url, safe=':/?=&')
    hn_discussion_html = f"• HN Discussion: <a href=\"{safe_hn_url}\" class=\"hn-link\">{story.hn_url}</a> <br>" if story.hn_url else ""
    score_html = f"• Score: {story.score} <br>" if int(story.score) > 0 else ""
    audio_html = f"• Text-to-Speech audio: <a href=\"{story.speech_url}\" class=\"story-link\">Listen</a> <br>" if story.speech_url else ""
    podcast_html = f"• AI-generated podcast: <a href=\"{story.notebooklm_url}\" class=\"story-link\">Listen</a> <br>" if story.notebooklm_url else ""
    return f"""
                    • Article: <a href="{safe_url}" class="story-link">{story.url}</a> <br>
                    {hn_discussion_html}
                    {score_html}
                    {audio_html}
                    {podcast_html}
    """
# get the email template
@task(log_prints=True, cache_policy=None)
def get_email_html(subject: str, stories) -> str:
    if not stories or len(stories) == 0:
        return ""
    stories_html = ""
    for story in stories:
        # Ensure URLs are absolute and properly encoded
        story_meta_html = _format_story_meta(story)
        summary_html = _format_content("Article Summary:", story.summary)
        comments_html = _format_content("Discussion Highlights:", story.comments_summary)
        stories_html += f"""
        <div class="section">
            <div class="header">{story.title}</div>
            <div class="story-meta">
                {story_meta_html}
                <div> You can listen to the audio and podcast with better experience on <a href="https://aicrafter.info" class="story-link">aicrafter.info</a>.</div>
            </div>
            {summary_html}
            {comments_html}
        </div>
        <hr class="story-divider">
        """
    return _get_email_html(subject, stories_html)

def _get_email_html(subject: str, stories_html: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Frontiers</title>
        {email_style}
    </head>
    <body>
        <div class="container">
            <div class="digest-header">
                <div class="digest-title">{subject}</div>
                <div class="digest-date">{datetime.now().strftime('%B %d, %Y')}</div>
            </div>
            {stories_html}
            <div class="footer">
                <p>
                    Built with ❤️ by <a href="https://dannyzheng.me">dannyzheng.me</a><br>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

email_style = """
<style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            .story-meta {
                font-size: 14px;
                color: #666;
                margin-bottom: 15px;
            }
            .story-link, .hn-link {
                color: #FF6F61;
                text-decoration: none;
            }
            .story-content {
                margin: 20px 0;
            }
            .story-content h3 {
                font-size: 18px;
                color: #444;
                margin: 15px 0 10px 0;
            }
            .story-content p {
                font-size: 16px;
                color: #555;
                margin: 10px 0;
            }
            .story-divider {
                border: 0;
                border-top: 1px solid #eee;
                margin: 30px 0;
            }
            .footer {
                font-size: 14px;
                color: #888;
                margin-top: 30px;
                border-top: 1px solid #ddd;
                padding-top: 20px;
                text-align: center;
            }
            .footer a {
                color: #4F46E5;
                text-decoration: none;
            }
            .digest-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .digest-title {
                font-size: 28px;
                color: #4F46E5;
                margin-bottom: 10px;
            }
            .digest-date {
                color: #666;
                font-size: 16px;
            }
            .content-section {
                margin: 15px 0;
            }
            
            .content-section p {
                margin: 10px 0;
                line-height: 1.6;
            }
            
            .digest-list {
                margin: 10px 0;
                padding-left: 20px;
                list-style: none;  /* Remove default bullets */
            }
            
            .digest-list li {
                margin: 8px 0;
                line-height: 1.6;
                position: relative;
                list-style-type: none;  /* Remove default bullets */
                padding-left: 20px;
                color: #555;  /* Match the regular text color */
            }
            
            .digest-list li:before {
                content: "•";
                position: absolute;
                left: 0;
                color: #555;  /* Match the text color */
            }
            /* For nested lists */
            .digest-list .digest-list {
                margin-top: 5px;
                margin-bottom: 5px;
            }
            
            /* Ensure proper spacing between sections */
            .story-content h3 {
                margin-top: 25px;
                margin-bottom: 15px;
            }
        </style>
    """

if __name__ == "__main__":
    test = {"html": "<p>test</p>", "title": "test"}
    print(test["html"])