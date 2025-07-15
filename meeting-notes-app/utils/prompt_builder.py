def build_prompt(transcript: str) -> str:
    return f"""
You are an assistant that extracts structured notes and tasks from meeting transcripts.

Based on the following transcript, provide:

1. A short summary
2. Key discussion points
3. Action items with assignees and deadlines (if mentioned)
4. Any open questions or follow-ups

Transcript:
\"\"\"
{transcript}
\"\"\"
"""
