# AI Gen Projects — YouTube

Hands-on Generative AI practicals built for YouTube tutorials.

## Practicals

1. **001 Basic Text Generation** — generate multiple types of text with the OpenAI Responses API.
2. **002 Zero-Shot Prompting** — perform classification without examples.
3. **003 One-Shot Prompting** — perform classification with one example.
4. **004 Few-Shot Prompting** — perform classification with multiple examples.
5. **005 Role-Based Prompting** — give the model a role and task.

## Setup

### Windows CMD

From the repository root:

```cmd
python -m venv venv
venv\Scripts\activate
pip install openai
set OPENAI_API_KEY=YOUR_API_KEY_HERE
echo %OPENAI_API_KEY%
```

Do not commit API keys to GitHub.

### Run

```cmd
python 001-basic-text-generation\first.py
python 002-zero-shot-prompting\zero_shot.py
python 003-one-shot-prompting\one_shot.py
python 004-few-shot-prompting\few_shot.py
python 005-role-based-prompting\role_based.py
```

## Git workflow used in the videos

```cmd
git add .
git commit -m "Add AI Gen practicals"
git push origin main
```
