from youtube_transcript_api import YouTubeTranscriptApi
# Define the URL of the YouTube video you want to summarize
URL_OF_YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=BtpDojXVSO8"

def get_transcript(video_url):
    video_id = video_url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([i['text'] for i in transcript])

if __name__ == "__main__":
    transcribed_text = get_transcript(URL_OF_YOUTUBE_VIDEO)

    print("Original Text:")
    print(transcribed_text)
