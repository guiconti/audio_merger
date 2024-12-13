from flask import Flask, request, jsonify
import base64
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route("/", methods=["POST"])
def test():
	content = request.json
	mic_audio_base_64 = content.get("mic_audio_base_64", "")
	system_audio_base_64 = content.get("system_audio_base_64", "")
	mic_audio_buffer = base64.b64decode(mic_audio_base_64)
	if not system_audio_base_64:
		audio_buffer = mic_audio_buffer
	else:
		system_audio_buffer = base64.b64decode(system_audio_base_64)
		if not mic_audio_base_64:
			audio_buffer = system_audio_buffer
		else:

			mic_audio_file = io.BytesIO(mic_audio_buffer)
			system_audio_file = io.BytesIO(system_audio_buffer)

			mic_audio = AudioSegment.from_file(mic_audio_file, format="webm")
			system_audio = AudioSegment.from_file(system_audio_file, format="mp4")
			# final_audio = mic_audio.overlay(system_audio)
			final_audio = system_audio.overlay(mic_audio)
			audio_buffer = io.BytesIO()
			final_audio.export(audio_buffer)
			audio_buffer = audio_buffer.getbuffer()
	merged_audio_base_64 = base64.b64encode(audio_buffer)
	return jsonify({"merged_audio_base_64": merged_audio_base_64})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)