#1.2.1

import subprocess, platform, requests, sys, zipfile, os, git, shutil

def updates(dlp, menu_choice):
    #Updating the program from github
    shutil.copy2("yt-mp3.py", ".yt-mp3.previous.py")
    try:
        repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))
        origin = repo.remotes.origin
        origin.fetch()
        repo.git.checkout('origin/main', '--', 'yt-mp3.py')
        print("Script updated. Please re-run.")
        sys.exit(0)
    except git.InvalidGitRepositoryError:
        print("Not a git repo, skipping update.")
    except Exception as e:
        print(f"Update failed: {e}")

    os.makedirs(".config", exist_ok=True)
    if menu_choice == "1":   
        os.makedirs("yt-dlp", exist_ok=True)
        url = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                with open(".config/DLP_VERSION", "r") as f:
                    version = f.read()
            except FileNotFoundError:
                version = "0.0"  # First run or something 
            latest_release = response.json()
            tag_name = latest_release["tag_name"]
            if platform.system() == "Linux":
                download_url = f"https://github.com/yt-dlp/yt-dlp/releases/download/{tag_name}/yt-dlp_linux"
            elif platform.system() == "Windows":
                download_url = f"https://github.com/yt-dlp/yt-dlp/releases/download/{tag_name}/yt-dlp.exe"

            if version.strip() != tag_name.strip() or "-d" in sys.argv:
                try:
                    response = requests.get(download_url, stream=True)
                    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                    with open(dlp, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"yt-dlp version updated to {tag_name}")
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading file: {e}")
                with open(".config/DLP_VERSION", "w") as f:
                    f.write(tag_name)
                if platform.system() == "Linux":
                    subprocess.run(["chmod", "+x", dlp])
        else:
            print("Unable to contact update server")


    url = "https://api.github.com/repos/yt-dlp/FFmpeg-Builds/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            with open(".config/FFMPEG_VERSION", "r") as f:
                version = f.read()
        except FileNotFoundError:
            version = "0.0"  # First run or something 
        latest_release = response.json()
        tag_name = latest_release["tag_name"]
        download_url = f"https://github.com/yt-dlp/FFmpeg-Builds/releases/download/{tag_name}/ffmpeg-master-latest-win64-gpl.zip"

        if version.strip() != tag_name.strip() or "-f" in sys.argv:
            try:
                response = requests.get(download_url, stream=True)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                with open("ffmpeg.zip", "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Downloaded")
                with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
                    zip_ref.extractall()
                os.remove("ffmpeg.zip")
                print("Extracted")
                print(f"ffmpeg version updated to {tag_name}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
            with open(".config/FFMPEG_VERSION", "w") as f:
                f.write(tag_name)
    else:
        print("Unable to contact update server")
    


def download_youtube(dlp):
    url = input("Enter the YouTube video URL: ")
    print("Formats:  mp3 aac mp4 mkv wav ogg webm")
    format = input("Select format: ").strip().lower()

    if format not in ["mp3", "aac", "mp4", "mkv", "3gp", "flv", "ogg", "wav", "webm"]:
        print("Invalid choice. Please enter a format.")
        return
    #temp fix for SABR stuff
    if format == "mp4":
        if platform.system() == "Windows":
            subprocess.run([dlp, "--recode-video", format.strip(), url, "--ffmpeg-location", "ffmpeg-master-latest-win64-gpl/bin", "-P", "videos"])
        elif platform.system() == "Linux":
            subprocess.run([dlp, "--recode-video", format.strip(), url, "-P", "videos"])
    else:
        if platform.system() == "Windows":
            subprocess.run([dlp, "-t", format.strip(), url, "--ffmpeg-location", "ffmpeg-master-latest-win64-gpl/bin", "-P", "videos"])
        elif platform.system() == "Linux":
            subprocess.run([dlp, "-t", format.strip(), url, "-P", "videos"])

def convert():
    in_file = input("Input File:  ").replace('"', "").replace("'", "")
    print("Formats:  mp3 aac mp4 mkv wav ogg webm.")
    dest_format = input("Converted Format:  ").lower().strip()
    file_name = in_file.rsplit('.', 1)[0]
    extension = in_file.split(".")[-1]
    os.rename(in_file, f"ytmp3temp.{extension}")
    if platform.system() == "Windows":
        subprocess.run(["ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe", "-i", f"ytmp3temp.{extension}", f"{file_name}.{dest_format}"])
    elif platform.system() == "Linux":
        subprocess.run(["ffmpeg", "-i", f"ytmp3temp.{extension}", f"{file_name}.{dest_format}"])
    os.rename(f"ytmp3temp.{extension}", in_file)

if __name__ == "__main__":
    if platform.system() == "Windows":
        dlp = "yt-dlp/yt-dlp.exe"
    elif platform.system() == "Linux":
        dlp = "yt-dlp/yt-dlp_linux"
    else:
        raise Exception
    menu_choice = input("(1) Download YT\n(2) Convert Format\nOption:  ").strip()
    if menu_choice not in ["1", "2"]:
        print("Please choose a valid option.")
        exit()
   

    updates(dlp, menu_choice)
    if menu_choice == "1":
        download_youtube(dlp)
    elif menu_choice == "2":
        convert()
        