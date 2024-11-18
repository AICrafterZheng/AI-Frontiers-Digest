from prefect import task, get_run_logger
import resend
import asyncio
from typing import List, Dict
from src.utils.supabase_utils import supabase
from src.config import RESEND_API_KEY

class EmailSender:
    def __init__(self, api_key: str, from_email: str, batch_size: int = 50, max_concurrent: int = 10):
        self.api_key = api_key
        self.from_email = from_email
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        
    async def send_single_email(self, subject: str, message: str, to_email: str) -> Dict:
        """Send a single email and return result"""
        if not message or not to_email:
            print("Message or recipient email is empty")
            return {"status": "error", "email": to_email, "error": "Empty message or recipient"}
            
        try:
            params = {
                "from": self.from_email,
                "to": [to_email],  # Send to single recipient
                "subject": subject,
                "html": message,
            }
            r = resend.Emails.send(params)
            print(f"✓ Sent to {to_email}")
            return {
                "status": "success",
                "email": to_email,
                "response": r
            }
        except Exception as error:
            print(f"✗ Error sending to {to_email}: {error}")
            return {
                "status": "error",
                "email": to_email,
                "error": str(error)
            }

    async def process_batch(self, emails: List[str], subject: str, html_content: str) -> List[Dict]:
        """Process a batch of emails concurrently"""
        tasks = []
        for email in emails:
            task = self.send_single_email(subject, html_content, email)
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def send_all(self, emails: List[str], subject: str, html_content: str) -> Dict:
        """Send emails to all recipients in parallel batches"""
        if not emails:
            return {"success": 0, "error": 0, "results": []}

        results = []
        total = len(emails)
        
        # Process in batches
        for i in range(0, total, self.batch_size):
            batch = emails[i:i + self.batch_size]
            print(f"Processing batch {i//self.batch_size + 1} ({len(batch)} recipients)")
            
            batch_results = await self.process_batch(batch, subject, html_content)
            results.extend(batch_results)
            
            # Small delay between batches
            if i + self.batch_size < total:
                await asyncio.sleep(1)

        # Calculate statistics
        successes = sum(1 for r in results if r["status"] == "success")
        errors = sum(1 for r in results if r["status"] == "error")

        return {
            "success": successes,
            "error": errors,
            "total": total,
            "results": results
        }

@task(log_prints=True)
async def send_emails(subject: str, message: str, to_emails: List[str] = None) -> Dict:
    """Prefect task to send emails in parallel"""
    logger = get_run_logger()
    try:
        if not message or message == "":
            print("Message is empty")
            return {"success": 0, "error": 0, "total": 0, "results": []}
        
        emails = to_emails if to_emails else get_emails()
        if not emails:
            print("No recipients found")
            return {"success": 0, "error": 0, "total": 0, "results": []}
        
        print(f"Preparing to send to {len(emails)} recipients")
    
        sender = EmailSender(
            api_key=RESEND_API_KEY,
            from_email="AI Frontiers <newsletter.digest@aicrafter.info>",
            batch_size=50,
            max_concurrent=10
    )

        results = await sender.send_all(emails, subject, message)
        
        # Print summary
        print(f"\nEmail sending complete:")
        print(f"Total recipients: {results['total']}")
        print(f"Successfully sent: {results['success']}")
        print(f"Failed: {results['error']}")
        return results
    except Exception as e:
        logger.error(f"Error sending emails: {e}")
        return {"success": 0, "error": 0, "total": 0, "results": []}

# get the emails from supabase
@task(log_prints=True)
def get_emails():
    try:
        response = supabase.table("NewsletterSubs")\
                          .select("*")\
                          .eq("unsubscribed", False)\
                          .execute().data
        print(f"Found {len(response)} active subscribers")
        emails = [email['email'] for email in response]
        return emails
    except Exception as error:
        print(f"Error fetching emails: {error}")
        return []