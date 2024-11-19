from prefect import task, flow
from datetime import datetime
from urllib.parse import quote

def format_content(text: str) -> str:
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
    return html

# get the email template
@task(log_prints=True)
def get_hn_email_template(subject: str, stories) -> str:
    if not stories or len(stories) == 0:
        return ""
    stories_html = ""
    for story in stories:
        summary_html = format_content(story.summary)
        comments_html = format_content(story.comments_summary)
        # Encode the URLs
        safe_url = quote(story.url, safe=':/?=&')
        safe_hn_url = quote(story.hn_url, safe=':/?=&')
        stories_html += f"""
        <div class="section">
            <div class="header">{story.title}</div>
            <div class="story-meta">
                    • Article: <a href="{safe_url}" class="story-link">{story.url}</a> <br>
                    • HN Discussion: <a href="{safe_hn_url}" class="hn-link">{story.hn_url}</a> <br>
                    • Score: {story.score}
            </div>
            
            <div class="story-content">
                <h3>Article Highlights:</h3>
                <div class="content-section">{summary_html}</div>
                
                <h3>Discussion Highlights:</h3>
                <div class="content-section">{comments_html}</div>
            </div>
        </div>
        <hr class="story-divider">
        """
    return get_email_html(subject, stories_html)

@task(log_prints=True)
def get_tc_email_template(subject: str, stories) -> str:
    if not stories or len(stories) == 0:
        return ""
    stories_html = ""
    for story in stories:
        formatted_content = format_content(story.summary)
        summary_html = formatted_content
        stories_html += f"""
        <div class="section">
            <div class="header">{story.title}</div>
            <div class="story-meta">
                Article: <a href="{story.url}" class="story-link">{story.url}</a>
            </div>
            
            <div class="story-content">
                <h3>Article Highlights:</h3>
                <div class="content-section">{summary_html}</div>
            </div>
        </div>
        <hr class="story-divider">
        """
    return get_email_html(subject, stories_html)

def get_email_html(subject: str, stories_html: str) -> str:
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