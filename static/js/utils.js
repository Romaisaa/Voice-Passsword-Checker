let getData = async () => {
  let input_bar = {
    type: "bar",
    // colorscale: colorScale,
  };
  let input_mel = {
    z: [],
    type: "heatmap",
    colorscale: "Hot",
  };

  let chart_data = {
    x: ["Dina", "Romaisaa", "Shaaban"],
    y: [],
    type: "bar",
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
  input_bar.x = plot_data[0];
  input_bar.y = plot_data[1];
  input_mel.x = plot_data[2];
  input_mel.y = plot_data[3];
  input_mel.z = plot_data[4];
  chart_data.y = plot_data[5];

  let spectrolayout = {
    height: 250,
    margin: { l: 50, r: 50, b: 25, t: 25, pad: 1 },
    yaxis: {
      showticklabels: false,
      showtickprefix: "none",
      showticksuffix: "none",
    },
    xaxis: {
      showticklabels: false,
      showtickprefix: "none",
      showticksuffix: "none",
    },
  };
  Plotly.newPlot("input_plot", [input_mel], spectrolayout);
  var min_score = Math.min.apply(Math, chart_data.y);
  var index = chart_data.y.indexOf(min_score);
  let high_scores = [];
  for (i = 0; i < 3; i++) {
    if (i === index) continue;
    high_scores.push(chart_data.y[i]);
  }
  var layout = {
    height: 250,
    margin: { l: 50, r: 50, b: 25, t: 25, pad: 1 },
    shapes: [
      {
        type: "line",
        xref: "paper",
        x0: 0,
        y0: high_scores[0],
        x1: 1,
        y1: high_scores[0],
        line: {
          color: "red",
          width: 2,
        },
      },
      {
        type: "line",
        xref: "paper",
        x0: 0,
        y0: high_scores[1],
        x1: 1,
        y1: high_scores[1],
        line: {
          color: "red",
          width: 2,
        },
      },
    ],
  };
  var bars_layout = {
    height: 250,
    margin: { l: 50, r: 50, b: 37, t: 25, pad: 1 },
  };
  let input_plot = document.getElementById("#input_plot");
  Plotly.newPlot("fingerprint", [chart_data], layout);
  let fingerprint = document.getElementById("#fingerprint");

  Plotly.newPlot("mfcc_bars", [input_bar], bars_layout);
  let mfcc_bars = document.getElementById("#mfcc_bars");
};

let lockText = document.querySelector("#lock-text");
let lockImg = document.querySelector("#lock-img");
let username = document.querySelector("#user-name");
let auth = document.querySelector("#auth");

let changeStyle = async (predicted_username) => {
  if (predicted_username == "Unknown" || predicted_username == "ERROR") {
    lockText.innerHTML = "Locked";
    lockImg.innerHTML =
      '<img src="/static/img/lock.svg"alt="locked"class="img-fluid"width="150"/>';
    auth.innerHTML = "You are not authorized";

    if (predicted_username == "ERROR") {
      username.innerHTML = "Error, please try again";
    } else username.innerHTML = "Sorry, Can't be recognized";
  } else {
    lockText.innerHTML = "Unlocked";
    lockImg.innerHTML =
      '<img src="/static/img/unlock.svg"alt="locked"class="img-fluid"width="150"/>';
    username.innerHTML = `Welcome, ${predicted_username}`;
    auth.innerHTML = "You have been authorized";
  }
};
