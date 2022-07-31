import subprocess
import shlex
from storage import Storage
from pydub import AudioSegment
from pydub.utils import make_chunks 
from math import ceil

# seconds
slotDurations = {
    'date':      3.0,
    'location':  4.2,
    'user_name': 2.41,
    'car':       5.5
}

def retime(path, slotName):
    slotDuration = slotDurations[slotName]
    segment = AudioSegment.from_wav(path) 
    # input has longer duration 
    if segment.duration_seconds > slotDuration:
        print('[WARNING] trimmed', path, f"from {segment.duration_seconds} to {slotDuration} secs")
        segment = segment[0:slotDuration*1000]
        return
    # add silence at the end
    silenceDuration = ceil((slotDuration-segment.duration_seconds)*1000) 
    segment += AudioSegment.silent(duration=silenceDuration)
    chunks = make_chunks(segment, slotDuration*1000)
    segment = chunks[0]
    # add leading silence if input is a user_name
    if (slotName == 'user_name'):
        leadSilenceDuration = 446 # millis
        segment_userName = AudioSegment.silent(duration=leadSilenceDuration) 
        segment_userName += segment
        chunks = make_chunks(segment_userName, slotDuration*1000) 
        segment = chunks[0]
    # export
    pathOut = path.replace(".wav", "_retimed.wav")
    segment.export(pathOut, format="wav") 
    print('retimed', path)
    return pathOut

def reencode(path): 
    pathOut = path.replace(".wav", ".m4a")
    cmd = f'ffmpeg -i {path} -c:a aac -b:a 128k -ar 44100 -ac 2 {pathOut} -y'
    cmd_sh = shlex.split(cmd)
    process = subprocess.Popen(cmd_sh, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
        raise RuntimeError(stderr)
    print(f're-encoded {path}')
    return pathOut

def conform(path, slotName):
    retimed = retime(path, slotName)
    reencoded = reencode(retimed)
    return reencoded

def upload(localPath, bucketName, remotePath, forceUpload=True):
    # s3 = Storage(bucket=bucketName, force_upload=forceUpload)
    # s3.upload_file(localPath, remotePath)
    print(f'uploaded {localPath}')