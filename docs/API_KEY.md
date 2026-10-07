# The API key: what it is and how to set it up

This project uses the Google Gemini API to talk to an LLM. To use it you need an API key. This page explains what the key is, how to create it for free, how to check the limits, and how to keep it safe.

## What an API key is

The LLM does not run on your computer. It runs on Google's computers. The Python code sends a prompt over the internet, and Google sends the answer back.

Google needs to know who is asking, so it can:

- count the requests against your free limit;
- stop other people from using the service in your name.

The API key is that identification. It works like a library card: the code shows it with every request. Without a key, the request is refused.

## How to create a free key

1. Go to [Google AI Studio](https://aistudio.google.com/api-keys) and log in with a Google account.
2. Click the button to create an API key.
3. Give the key a name, for example `easy-leaflet`.
4. Choose a project. If the list says "No Cloud Projects Available", create a new project (any name). A project is only a folder on Google's side, and it is free.
5. Click "Create key" and copy the key.

No credit card is needed. If a screen asks for billing or a payment card, stop: you do not need it for this project.

## How to give the key to the project

1. In the project root, copy the file `.env.example` and name the copy `.env`.
2. Open `.env` and paste your key:

   ```
   GEMINI_API_KEY=paste-your-key-here
   ```

3. Check that Git ignores the file:

   ```
   git status
   ```

   `.env` must not appear in the list.

The code reads this file with the `python-dotenv` library, so the key is never written inside the Python code.

| File | Goes to GitHub? | What is inside |
|---|---|---|
| `.env` | No (it is in `.gitignore`) | Your real key |
| `.env.example` | Yes | Only the name of the variable, with no real key |

## The free limits

The free tier has limits. There are three types:

| Short name | Meaning | Example of what it limits |
|---|---|---|
| RPM | Requests per minute | How fast you can send questions |
| RPD | Requests per day | How many questions in one day |
| TPM | Tokens per minute | How much text you can send in one minute |

A token is a small piece of a word. In Portuguese, 1000 characters is about 250 to 300 tokens.

### Where to see your limits

The numbers are different for each model and Google changes them over time, so this page does not list them. To see the current numbers for your account:

1. Open [Google AI Studio](https://aistudio.google.com).
2. In the left menu, open **Dashboard**.
3. Look for the pages about **usage** and **rate limits**. They show the limit of each model and how much you have used.

On the API keys page, each key also shows its plan. It should say it is on the free tier.

### What happens when you reach a limit

The request fails with an error number **429** (the text usually says "quota" or "resource exhausted"). Nothing is charged. What to do:

- If it is the per-minute limit: wait one minute and try again.
- If it is the per-day limit: wait until the next day, or use a smaller model.

### Is the free tier enough for this project?

This project is small:

- Each question is one request, with about 4 chunks of text (around 1500 tokens).
- The evaluation uses a test set of about 30 questions, so one full run is about 30 requests.
- The search step (embeddings) runs on your own computer and does not use the API at all.

To stay inside the limits, the evaluation script should wait a few seconds between questions.

## Safety rules

1. **Never commit `.env`.** Always look at `git status` before `git add`.
2. **Never paste the key** in the code, in the README, in a screenshot, or in a chat.
3. **Never turn on billing** for this project. Without billing, the worst case is an error message, not a bill.
4. **If the key was seen by someone**, delete it on the API keys page and create a new one. Only the line in `.env` changes.
5. **When the project is finished for good**, delete the key. While you still use the project (for example to show the demo), keep it.

## Common problems

| Problem | Likely reason | Fix |
|---|---|---|
| Error about a missing API key | `.env` does not exist, is in the wrong folder, or the name is not `GEMINI_API_KEY` | Check the file is in the project root and the name is exact |
| Error 429 | A free limit was reached | Wait and try again (see above) |
| Error saying the model was not found | The model name changed | Check the current model names in AI Studio and change the name in `llm.py` |
| `.env` appears in `git status` | `.gitignore` does not have `.env` | Add a line `.env` to `.gitignore` before any commit |
