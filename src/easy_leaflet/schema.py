from pydantic import BaseModel


# The exact format we expect from the LLM
class LLMOutput(BaseModel):
    found: bool # was the answer in the leaflet?
    answer: str # the text for the user
    excerpts: list[int] # numbers of the excerpts used, for example [1, 3]


def parse_llm_output(raw_text):
    # LLMs often put the JSON inside (json ...), so we remove that first
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]

    # Check the JSON and turn it into an LLMOutput.
    # If something is wrong, Pydantic raises a ValidationError.
    return LLMOutput.model_validate_json(text)