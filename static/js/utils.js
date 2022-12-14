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
  let hist_plot = {
    x: ["Feature1", "Feature2", "Feature3", "Feature4", "Feature5"],
    y: [],
    type: "bar",
  };

  let chart_data = {
    x: ["Dina", "Romaisaa", "Shaaban"],
    y: [],
    type: "bar",
  };
  let words_chart = {
    x: ["Close", "Open", "Push", "Window"],
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
  hist_plot.y = plot_data[2];
  input_mel.x = plot_data[3];
  input_mel.y = plot_data[4];
  input_mel.z = plot_data[5];
  chart_data.y = plot_data[6];
  words_chart.y = plot_data[7];

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
  };
  var bars_layout = {
    height: 250,
    margin: { l: 50, r: 50, b: 37, t: 25, pad: 1 },
  };
  let score_layout = {
    width: 350,
    height: 333,
    margin: { l: 40, r: 10, b: 37, t: 0, pad: 1 },
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
  let words_layout = {
    width: 350,
    height: 333,
    margin: { l: 40, r: 10, b: 37, t: 0, pad: 1 },
    shapes: [
      {
        type: "line",
        xref: "paper",
        x0: 0,
        y0: Math.max.apply(Math, words_chart.y),
        x1: 1,
        y1: Math.max.apply(Math, words_chart.y),
        line: {
          color: "red",
          width: 2,
        },
      },
    ],
  };
  let input_plot = document.getElementById("#input_plot");
  Plotly.newPlot("fingerprint", [input_bar], bars_layout);
  let fingerprint = document.getElementById("#fingerprint");

  Plotly.newPlot("mfcc_bars", [hist_plot], layout);
  let mfcc_bars = document.getElementById("#mfcc_bars");
  let scores_plot = document.getElementById("#scores_plot");
  Plotly.newPlot("scores_plot", [words_chart], words_layout);
  let words_plot = document.getElementById("#words_plot");
  Plotly.newPlot("words_plot", [chart_data], score_layout);
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
