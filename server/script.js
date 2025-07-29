```javascript
function getDeviceInfo() {
  return {
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    battery: null,
    location: null
  };
}

async function sendData(data) {
  await fetch("/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });
}

navigator.getBattery().then(batt => {
  let info = getDeviceInfo();
  info.battery = `${Math.round(batt.level * 100)}%`;

  navigator.geolocation.getCurrentPosition(pos => {
    info.location = {
      lat: pos.coords.latitude,
      lon: pos.coords.longitude
    };
    sendData(info);
  }, () => {
    sendData(info);
  });
});