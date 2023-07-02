# vdroid - Movie and Book Summary Generator

This is a IA Python application designed to generate video summaries of movies or books from their titles. It uses chatGPT for text generation, Azure Speech for narrative voice generation, and Bing for image search.

<p align="center">
  <img src="https://github.com/ricardoborges/vdroid/assets/404572/e5811317-2744-41ba-8d8b-075c80a99541" width="500">
</p>

## Prerequisites

This application requires Python 3.8 or later, and the following API keys:

- Azure Speech API
- Bing Image Search API
- GPT API

Additionally, you'll need to install certain Python libraries. You can install all the required dependencies by running the following command:

pip install -r requirements.txt

## API KEYS

You should setup enviroment variables for the api keys: 

- OPENAI_API_KEY=
- BING_API_KEY=
- AZURE_SPEECH_KEY=
- SERVICE_REGION_NAME=

## Usage

This application can be run either in single or batch mode. In single mode, it generates a summary for one movie or book. In batch mode, it processes a list of movies or books provided in the configuration files `movie.config` and `book.config` respectively.

Use the following commands to run the application:

**For movies:**

python main.py movie

**For batch processing of movies:**

python main.py movie --batch

**For books:**
python main.py book

**For batch processing of books:**
python main.py book --batch

In the `movie.config` and `book.config` files, each title should be in the following format:

[
{
"title": "Title here", // The title of the movie
"english": "True|False", // The language of the generated summary
"short": "True|False" // if short the bing search will prioritize vertical images
},
...
]

Example:
[
{ "title": "Back to the Future", "english":"True", "short":"False" }
]

## Features

Here are the main features of the application:

- Work in progress for books
- Creates a text summary of a movie or a book using GPT.
- Uses Azure Speech to generate a narrative voice for the summary.
- Searches Bing for images related to the movie or book.

## TODO 

- Create voice provider using eleven labs
- Create dall-e image generation option
- Create google image search option

## Contributing

Contributions are always welcome! If you have any suggestions for improvement, please open an issue or create a pull request.

## License

[MIT](https://choosealicense.com/licenses/mit/)
