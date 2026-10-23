# AI Question & Answering System

A Streamlit chat application that answers questions and follow-ups using the official Google Gen AI Python SDK. Conversation history is kept in the current Streamlit session.

## Features

- Chat-style interface with separate user and assistant messages
- Multi-turn conversation history and a clear-conversation control
- Configurable Gemini model and response temperature
- Friendly handling for missing configuration and API failures
- Unit tests that mock the Gemini client and do not make network requests

## Architecture

The Streamlit entry point is in `app/main.py`. Settings are validated in `app/config/settings.py`; all Gemini API calls are contained in `app/services/gemini_service.py`; assistant instructions are maintained in `app/prompts/qa_prompt.py`; and standard-library logging is configured in `app/utils/logging_config.py`.

## Project Structure

```text
question_answering_app/
├── app/
│   ├── config/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.sh
```

## Prerequisites

- Python 3.10 or newer
- A Gemini API key with access to the configured model
- `pip`

## Setup

From the `question_answering_app` directory, create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux activation:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and edit `.env` with your key and preferred settings.

Windows PowerShell:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

macOS/Linux:

```bash
cp .env.example .env
```

The configuration variables are:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
TEMPERATURE=0.2
```

Add your Gemini API key from Google AI Studio to `GEMINI_API_KEY` in `.env`. If `.env` already exists, add the Gemini variables without replacing the file or its other values. The application does not modify `.env`. Never commit `.env` or share its contents. The API key is not displayed by the application or included in application logs.

## Run the Application

Start from the `question_answering_app` directory after activating the virtual environment:

```bash
streamlit run app/main.py
```

Alternatively, on macOS/Linux run `./run.sh`. Streamlit prints the local URL in the terminal. To stop the server, press `Ctrl+C` in that terminal.

## Run Tests

```bash
python -m pytest
```

The tests use a mocked Gemini client and need no real API key.

## Example Questions

- What is the difference between weather and climate?
- Explain how a Python dictionary works, with a short example.
- Can you summarize the previous answer in one sentence?

## Troubleshooting

- **Missing API key:** Copy `.env.example` to `.env` and set `GEMINI_API_KEY`. If `.env` already exists, add this variable without replacing its other values. Restart Streamlit after changing environment configuration.
- **Authentication or access error:** Check that the key is a Gemini API key and the account can use the selected model. The UI intentionally shows a generic API failure message.
- **Model error:** Set `GEMINI_MODEL` to a model available to your account.
- **Temperature error:** `TEMPERATURE` must be numeric and between `0` and `2`.
- **Streamlit command not found:** Activate the virtual environment and install `requirements.txt` again.

## Security Considerations

- Keep `.env` out of version control and use `.env.example` only for placeholders.
- Do not paste API keys into source code, issue reports, or logs.
- The application logs event/error types but does not log user messages or provider exception details.
- Conversation history remains in Streamlit session state; do not deploy this application with sensitive data unless your data handling, access controls, and retention requirements have been reviewed.
- For production, use a managed secret store, authenticated access, rate limiting, and appropriate monitoring.

## Deactivate the Virtual Environment

On Windows, macOS, or Linux:

```bash
deactivate
```

## Future Enhancements

- Add authentication and per-user conversation persistence
- Add configurable system prompts and model selection in the interface
- Add deployment health checks, rate limiting, and usage tracking
- Add broader tests for Streamlit interaction and provider error categories