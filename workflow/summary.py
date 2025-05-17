

from src.summarizer.simple_summarizer import SimpleSummarizer
from src.utils.llm_client import LLMClient
from src.utils.helpers import extract_llm_response
from src.summarizer.prompts import podcast_system_prompt, podcast_user_prompt
from src.common import LLMProvider

def summarize_file( llm_client: LLMClient, content: str, output_file: str, chunk_size: int = 10000, chunking: bool = False) -> None:
    try:
        # Read the input file
        # with open(file_path, 'r', encoding='utf-8') as file:
        #     content = file.read()

        # Split the content into chunks
        if chunking:
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        else:
            chunks = [content]

        # Summarize each chunk
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk {i+1}/{len(chunks)}, length: {len(chunk)}")
            # prompt = chunk_prompt.format(previous_summary=previous_summary, chunk_transcript=chunk, language=language)
            prompt = podcast_user_prompt.format( HIGHLIGHTS=highlights, TRANSCRIPT=chunk)

            summary = llm_client.call_llm(sys_prompt=podcast_system_prompt, user_input=prompt)
            summary = extract_llm_response(summary, "blog_post")
            summaries.append(summary)
        # Write summaries to the output file
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for i, summary in enumerate(summaries):
                out_file.write(summary)
        print(f"Summaries have been saved to {output_file}")
    except Exception as e:
        print(f"Error in summarize_file: {e}")


if __name__ == "__main__":

    file_name = "the_power_of_introvert"
    content = f"/Users/danny/Documents/repos/posts/aicrafterzheng.github.io/docs/posts/podcasts/transcripts/{file_name}.txt"
    file_name = f"{file_name}1.md"
    output_file = f"/Users/danny/Documents/repos/posts/aicrafterzheng.github.io/docs/posts/podcasts/{file_name}"
    # llm_client = LLMClient(llm_provider=LLMProvider.AZURE_OPENAI_GPT_4o)
    llm_client = LLMClient(llm_provider=LLMProvider.AZURE_OPENAI_GPT_41)
    highlights = ""
    transcript = ""
    with open(content, 'r', encoding='utf-8') as file:
        file_content = file.read()
        [highlights, transcript] = file_content.split("danny_cut")
    # summarize_file(llm_client, transcript, output_file, chunking=chunking)
    prompt = podcast_user_prompt.format( HIGHLIGHTS=highlights, TRANSCRIPT=transcript)

    summarizer = SimpleSummarizer(llm_client, "", prompt)
    summarizer.summarize_content(output_file=output_file)
  