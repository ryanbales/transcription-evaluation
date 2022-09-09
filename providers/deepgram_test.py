from deepgram import Deepgram
import asyncio
import json

# API Configuration
DEEPGRAM_API_KEY = "<api key here>"

# Replace with your file path and audio mimetype
PATH_TO_FILE = "data/input/shopping_example.wav"
MIMETYPE = "audio/wav"


async def main():
    # Initializes the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    with open(PATH_TO_FILE, "rb") as audio:
        source = {"buffer": audio, "mimetype": MIMETYPE}
        options = {
            "model": "general",
            "language": "en",
            "tier": "enhanced",
            "punctuate": True,
            "multichannel": True
        }

        print("Requesting transcript...")
        print("Your file may take up to a couple minutes to process.")

        response = await dg_client.transcription.prerecorded(source, options)        
        with open("data/output/deepgram_results.json", "w") as transcript_output_file:
            json.dump(response, transcript_output_file, indent=4)

        print(json.dumps(response, indent=4))
        print("Transcription processing complete!")

asyncio.run(main())
