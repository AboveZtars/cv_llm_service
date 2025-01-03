## Rafa's portfolio backend.

An API that uses FastApi as it main tool.

##Routes

- /
  This route is used to start the server and verify the status of it, the frontend should call it when someone loads the main page of the Rafa's portfolio website and it should return Hello world with a 200 status code. If the response is different then the frontend waits for the backend to be ready.
- /openai
  This route calls the openai api to generate a response to the user.
