from pydub import AudioSegment
from pydub.utils import make_chunks
import requests
import subprocess
import os
from lxml import etree
import speech_recognition as sr
import audio2text_converter
import pocketsphinx
import info



def download_video(url):
    video_file_name = info.get_video_name(url)
    with open(video_file_name, "wb") as f:
        f.write(requests.get(url=info.get_video_url(url), stream=True).content)



def video_to_audio(url):
    download_video(url)
    video_name = info.get_video_name(url)
    audio_name = info.get_audio_name(url)
    input = video_name
    output = audio_name
    #call thread with os package
    cmd_go_to_project_directory = os.getcwd()
    #call a subprocess
    subprocess.call(cmd_go_to_project_directory, shell=True)
    cmd = "ffmpeg -i " + input + " " + output
    subprocess.check_output(cmd, shell=True)

    return output


def audio_to_text(audio_file_name):
    # get the original audio
    myaudio = AudioSegment.from_file(audio_file_name, "wav")

    #define the length of each audio chunk as 1000ms
    chunk_length_ms = 10000
    #cut the original audio into chunks and save it to variable chunks
    chunks = make_chunks(myaudio, chunk_length_ms)
    #calculator string result
    result = ""
    # for each audio chunk, convert audio to text
    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        print
        "exporting", chunk_name
        chunk.export(chunk_name, format="wav")
        result += audio2text_converter.convert_audio(chunk_name)
    return result


def run():
    url = 'http://video.eastday.com/a/170602114054589846059.html?indexlbt'
    text = audio_to_text(video_to_audio(url))

    with open("weather.txt", "w") as result:
        result.write(text)

run()


