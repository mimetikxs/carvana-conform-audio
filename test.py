import os
import conform_audio as ca

# conform
localPath_car = ca.conform('sampleAudios/sample_car.wav', 'car')
localPath_date = ca.conform('sampleAudios/sample_date.wav', 'date')
localPath_location = ca.conform('sampleAudios/sample_location.wav', 'location')
localPath_user_name = ca.conform('sampleAudios/sample_user_name.wav', 'user_name')

# upload
ca.upload(localPath_car, 'a3_bucket_name', f'audio_pieces/car/{os.path.basename(localPath_car)}')
ca.upload(localPath_date, 'a3_bucket_name', f'audio_pieces/date/{os.path.basename(localPath_date)}')
ca.upload(localPath_location, 'a3_bucket_name', f'audio_pieces/location/{os.path.basename(localPath_location)}')
ca.upload(localPath_user_name, 'a3_bucket_name', f'audio_pieces/user_name/{os.path.basename(localPath_user_name)}')