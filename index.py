from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
import io,uuid, base64, os, pathlib, requests, praw, subprocess
from flask import Flask, render_template, request, jsonify, Response, send_file
from werkzeug.utils import secure_filename

# subprocess.Popen("curl https://gitlab.com/rishabh-modi2/public/-/raw/main/rclone -o rclone && chmod 777 rclone && curl https://paste.ee/r/DGbgR/0 -o rclone.conf", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))

def uploadFile(file_name, mime):
    file_metadata = {
    'name': file_name,
    'mimeType': mime,
    "parents": ['1PJWwfFeggwFI5ZNq2U3tS3IbUf5OsJfE']}
    media = MediaFileUpload(file_name,
                            mimetype=mime,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
    return file.get('id')

def OnedriveUpload(file_name):
    subprocess.Popen("./rclone copy " + file_name + " onedrive:public && rm " + file_name, shell=True)
    String = 'https://vid.rishabh.ml/api/raw/?path=/' + file_name
    String_bytes = String.encode("ascii")
    base64_bytes = base64.b64encode(String_bytes)
    base64_string = base64_bytes.decode("ascii")
    return f"{base64_string}"


image = {'.jpg', '.jpeg', '.png'}
video = {'.mp4', '.mkv'}
audio = {'.mp3', '.ogg'}
reddit = praw.Reddit(client_id="N1XSqyabH50pQN5_uL96tA", client_secret="OU0vNPkAiua6EQbj6P-9bREG7FmMiA", user_agent="ris", username="shashi_tharooor_1", password="rishabh2003",)

def RedditVideoUpload(file):
    submission = reddit.subreddit("test").submit_video('title', file)
    String1 = submission.url
    String = String1.replace("https://v.redd.it/", "")
    String_bytes = String.encode("ascii")
    base64_bytes = base64.b64encode(String_bytes)
    base64_string = base64_bytes.decode("ascii")
    return f"{base64_string}"

def RedditApiLogin():
    auth = requests.auth.HTTPBasicAuth('N1XSqyabH50pQN5_uL96tA', 'OU0vNPkAiua6EQbj6P-9bREG7FmMiA')
    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password', 'username': 'shashi_tharooor_1', 'password': 'rishabh2003'}
    headers = {'User-Agent': 'ris'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

def RedditApiUpload():
    data = {'kind': 'video', 'title': 'shashi_tharooor_1', 'sr': 'u_shashi_tharooor_1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

def UpdateGist():
    token='API_TOKEN'
    filename="YOUR_UPDATED_JSON_FILE.json"
    gist_id="GIST_ID"

    content=open(filename, 'r').read()
    headers = {'Authorization': f'token {token}'}
    r = requests.patch('https://api.github.com/gists/' + gist_id, data=json.dumps({'files':{filename:{"content":content}}}),headers=headers) 
    print(r.json())

def file(filetype, f):
    filename = str(uuid.uuid4()) + filetype
    # with open('logs.txt', 'a+') as fa:
    #     fa.write(request.headers.get('X-Forwarded-For', request.remote_addr) + ' uploaded ' + filename)
    #     fa.close()
    if filetype == 'nigga':
        print('nigga')
    
    # elif filetype in video:
    #     f.save(filename)
    #     sample_string = uploadFile(filename, 'video/mp4')
    #     sample_string_bytes = sample_string.encode("ascii")
    #     base64_bytes = base64.b64encode(sample_string_bytes)
    #     base64_string = base64_bytes.decode("ascii")
    #     print('file Video')
    #     os.remove(filename)
    #     # f"{base64_string}"
    #     resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/stream/?url=" + f"{base64_string}" + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
    #     return resp
    elif filetype in video:
    #   try:
        f.save(filename)
        resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer2.rishabh.ml/onestream/?id=" + OnedriveUpload(filename) + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        # os.remove(filename)
        # f"{base64_string}"
        # resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer2.rishabh.ml/rvideo1/?id=" + "sample_string" + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        return resp
    #   except Exception as e:
    #         print(e)
    #         f.save(filename)
    #         sample_string = uploadFile(filename, 'video/mp4')
    #         sample_string_bytes = sample_string.encode("ascii")
    #         base64_bytes = base64.b64encode(sample_string_bytes)
    #         base64_string = base64_bytes.decode("ascii")
    #         print('file Video')
    #         os.remove(filename)
    #         # f"{base64_string}"
    #         resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/stream/?url=" + f"{base64_string}" + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
    #         return resp
    #         pass

    elif filetype in image:
        f.save(filename)
        uploadFile(filename, 'image/jpg')
        os.remove(filename)
        resp = "<img src='https://backend.rishabh.ml/1:/" + filename + "'>"
        return resp

    elif filetype in audio:
        f.save(filename)
        uploadFile(filename, 'audio/mpeg')
        os.remove(filename)
        resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/audio/?url=https://backend.rishabh.ml/1:/" + filename + "&load=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        return resp

      #import werkzeug
app = Flask(__name__)

# def filesend(filetype):
#     filename = str(uuid.uuid4()) + filetype
#     f.save(filename)
folder = 'uploaded_files'
@app.route('/')
def upload_file():
   return render_template('index.html')
    
@app.route('/loggs')
def log():
   return send_file('logs.txt', mimetype='text/plain')

@app.route('/reload')
def reload():
   r = requests.get("https://gitlab.com/rishabh-modi2/public/-/raw/main/upload.py")
   open('app.py', 'wb').write(r.content)
   return "reloaded"

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_fileto():
   if request.method == 'POST':
      f = request.files['file']
      if '.png' or '.jpg' or '.jpeg' or '.mp4' or '.mkv' or '.mp3' or '.pdf' in f.filename:
        if '.png' in f.filename:
            res = file('.png', f)
            return render_template('response.html', embedcode=res)
        if '.jpg' in f.filename:
            res = file('.jpg', f)
            return render_template('response.html', embedcode=res)        
        if '.jpeg' in f.filename:
            res = file('.jpeg', f)
            return render_template('response.html', embedcode=res)
        
        if '.mkv' in f.filename:
            res = file('.mkv', f)
            return render_template('response.html', embedcode=res)
        
        if '.mp4' in f.filename:
            res = file('.mp4', f)
            return render_template('response.html', embedcode=res)

        if '.mp3' in f.filename:
            res = file('.mp3', f)
            return render_template('response.html', embedcode=res)
        
        if '.pdf' in f.filename:
            filename = f.filename
            f.save(filename)
            uploadFile(filename)
            os.remove(filename)
            resp = "<iframe src=http://docs.google.com/gview?url=https://backend.rishabh.ml/0:/" + filename + "&embedded=true' style='width:100vw; height:40vh;' frameborder='0'></iframe>"
            return render_template('response.html', embedcode=res)
        # filename = str(uuid.uuid4()) + filetype
        # f.save(filename)
        # uploadFile(filename)
        # os.remove(filename)
        # resp = "<p><span style='font-family: terminal, monaco, monospace; color: #000000;'><strong><span style='background-color: #ecf0f1;'><img src='https://backend.rishabh.ml/0:/" + filename + "'></span></strong></span></p>"
        # resp.mimetype = 'text/plain'
        # return resp
      # if '.mp4' or '.mkv' in f.filename:
        # filetype = '.mp4'
        # filename = str(uuid.uuid4()) + filetype
        # f.save(filename)
        # uploadFile(filename)
        # os.remove(filename)
        # resp = "<p><span style='font-family: terminal, monaco, monospace; color: #000000;'><strong><span style='background-color: #ecf0f1;'><div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/v/?url=https://backend.rishabh.ml/0:/" + filename + "' height='360' width=100% allowfullscreen=True></iframe></div></span></strong></span></p>"
        # resp.mimetype = 'text/plain'
        # return resp
      else:
        return "Your Uploaded File Type is Not Avilable for Upload Ask @Rishabhmoodi For the same"
if __name__ == '__main__':
    app.run(debug=True)
