class VoiceRecorder {
  constructor() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      console.log("getUserMedia supported");
    } else {
      console.log("getUserMedia is not supported on your browser!");
    }

    this.mediaRecorder;
    this.stream;
    this.chunks = [];
    this.isRecording = false;
    this.startRef = document.querySelector("#recordButton");
    this.startRef.onclick = this.startRecording.bind(this);

    this.constraints = {
      audio: true,
      video: false,
    };
  }

  handleSuccess(stream) {
    this.stream = stream;

    this.stream.oninactive = () => {
      console.log("Stream ended!");
    };
    this.mediaRecorder = new MediaRecorder(this.stream);
    console.log(this.mediaRecorder);
    this.mediaRecorder.ondataavailable =
      this.onMediaRecorderDataAvailable.bind(this);
    this.mediaRecorder.onstop = this.onMediaRecorderStop.bind(this);
    this.mediaRecorder.start();
  }

  handleError(error) {
    console.log("navigator.getUserMedia error: ", error);
  }

  onMediaRecorderDataAvailable(e) {
    this.chunks.push(e.data);
  }

  async onMediaRecorderStop(e) {
    const blob = new Blob(this.chunks, { type: "audio/wav; codecs=opus" });
    blob.name = "new_record.wav";
    const audioURL = window.URL.createObjectURL(blob);
    console.log(audioURL);
    // this.playerRef.src = audioURL;
    this.chunks = [];
    this.stream.getAudioTracks().forEach((track) => track.stop());
    this.stream = null;
    console.log(blob);
    let userName;
    await $.ajax({
      method: "POST",
      url: "http://127.0.0.1:5001/predict-user",
      dataType: "json",
      async: false,
      data: {
        record: "wav_file",
      },
      success: function (res, status, xhr) {
        userName = res;
      },
    });
    console.log(userName);
  }

  async startRecording() {
    if (this.isRecording) return;
    this.startRef.innerHTML = '<button class="Rec">Recording</button>';
    this.isRecording = true;
    // this.playerRef.src = "";
    navigator.mediaDevices
      .getUserMedia(this.constraints)
      .then(this.handleSuccess.bind(this))
      .catch(this.handleError.bind(this));
    await new Promise((resolve) => setTimeout(resolve, 3000));
    this.startRef.innerHTML =
      '<img src="/static/img/mic.svg" alt="Record" class="img-fluid id="stop"" />';
    this.stopRecording();
  }

  stopRecording() {
    if (!this.isRecording) return;
    this.isRecording = false;
    this.mediaRecorder.stop();
  }
}

window.voiceRecorder = new VoiceRecorder();
