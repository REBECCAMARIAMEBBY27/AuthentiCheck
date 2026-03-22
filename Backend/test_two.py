from app.services.image_service import predict_image
from app.services.audio_service import predict_audio

# Image
label_img, img_conf = predict_image("test.jpg")
print("Image:", label_img, img_conf)

# Audio
label_audio, audio_conf = predict_audio("test.wav")
print("Audio:", label_audio, audio_conf)

# 🔥 Weighted combination
final_conf = (0.6 * img_conf) + (0.4 * audio_conf)

final_label = "AI Generated" if final_conf > 50 else "Human Generated"

print("\nFINAL RESULT:")
print(final_label, final_conf)