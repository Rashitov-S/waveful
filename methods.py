import mutagen


def get_track_length(file_path):
    file = mutagen.File(f"resources\\{file_path}")
    seconds = round(file.info.length)
    duration = f"{seconds // 60}:{seconds % 60:02d}"
    return duration
