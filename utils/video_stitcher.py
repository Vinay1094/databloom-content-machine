import os
import subprocess


def stitch_videos_and_audio(video_folder, audio_path, output_path):
    """
    Concatenates all MP4 files in a folder and overlays a master audio track.
    Uses FFmpeg concat demuxer for fast, lossless video joining.
    """
    clips = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    clips.sort()

    if not clips:
        print("No video clips found to stitch.")
        return

    print(f"Found {len(clips)} clips to stitch.")

    list_file_path = os.path.join(video_folder, "concat_list.txt")
    with open(list_file_path, 'w') as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    command = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    print("Stitching final video with FFmpeg...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    os.remove(list_file_path)
    print(f"Final video rendered at: {output_path}")
