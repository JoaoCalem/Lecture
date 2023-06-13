from streamlit_webrtc import WebRtcMode, webrtc_streamer
import av
import cv2
from twilio.rest import Client
import streamlit as st

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = st.secrets['sid']
auth_token = st.secrets['token']
client = Client(account_sid, auth_token)

token = client.tokens.create()

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")
    cv2.putText(
            image,
            str(image.mean()),
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2,
        )
    return av.VideoFrame.from_ndarray(image, format="bgr24")


webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    rtc_configuration={
      "iceServers": token.ice_servers
    },
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)
