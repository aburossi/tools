import os
from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
    video_clip = VideoFileClip(mp4_file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3_file_path)
    audio_clip.close()
    video_clip.close()

def main():
    mp4_file_path = input("Bitte geben Sie den Pfad zur MP4-Datei ein: ")
    if not os.path.isfile(mp4_file_path):
        print("Datei nicht gefunden. Bitte überprüfen Sie den Pfad und versuchen Sie es erneut.")
        return

    mp3_file_path = input("Bitte geben Sie den Pfad für die zu erstellende MP3-Datei ein: ")
    convert_mp4_to_mp3(mp4_file_path, mp3_file_path)
    print("Konvertierung abgeschlossen.")

if __name__ == "__main__":
    main()