from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import html2text
import aiohttp
import asyncio
import json
import os
from pathlib import Path
from src.summarizer.prompts import SUMMARIZE_COMMENTS_SYSTEM_PROMPT, SUMMARIZE_COMMENTS_USER_PROMPT
from src.utils.llm_client import LLMClient
from src.config import HN_API_BASE
from prefect import task, flow
from src.utils.helpers import extract_llm_response

@dataclass
class Comment:
    id: str
    author: str
    text: str
    timestamp: datetime
    replies: List['Comment']
    score: Optional[int] = 0
    
    def to_llm_format(self, level=0) -> str:
        """Convert comment and its replies to a format suitable for LLM"""
        # Convert HTML to plain text
        h = html2text.HTML2Text()
        h.ignore_links = True
        clean_text = h.handle(self.text).strip()
        # Format the comment
        formatted = f"[Comment by {self.author}]: {clean_text}\n"
        # Add replies indented
        if self.replies:
            formatted += "Replies:\n"
            for reply in self.replies:
                formatted += f"{' ' * (level + 2)}└─ {reply.to_llm_format(level + 2)}"
        return formatted

class HNCommentsSummarizer: 
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    @task(log_prints=True, cache_key_fn=None)
    def organize_comments_for_llm(self, comments: List[Comment], max_tokens=4000) -> List[str]:
        """
        Organize comments into chunks suitable for LLM processing
        Returns a list of conversation threads
        """
        discussion_threads = []
        current_thread = ""
        
        for comment in comments:
            thread = f"\n{comment.to_llm_format()}\n"
            # If thread is too long, start a new one
            if len(current_thread) + len(thread) > max_tokens:
                if current_thread:
                    discussion_threads.append(current_thread)
                current_thread = thread
            else:
                current_thread += thread
        # Add the last thread
        if current_thread:
            discussion_threads.append(current_thread)
        return discussion_threads

    @task(log_prints=True, cache_key_fn=None)
    async def fetch_comments(self, item_id: str) -> list:
        """Fetch comments for a Hacker News item"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{HN_API_BASE}/item/{item_id}.json") as response:
                data = await response.json()
                if not data:
                    return []
                
                comments = []
                if 'kids' in data:
                    tasks = []
                    for kid_id in data['kids']:
                        tasks.append(self.fetch_comment(kid_id))
                    comments = await asyncio.gather(*tasks)
                    # Remove None values from comments
                    comments = [c for c in comments if c]
                return comments

    async def fetch_comment(self, comment_id: str) -> dict:
        """Fetch a single comment and its replies"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{HN_API_BASE}/item/{comment_id}.json") as response:
                data = await response.json()
                if not data or data.get('deleted') or data.get('dead'):
                    return None
                
                comment = {
                    'id': data.get('id'),
                    'text': data.get('text', ''),
                    'by': data.get('by', ''),
                    'time': data.get('time', 0),
                    'replies': []
                }
                
                # Recursively fetch replies
                if 'kids' in data:
                    tasks = []
                    for kid_id in data['kids']:
                        tasks.append(self.fetch_comment(kid_id))
                    replies = await asyncio.gather(*tasks)
                    # Remove None values from replies
                    comment['replies'] = [r for r in replies if r]
                return comment


    @task(log_prints=True, cache_key_fn=None)
    async def get_comments_for_llm(self, story_id: str) -> dict:
        """Fetch and organize comments for summarization"""
        raw_comments = await self.fetch_comments(story_id)
        # Convert raw comments to Comment objects
        comments = []
        for raw in raw_comments:
            comment = Comment(
                id=str(raw['id']),
                author=raw['by'],
                text=raw['text'],
                timestamp=datetime.fromtimestamp(raw['time']),
                replies=[],
                score=0  # HN doesn't provide comment scores
            )
            
            # Convert replies recursively
            if raw['replies']:
                for reply in raw['replies']:
                    comment.replies.append(Comment(
                        id=str(reply['id']),
                        author=reply['by'],
                        text=reply['text'],
                        timestamp=datetime.fromtimestamp(reply['time']),
                        replies=[],
                        score=0
                    ))
            comments.append(comment)
        
        # Organize comments into discussion threads
        discussion_threads = self.organize_comments_for_llm(comments)
        
        return {
            'total_comments': len(raw_comments),
            'discussion_threads': discussion_threads
        }

    async def save_comments(self, story_id: str, output_dir: str = "comments"):
        """Save comments to files in both JSON and readable text formats"""
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Get current timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Fetch and organize comments
        comments_data = await self.get_comments_for_llm(story_id)
        
        # Save raw JSON
        json_path = os.path.join(output_dir, f"comments_{story_id}_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(comments_data, f, indent=2, ensure_ascii=False)
        
        # Save readable text format
        text_path = os.path.join(output_dir, f"comments_{story_id}_{timestamp}.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(f"Hacker News Story ID: {story_id}\n")
            f.write(f"Total Comments: {comments_data['total_comments']}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, thread in enumerate(comments_data['discussion_threads'], 1):
                f.write(f"Thread {i}:\n")
                f.write("-" * 40 + "\n")
                f.write(thread)
                f.write("\n\n" + "=" * 80 + "\n\n")
        
        # Save LLM-friendly format
        llm_path = os.path.join(output_dir, f"comments_{story_id}_{timestamp}_llm.txt")
        with open(llm_path, 'w', encoding='utf-8') as f:
            for i, thread in enumerate(comments_data['discussion_threads'], 1):
                f.write(f"Thread {i}:\n\n")
                f.write(thread)
                f.write("\n\n---\n\n")
        
        return {
            'json_path': json_path,
            'text_path': text_path,
            'llm_path': llm_path
        }

    @task(log_prints=True, cache_key_fn=None)
    def get_full_discussion_summary(self, comments: str) -> str:
        """Get a full summary of the discussion using an LLM"""
        user_input = SUMMARIZE_COMMENTS_USER_PROMPT.format(HN_COMMENTS=comments)
        return self.llm_client.call_llm(SUMMARIZE_COMMENTS_SYSTEM_PROMPT, user_input)

    @flow(log_prints=True)
    async def summarize_comments(self, story_id: str):
        comments = await self.get_comments_for_llm(str(story_id))
        print(f"comments: {comments}")
        summary = self.get_full_discussion_summary(comments)
        print(f"comments summary: {summary}")
        summary = extract_llm_response(summary, "summary")
        return summary

# Usage example:
if __name__ == "__main__":
    # llm_client = LLMClient(use_openrouter=True, model=OPENROUTER_MODEL_MISTRAL_3B)
    llm_client = LLMClient(use_azure=True)
    asyncio.run(HNCommentsSummarizer(llm_client).summarize_comments("41991291"))