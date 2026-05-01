import yt_dlp

with yt_dlp.YoutubeDL({'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav', 'preferredquality': '192'}]}) as ydl:
    ydl.download(['https://www.youtube.com/shorts/dFGHrYjRd7U'])