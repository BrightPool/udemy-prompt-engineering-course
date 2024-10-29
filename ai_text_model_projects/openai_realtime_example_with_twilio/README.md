# Speech Assistant with Twilio Voice and the OpenAI Realtime API (Python)

This application demonstrates how to use Python, [Twilio Voice](https://www.twilio.com/docs/voice) and [Media Streams](https://www.twilio.com/docs/voice/media-streams), and [OpenAI's Realtime API](https://platform.openai.com/docs/) to make a phone call to speak with an AI Assistant.

The application opens websockets with the OpenAI Realtime API and Twilio, and sends voice audio from one to the other to enable a two-way conversation.

See [here](https://www.twilio.com/en-us/blog/voice-ai-assistant-openai-realtime-api-python) for a tutorial overview of the code.

This application uses the following Twilio products in conjuction with OpenAI's Realtime API:

- Voice (and TwiML, Media Streams)
- Phone Numbers

## Prerequisites

To use the app, you will need:

- **Python 3.9+** We used \`3.9.13\` for development; download from [here](https://www.python.org/downloads/).
- **A Twilio account.** You can sign up for a free trial [here](https://www.twilio.com/try-twilio).
- **A Twilio number with _Voice_ capabilities.** [Here are instructions](https://help.twilio.com/articles/223135247-How-to-Search-for-and-Buy-a-Twilio-Phone-Number-from-Console) to purchase a phone number.
- **An OpenAI account and an OpenAI API Key.** You can sign up [here](https://platform.openai.com/).
  - **OpenAI Realtime API access.**

## Local Setup

There are 4 required steps and 1 optional step to get the app up-and-running locally for development and testing:

1. Run ngrok or another tunneling solution to expose your local server to the internet for testing. Download ngrok [here](https://ngrok.com/).
2. (optional) Create and use a virtual environment
3. Install the packages
4. Twilio setup
5. Update the .env file

### Open an ngrok tunnel

When developing & testing locally, you'll need to open a tunnel to forward requests to your local development server. These instructions use ngrok.

Open a Terminal and run:

```
ngrok http 5050
```

Once the tunnel has been opened, copy the `Forwarding` URL. It will look something like: `https://[your-ngrok-subdomain].ngrok.app`. You will
need this when configuring your Twilio number setup.

Note that the `ngrok` command above forwards to a development server running on port `5050`, which is the default port configured in this application. If
you override the `PORT` defined in `index.js`, you will need to update the `ngrok` command accordingly.

Keep in mind that each time you run the `ngrok http` command, a new URL will be created, and you'll need to update it everywhere it is referenced below.

### (Optional) Create and use a virtual environment

To reduce cluttering your global Python environment on your machine, you can create a virtual environment. On your command line, enter:

```
python3 -m venv env
source env/bin/activate
```

### Install required packages

In the terminal (with the virtual environment, if you set it up) run:

```
pip install -r requirements.txt
```

### Twilio setup

#### Point a Phone Number to your ngrok URL

In the [Twilio Console](https://console.twilio.com/), go to **Phone Numbers** > **Manage** > **Active Numbers** and click on the additional phone number you purchased for this app in the **Prerequisites**.

In your Phone Number configuration settings, update the first **A call comes in** dropdown to **Webhook**, and paste your ngrok forwarding URL (referenced above), followed by `/incoming-call`. For example, `https://[your-ngrok-subdomain].ngrok.app/incoming-call`. Then, click **Save configuration**.

### Update the .env file

Create a `/env` file, or copy the `.env.example` file to `.env`:

```
cp .env.example .env
```

In the .env file, update the `OPENAI_API_KEY` to your OpenAI API key from the **Prerequisites**.

## Run the app

Once ngrok is running, dependencies are installed, Twilio is configured properly, and the `.env` is set up, run the dev server with the following command:

```
python main.py
```

## Test the app

With the development server running, call the phone number you purchased in the **Prerequisites**. After the introduction, you should be able to talk to the AI Assistant. Have fun!

## Special features

### Have the AI speak first

To have the AI voice assistant talk before the user, uncomment the line `# await send_initial_conversation_item(openai_ws)`. The initial greeting is controlled in `async def send_initial_conversation_item(openai_ws)`.

### Interrupt handling/AI preemption

When the user speaks and OpenAI sends `input_audio_buffer.speech_started`, the code will clear the Twilio Media Streams buffer and send OpenAI `conversation.item.truncate`.

Depending on your application's needs, you may want to use the [`input_audio_buffer.speech_stopped`](https://platform.openai.com/docs/api-reference/realtime-server-events/input-audio-buffer-speech-stopped) event, instead, os a combination of the two.
