import atexit
import subprocess
#import vlc

class WebcamStreamer:
    def __init__(self, config):
        """
        Expected rtsp url format:
        "rtsp://user:password@192.168.0.1"
        """
        #self.instance = vlc.Instance()
        self.stream_name = "webcam"
        self.rtsp_url = config["rtsp_url"]
        atexit.register(self.cleanup)
        self.proc = None

    def cleanup(self):
        if self.proc is not None:
            self.proc.kill()

    def launch_webcam_stream_converter(self):
        """
        Basically here is what is done:
            cmd= ["cvlc", "-v", f"rtsp://user:password@192.168.0.16",
            f"--sout='#transcode{{vcodec=theo,vb=800,acodec=vorb,ab=128,channels=2,samplerate=44100,scodedec=none}}:http{{dst=:8080/webcam.ogg}}'"]
            subprocess.run(cmd)
        """
        # ret = vlc.libvlc_vlm_add_broadcast(
        #     p_instance=self.instance,
        #     psz_name=self.stream_name.encode(),
        #     psz_input=self.rtsp_url.encode(),
        #     psz_output=f"#transcode{{vcodec=theo,vb=800,acodec=vorb,ab=128,channels=2,samplerate=44100,scodedec=none}}:http{{dst=:8080/webcam.ogg}}".encode(),
        #     i_options=0,
        #     ppsz_options=[],
        #     b_enabled=True,
        #     b_loop=False
        # )
        # assert (ret == 0)
        # vlc.libvlc_vlm_play_media(self.instance, self.stream_name)
        cmd = ["cvlc", self.rtsp_url,
               "--sout='#transcode{vcodec=theo,vb=800,acodec=vorb,ab=128,channels=2,samplerate=44100,scodedec=none}:http{dst=:8080/webcam.ogg}'"]
        self.proc = subprocess.Popen(['/bin/bash', '-c', " ".join(cmd)], close_fds=True)