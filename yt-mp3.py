#1.0

import subprocess, platform, requests, sys

def updates(dlp):
    url = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            with open(".DLP_VERSION", "r") as f:
                version = f.read()
        except FileNotFoundError:
            version = "0.0"  # First run or something 
        latest_release = response.json()
        tag_name = latest_release["tag_name"]
        if platform.system() == "Linux":
            download_url = f"https://github.com/yt-dlp/yt-dlp/releases/download/{tag_name}/yt-dlp_linux"
        elif platform.system() == "Windows":
            download_url = f"https://github.com/yt-dlp/yt-dlp/releases/download/{tag_name}/yt-dlp.exe"

        if version.strip() != tag_name.strip() or "-f" in sys.argv:
            try:
                response = requests.get(download_url, stream=True)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                with open(dlp, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"yt-dlp version updated to {tag_name}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
            with open(".DLP_VERSION", "w") as f:
                f.write(tag_name)
            if platform.system() == "Linux":
                subprocess.run(["chmod", "+x", dlp])
    else:
        print("Unable to contact update server")


def download_youtube(dlp):
    url = input("Enter the YouTube video URL: ")
    print("Formats:  mp3 aac mp4 mkv")
    format = input("Select format: ").strip().lower()

    if format not in ["mp3", "aac", "mp4", "mkv"]:
        print("Invalid choice. Please enter a format.")
        return
    subprocess.run([dlp, "-t", format.strip(), url])

if __name__ == "__main__":
    if platform.system() == "Windows":
        dlp = "yt-dlp.exe"
    elif platform.system() == "Linux":
        dlp = "./yt-dlp_linux"
    else:
        raise Exception
    updates(dlp)
    download_youtube(dlp)
