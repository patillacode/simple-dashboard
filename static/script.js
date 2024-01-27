let elapsedTime = 0;
let refreshInterval = 300000; // 5 minutes in milliseconds
// let refreshInterval = 60000; // 1 minute in milliseconds
// let refreshInterval = 30000; // 30 seconds in milliseconds
// let refreshInterval = 10000; // 10 seconds in milliseconds
let intervals = [];
let updateTimeInterval = null;

function formatElapsedTime(seconds) {
  if (seconds == 0) {
    return "just now";
  } else if (seconds < 60) {
    return `${seconds} seconds ago`;
  } else if (seconds < 3600) {
    if (seconds < 120) {
      return "1 minute ago";
    }
    return `${Math.floor(seconds / 60)} minutes ago`;
  } else {
    return `${Math.floor(seconds / 3600)} hours ago`;
  }
}

function updateRefreshTime() {
    elapsedTime += 5;
    const refreshTimeSpan = document.getElementById("refresh-time");
    refreshTimeSpan.textContent = formatElapsedTime(elapsedTime);
}

function refreshService(serviceId) {
    elapsedTime = -5;

    fetch(`/status/${serviceId}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            const serviceDiv = document.getElementById(`service--${serviceId}`);
            const statusIndicator = document.getElementById(`status-indicator-${serviceId}`);
            const hrStatusIndicator = document.getElementById(`hr-status-indicator-${serviceId}`);

            serviceDiv.className = `bg-gray-800 text-white p-4 rounded-lg justify-center border-1  ${
                data.active ? "neon-green" : "neon-pink"
            }`;
            statusIndicator.className = `rounded-full h-1.5 w-1.5 ${
                data.active ? "bg-lime-500 neon-green" : "bg-rose-600 neon-pink"
            }`;
            hrStatusIndicator.className = `w-1/2 my-1 ${
              data.active
                ? "neon-green border-lime-500"
                : "neon-pink border-rose-600"
            }`;

            console.log(`Refreshed service ${serviceId} ${data.active}`);

        })
        .catch((error) => {
            const refreshTimeSpan = document.getElementById("refresh-time");
            refreshTimeSpan.textContent = `failed for service ${serviceId}: ${error.message}`;

            // Clear all intervals
            intervals.forEach(clearInterval);
            clearInterval(updateTimeInterval); // Clear the updateRefreshTime interval
        });
    updateRefreshTime();
}

function initializeServiceRefresh() {
    const serviceDivs = document.querySelectorAll('[id^="service--"]');

    serviceDivs.forEach((serviceDiv) => {
        const serviceId = serviceDiv.id.split("--")[1];
        const intervalId = setInterval(() => refreshService(serviceId), refreshInterval);
        intervals.push(intervalId);
    });

    // Store the interval ID for the updateRefreshTime function
    updateTimeInterval = setInterval(updateRefreshTime, 5000);
}

initializeServiceRefresh();
