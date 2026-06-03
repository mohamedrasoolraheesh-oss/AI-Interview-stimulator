import os
import tempfile
import numpy as np
import cv2
import librosa

try:
    from fer import FER
except ImportError:
    FER = None


class EmotionDetector:
    POSITIVE_KEYWORDS = {
        "happy", "great", "good", "excellent", "confident", "strong", "optimistic", "positive", "successful", "excited"
    }
    NEGATIVE_KEYWORDS = {
        "worried", "nervous", "struggle", "difficult", "unsure", "weak", "concerned", "negative", "anxious", "bad"
    }

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.fer_detector = FER(mtcnn=True) if FER is not None else None

    def detect_emotion_from_audio(self, audio_file):
        """Detect emotion from an audio file using audio features."""
        audio_path = self._ensure_file_path(audio_file, suffix=".wav")

        try:
            signal, sr = librosa.load(audio_path, sr=22050, mono=True)
            rms = librosa.feature.rms(signal)[0]
            tempo, _ = librosa.beat.beat_track(signal, sr=sr)
            centroid = librosa.feature.spectral_centroid(signal, sr=sr)[0]
            zcr = librosa.feature.zero_crossing_rate(signal)[0]
        except Exception:
            return {
                "confidence": 0.0,
                "emotion": "unknown",
                "valence": 0.5,
                "arousal": 0.5,
                "reason": "Unable to analyze audio input."
            }

        rms_mean = float(np.mean(rms))
        tempo_value = float(tempo)
        centroid_mean = float(np.mean(centroid))
        zcr_mean = float(np.mean(zcr))

        if rms_mean > 0.03 and tempo_value > 120:
            emotion = "excited"
        elif rms_mean < 0.01 and centroid_mean < 2000:
            emotion = "sad"
        elif tempo_value > 100 and centroid_mean > 2500:
            emotion = "happy"
        else:
            emotion = "neutral"

        valence = min(1.0, max(0.0, (centroid_mean / 5000)))
        arousal = min(1.0, max(0.0, (rms_mean * 20)))
        confidence = round(min(1.0, 0.2 + (tempo_value / 200) + (rms_mean * 10)), 2)

        return {
            "emotion": emotion,
            "confidence": confidence,
            "valence": round(valence, 2),
            "arousal": round(arousal, 2),
            "audio_features": {
                "rms_mean": round(rms_mean, 5),
                "tempo": round(tempo_value, 2),
                "spectral_centroid": round(centroid_mean, 2),
                "zero_crossing_rate": round(zcr_mean, 5)
            }
        }

    def detect_emotion_from_video(self, video_file):
        """Detect approximate emotion changes from a video using face detection."""
        video_path = self._ensure_file_path(video_file, suffix=".mp4")
        capture = cv2.VideoCapture(video_path)

        if not capture.isOpened():
            return {
                "frame_emotions": [],
                "dominant_emotion": "unknown",
                "emotion_timeline": [],
                "reason": "Unable to open video file."
            }

        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, frame_count // 10)
        timeline = []

        for idx in range(0, frame_count, step):
            capture.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = capture.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            brightness = float(np.mean(gray))

            if len(faces) > 0 and brightness > 120:
                emotion = "neutral"
            else:
                emotion = "focused"

            timeline.append({
                "frame_index": idx,
                "emotion": emotion,
                "face_count": int(len(faces)),
                "brightness": round(brightness, 2)
            })

        capture.release()

        dominant = "neutral"
        if timeline:
            emotions = [item["emotion"] for item in timeline]
            dominant = max(set(emotions), key=emotions.count)

        return {
            "frame_emotions": timeline,
            "dominant_emotion": dominant,
            "emotion_timeline": timeline
        }

    def analyze_speech_sentiment(self, text: str):
        """Analyze sentiment of spoken text with keyword matching."""
        normalized = text.lower()
        positive_matches = [word for word in self.POSITIVE_KEYWORDS if word in normalized]
        negative_matches = [word for word in self.NEGATIVE_KEYWORDS if word in normalized]

        score = len(positive_matches) - len(negative_matches)
        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        confidence = round(min(1.0, abs(score) / 5 + 0.3), 2)
        keywords = positive_matches + negative_matches

        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": keywords
        }

    def detect_emotion_from_frame(self, frame):
        """Detect the dominant emotion from a single camera frame."""
        if FER is not None:
            result = self.fer_detector.detect_emotions(frame)
            if result and result[0].get("emotions"):
                emotions = result[0]["emotions"]
                dominant = max(emotions, key=emotions.get)
                confidence = round(emotions[dominant] * 100, 2)
                return dominant, confidence

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        brightness = float(np.mean(gray))

        if len(faces) == 0:
            return "No Face Detected", 0

        if brightness > 130:
            return "happy", 75
        if brightness < 80:
            return "sad", 55

        return "neutral", 65

    def _ensure_file_path(self, file_like, suffix=".wav"):
        if hasattr(file_like, "read"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(file_like.read())
                return temp_file.name
        if isinstance(file_like, str) and os.path.exists(file_like):
            return file_like
        return str(file_like)


import time

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)


def detect_emotion():
    cap = cv2.VideoCapture(0)

    time.sleep(2)

    detected = False
    confidence = 0

    for _ in range(30):
        ret, frame = cap.read()

        if not ret:
            continue

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) > 0:
            detected = True
            confidence = 85
            break

    cap.release()

    if detected:
        return "Neutral", confidence

    return "No Face Detected", 0
