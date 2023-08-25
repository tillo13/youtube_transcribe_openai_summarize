#2023-Aug-25 
#testing github copilot on a use case: https://en.wikipedia.org/wiki/GitHub_Copilot
#using https://pypi.org/project/youtube-transcript-api/
#filename: ingest_youtube.py
#github https://github.com/tillo13/youtube_transcribe_openai_summarize


from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from urllib.parse import urlparse, parse_qs

#enter a url of the youtube video you want to transcribe 
URL_OF_YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=iK4u95thQn0" # has transcripts
URL_OF_YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=51TpMIEyUxk" ##no transcripts test

def get_video_id(video_url):
    parsed_url = urlparse(video_url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    return None

def get_transcript_and_metadata(video_url, language_codes=['en']):
    video_id = get_video_id(video_url)

    if video_id is None:
        raise Exception(f"Could not parse video URL: {video_url}")

    try:
        transcripts = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        print(f"Transcription is disabled for the video: {video_url}")
        print("Please choose another video where transcription is enabled.")
        return None, None

    transcribed_text = " ".join([caption['text'] for caption in transcripts])

    # Getting the list of all available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    for transcript in transcript_list:
        is_generated = transcript.is_generated
        is_translatable = transcript.is_translatable

    translatable_to_spanish = "es" in [lang['language_code'] for lang in transcript_list.find_transcript(language_codes).translation_languages]
    translatable_to_japanese = "ja" in [lang['language_code'] for lang in transcript_list.find_transcript(language_codes).translation_languages]

    metadata = {
            'video_id': video_id,
            'language': transcript_list.find_transcript(language_codes).language,
            'language_code': transcript_list.find_transcript(language_codes).language_code,
            'is_generated': is_generated,
            'is_translatable': is_translatable,
            'translatable_to_spanish': translatable_to_spanish,
            'translatable_to_japanese': translatable_to_japanese
        }

    return transcribed_text, metadata

if __name__ == "__main__":
    transcribed_text, metadata = get_transcript_and_metadata(URL_OF_YOUTUBE_VIDEO)

    print("Original Text:")
    print(transcribed_text)

    print("\nMetadata:")
    print(metadata)