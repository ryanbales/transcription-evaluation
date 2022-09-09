import argparse
import os
import utils
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audio_file', help='url to file or local audio filename')
    parser.add_argument('--local', action='store_true', help='must be set if audio_file is local')
    parser.add_argument('--api_key', action='store', help='<YOUR-API-KEY>')

    args = parser.parse_args()

    if args.api_key is None:
        args.api_key = os.getenv("AAI_API_KEY")
        if args.api_key is None:
            raise RuntimeError("AAI_API_KEY environment variable not set.  \
                Try setting it now, or passing in your  \
                API key as a command line argument with `--api_key`.")

    # Create header with authorization along with content-type
    header = {
        'authorization': args.api_key,
        'content-type': 'application/json'
    }

    if args.local:
        # Upload the audio file to AssemblyAI
        upload_url = utils.upload_file(args.audio_file, header)
    else:
        upload_url = {'upload_url': args.audio_file}

    # Request a transcription
    transcript_response = utils.request_transcript(upload_url, header)

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utils.make_polling_endpoint(transcript_response)

    # Wait until the transcription is complete
    utils.wait_for_completion(polling_endpoint, header)

    # Request the raw transcript
    trascript = utils.get_transcript(polling_endpoint, header)

    # Save transcript results
    with open("data/output/assemblyai_results.json", "w") as transcript_output_file:
        json.dump(trascript, transcript_output_file, indent=4)

    # Print transcript results
    print(json.dumps(trascript, indent=4))
    print("Transcription processing complete!")

    return


if __name__ == '__main__':
    main()
