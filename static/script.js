let moistureData = [];
let tempData = [];
let humidityData = [];
let timeLabels = [];

const moistureLabel = document.getElementById('moisture');
const tempLabel = document.getElementById('temp');
const humidityLabel = document.getElementById('humidity');
const irrigationLabel = document.getElementById('irrigation');

const moistureChart = new Chart(document.getElementById('moistureChart'), {
  type: 'line',
  data: {
    labels: timeLabels,
    datasets: [{
      label: 'Soil Moisture (%)',
      data: moistureData,
      borderColor: '#43a047',
      backgroundColor: 'rgba(67,160,71,0.2)',
      tension: 0.4,
      fill: true
    }]
  },
  options: {
    responsive: true,
    interaction: {
      mode: 'nearest',
      intersect: false
    },
    plugins: {
      tooltip: {
        enabled: true
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'x', // Enable horizontal panning
          modifierKey: null
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true
          },
          mode: 'x',
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Soil Moisture (%)'
        },
        ticks: {
          color: '#43a047' // Set y-axis label color to match point color (green)
        }
      }
    }
  }
});

const tempHumidityChart = new Chart(document.getElementById('tempHumidityChart'), {
  type: 'line',
  data: {
    labels: timeLabels,
    datasets: [
      {
        label: 'Temperature (°C)',
        data: tempData,
        borderColor: '#f57c00',
        backgroundColor: 'rgba(255,152,0,0.3)',
        tension: 0.4,
        yAxisID: 'y',
        fill: false
      },
      {
        label: 'Humidity (%)',
        data: humidityData,
        borderColor: '#0288d1',
        backgroundColor: 'rgba(2,136,209,0.3)',
        tension: 0.4,
        yAxisID: 'y1',
        fill: false
      }
    ]
  },
  options: {
    responsive: true,
    interaction: {
      mode: 'index', // Show all datasets at hovered x
      intersect: false
    },
    plugins: {
      tooltip: {
        enabled: true,
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            // Show both temperature and humidity on hover
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            return `${label}: ${value}`;
          }
        }
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'x',
          modifierKey: null
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true
          },
          mode: 'x',
        }
      }
    },
    scales: {
      y: {
        type: 'linear',
        position: 'left',
        min: 0,
        max: 50,
        title: {
          display: true,
          text: 'Temperature (°C)'
        },
        ticks: {
          color: '#f57c00' // Temperature axis label color (orange)
        }
      },
      y1: {
        type: 'linear',
        position: 'right',
        min: 0,
        max: 100,
        grid: { drawOnChartArea: false },
        title: {
          display: true,
          text: 'Humidity (%)'
        },
        ticks: {
          color: '#0288d1' // Humidity axis label color (blue)
        }
      }
    }
  }
});

function updateDashboard() {
  fetch('/sensor_data')
    .then(response => response.json())
    .then(data => {
      if (data.error) return;

      const now = new Date().toLocaleTimeString();
      const moisture = Math.round(data.soil);
      const temp = Math.round(data.temp);
      const humidity = Math.round(data.hum);
      const irrigationStatus = data.pump;

      moistureLabel.innerText = moisture + ' %';
      tempLabel.innerText = temp + ' °C';
      humidityLabel.innerText = humidity + ' %';
      irrigationLabel.innerText = irrigationStatus;

      // Set color based on pump status
      if (irrigationStatus === "ON") {
        irrigationLabel.style.color = "green";
      } else if (irrigationStatus === "OFF") {
        irrigationLabel.style.color = "red";
      } else {
        irrigationLabel.style.color = ""; // default
      }

      // if (timeLabels.length > 10) {
      //   timeLabels.shift();
      //   moistureData.shift();
      //   tempData.shift();
      //   humidityData.shift();
      // }

      timeLabels.push(now);
      moistureData.push(moisture);
      tempData.push(temp);
      humidityData.push(humidity);

      moistureChart.update();
      tempHumidityChart.update();
    });
}

function resetZoomAll() {
  moistureChart.resetZoom();
  tempHumidityChart.resetZoom();
}

setInterval(updateDashboard, 2000);
updateDashboard();
