# Lazy Logistics Hack-day write up

This is a small application built using GCP resources to assess the suppliers of
a given company.



## Methodology

I asked ChatGPT to design a tool to return lists of suppliers for a given
company name. I then asked it to create a Cursor prompt to generate this tool as
a client-server application. I specified the use of GenAI tooling and GCP
resources.

[Link to chat](https://chatgpt.com/c/68556033-1d08-8000-bcee-19f0f82b7c1b)

I used this prompt for the initial setup, following instructions to create GCP
resources when prompted. Most required resources could be created automatically
once authorization had been provided to the GCP CLI.

After repeated failures to start the service using real authentication, Cursor
created a mock interface. As this was unsuitable for the POC I planned to demo,
I created a new chat context to resolve the auth issue only.

Full Cursor chat logs are available in the [/chatlogs](/chatlogs) folder.



## WARNINGS

Cursor can and will create real resources; please include guards in your prompt
to request user interaction before-hand. I would strongly recommend only
allowing read-only access to infrastructure, then asking Cursor to generate
commands or instructions to create the necessary pieces. Otherwise you risk a
significant bill for runaway resource creation.



## Learnings

It is possible to export chats!


Cursor was unable to correctly identify which language models were available to
me; I suspect this could be resolved with the correct tool call invocation, but
I found it quicker to just find the correct values myself.


My interactions with the chat became more terse over time, dropping down to
single-word and single-letter responses. These were correctly interpreted
despite spelling mistakes and broken English.



## Future work

Further investigation into the quality of results would help. Currently this is
using a regular web search; creating some bounds could improve the relevance of
returned results.

Sometimes we get more results back than we asked for. I have seen 4 results
returned when setting max_results to 3. As I followed a vibe-coding methodology,
I have no idea why.

Resource management for infrastructure is entirely manual. Resources would
ideally be managed using an IaC utility (`terraform` for preference).

We have not assessed the scalability or cost of this solution.



## Links

- [GCP Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
- [GCP Custom Search](https://developers.google.com/custom-search/v1/overview)
- [Programmable Search](https://programmablesearchengine.google.com/controlpanel/create/congrats?cx=17adeb8623fe5477a)
- [Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)
