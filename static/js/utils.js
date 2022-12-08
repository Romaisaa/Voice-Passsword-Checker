let getData = async () => {
  // let colorScale = [
  //   ["0.0", "#023a21"],
  //   ["0.111111111111", "#035934"],
  //   ["0.222222222222", "#027161"],
  //   ["0.333333333333", "#02888e"],
  //   ["0.444444444444", "#01a0bb"],
  //   ["0.555555555556", "#00b7e8"],
  //   ["0.666666666667", "#048ac5"],
  //   ["0.777777777778", "#085da2"],
  //   ["0.888888888889", "#0f025b"],
  //   ["1.0", "#0f025b"],
  // ];
  // let colorScale = [
  //   [0.0, "rgb(237, 229, 207)"],
  //   [0.16666666666666666, "rgb(224,194, 162)"],
  //   [0.3333333333333333, "rgb(211, 156, 131)"],
  //   [0.5, "rgb(193, 118, 111)"],
  //   [0.6666666666666666, "rgb(166, 84, 97)"],
  //   [0.8333333333333334, "rgb(129, 55, 83)"],
  //   [1.0, "rgb(84, 31,63)"],
  // ];
  let spectro = {
    z: [],
    type: "heatmap",
    colorscale: "Hot",
    // colorscale: colorScale,
  };
  let scatter = {
    x: [],
    y: [],
    type: "scatter",
    mode: "markers",

    marker: { color: "blue", size: 10 },
  };
  let plot_data;
  $.ajax({
    method: "POST",
    url: "http://127.0.0.1:5001/plot-data",
    dataType: "json",
    async: false,
    data: {},
    success: function (res, status, xhr) {
      plot_data = res;
    },
  });
  spectro.x = plot_data[0];
  spectro.y = plot_data[1];
  spectro.z = plot_data[2];
  scatter.x = plot_data[3];
  scatter.y = plot_data[4];

  let spectrolayout = {
    // width: auto,
    height: 300,
    margin: { l: 50, r: 50, b: 25, t: 25, pad: 1 },
    yaxis: {
      // range: [0, Math.max.apply(Math, spectro.x)],
      showticklabels: false,
      showtickprefix: "none",
      showticksuffix: "none",
    },
    xaxis: {
      showticklabels: false,
      showtickprefix: "none",
      showticksuffix: "none",
    },
    title: "Input Audio",
  };
  Plotly.newPlot("input_plot", [scatter, spectro], spectrolayout);
  Plotly.newPlot("fingerprint", [spectro], spectrolayout);

  let input_plot = document.getElementById("#input_plot");
  let fingerprint = document.getElementById("#fingerprint");
};

let lockText = document.querySelector("#lock-text");
let lockImg = document.querySelector("#lock-img");
let username = document.querySelector("#user-name");
let auth = document.querySelector("#auth");

let changeStyle = async (predicted_username) => {
  if (predicted_username == "Unknown") {
    lockText.innerHTML = "Locked";
    lockImg.innerHTML =
      '<img src="/static/img/lock.svg"alt="locked"class="img-fluid"width="150"/>';
    username.innerHTML = "Sorry, Can't be recognized";
    auth.innerHTML = "You are not authorized";
  } else {
    lockText.innerHTML = "Unlocked";
    lockImg.innerHTML =
      '<img src="/static/img/unlock.svg"alt="locked"class="img-fluid"width="150"/>';
    username.innerHTML = `Welcome, ${predicted_username}`;
    auth.innerHTML = "You have been authorized";
  }
};
