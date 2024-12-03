from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp as youtube_dl
import os

app = Flask(__name__)

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle download requests
@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['type']

    try:
        # Set the download directory (local folder on the server)
        download_folder = os.path.join(os.getcwd(), 'downloads')  # Ensure the path is absolute
        
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Set download options based on audio or video
        ydl_opts = {
            'format': 'bestaudio/best' if download_type == 'audio' else 'best',  # Select best audio/video
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save with video title
        }

        # Download using yt-dlp
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # After downloading, send the file to the user as an attachment
        return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8200)
