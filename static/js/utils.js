let getData = async () => {
  let input_spectro = {
    z: [],
    type: "heatmap",
    colorscale: "Hot",
    // colorscale: colorScale,
  };
  let input_scatter = {
    x: [],
    y: [],
    type: "scatter",
    mode: "markers",

    marker: { color: "blue", size: 10 },
  };
  let predicted_spectro = {
    z: [],
    type: "heatmap",
    colorscale: "Hot",
    // colorscale: colorScale,
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
  input_spectro.x = plot_data[0];
  input_spectro.y = plot_data[1];
  input_spectro.z = plot_data[2];
  input_scatter.x = plot_data[3];
  input_scatter.y = plot_data[4];
  predicted_spectro.x = plot_data[5];
  predicted_spectro.y = plot_data[6];
  predicted_spectro.z = plot_data[7];

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
  };
  Plotly.newPlot("input_plot", [input_scatter, input_spectro], spectrolayout);
  let input_plot = document.getElementById("#input_plot");
  Plotly.newPlot("fingerprint", [predicted_spectro], spectrolayout);
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
