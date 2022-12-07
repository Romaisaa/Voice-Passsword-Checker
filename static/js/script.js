class VoiceRecorder {
  constructor() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      console.log("getUserMedia supported");
    } else {
      console.log("getUserMedia is not supported on your browser!");
    }
    this.isRecording = false;
    this.startRef = document.querySelector("#recordButton");
    this.startRef.onclick = this.startRecording.bind(this);
    this.constraints = {
      audio: true,
      video: false,
    };
    this.counter = 0;
  }

  async startRecording() {
    // if (this.isRecording) return;
    this.startRef.innerHTML = '<button class="Rec">Recording</button>';
    this.isRecording = true;
    // Start Recording Functionality
    var gumStream, rec, input, audioContext;
    navigator.mediaDevices
      .getUserMedia(this.constraints)
      .then(function (stream) {
        gumStream = stream;
        audioContext = new AudioContext();
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input, { numChannels: 1 });
        rec.record();
      })
      .catch(function (err) {
        console.log(err);
      });
    // 3 Sec Record
    await new Promise((resolve) => setTimeout(resolve, 3000));

    // Stop Recording

    rec.stop();
    this.startRef.innerHTML =
      '<img src="/static/img/mic.svg" alt="Record" class="img-fluid id="stop"" />';
    gumStream.getAudioTracks()[0].stop();

    //Export record as wav file and send to back
    rec.exportWAV(this.exportToBack);
  }

  // Send blob file to backend
  async exportToBack(blob) {
    let userName;
    var formData = new FormData();
    formData.append("source", blob, blob.name);
    await $.ajax({
      method: "POST",
      url: "http://127.0.0.1:5001/predict-user",
      processData: false,
      contentType: false,
      async: false,
      data: formData,
      success: function (res, status, xhr) {
        userName = res;
      },
    });
    console.log(userName);
    // var url = URL.createObjectURL(blob);
    // var au = document.createElement("audio");
    // var li = document.createElement("li");
    // var link = document.createElement("a");
    // //add controls to the <audio> element
    // au.controls = true;
    // au.src = url;
    // //link the a element to the blob
    // link.href = url;
    // link.download = new Date().toISOString() + ".wav";
    // link.innerHTML = link.download;
  }
}

window.voiceRecorder = new VoiceRecorder();
