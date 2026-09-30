/* JARVIS Sci-Fi Visual HUD App Script - Complete Camera Hardware Release Edition */

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initCore3DCanvas();
    initAudioSpectrum();
    initControls();
    initRealtimeAutoSync();

    // Default ON: Automatically start camera when app loads
    setTimeout(() => {
        if (window.toggleWebcam) {
            window.toggleWebcam(true);
        }
    }, 600);
});

let webcamStream = null;
let isCameraActive = false;

// 1. System Clock
function initClock() {
    const timeEl = document.getElementById('system-time');
    function updateTime() {
        const now = new Date();
        timeEl.textContent = now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
    }
    setInterval(updateTime, 1000);
    updateTime();
}

let isTogglingCamera = false;

// 2. Complete Hardware Camera Release Toggle Controller
async function toggleWebcam(forceState) {
    if (isTogglingCamera) return;
    if (forceState !== undefined && forceState === isCameraActive) {
        return;
    }
    const shouldActivate = (forceState !== undefined) ? forceState : !isCameraActive;

    const video = document.getElementById('webcam-video');
    const camStatus = document.getElementById('camera-status');
    const overlay = document.getElementById('video-privacy-overlay');
    const reticle = document.getElementById('reticle-overlay');
    const btnToggle = document.getElementById('btn-toggle-video');
    const presenceVal = document.getElementById('presence-value');
    const fpsTag = document.getElementById('fps-tag');

    isTogglingCamera = true;

    if (shouldActivate) {
        // TURN CAMERA ON
        try {
            // Clean up any existing stream first
            if (webcamStream) {
                webcamStream.getTracks().forEach(t => { try { t.stop(); } catch(e){} });
                webcamStream = null;
            }

            try {
                webcamStream = await navigator.mediaDevices.getUserMedia({
                    video: { width: { ideal: 1280 }, height: { ideal: 720 } },
                    audio: false
                });
            } catch (strictErr) {
                console.warn('Strict constraints failed, falling back to default video:', strictErr);
                webcamStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            }

            if (video) {
                video.srcObject = webcamStream;
                video.muted = true;
                video.play().catch(playErr => console.warn('video.play handled:', playErr));
            }

            isCameraActive = true;

            if (overlay) overlay.style.display = 'none';
            if (reticle) reticle.style.display = 'block';

            if (camStatus) {
                camStatus.textContent = 'CAM: ONLINE (30 FPS)';
                camStatus.className = '';
                camStatus.style.color = '#00ff88';
            }

            if (fpsTag) {
                fpsTag.textContent = '30 FPS';
                fpsTag.style.color = '#00ff88';
            }

            if (presenceVal) {
                presenceVal.textContent = 'USER_ARRIVED (ONLINE)';
                presenceVal.style.color = '#00ff88';
            }

            if (btnToggle) {
                btnToggle.textContent = '📷 VIDEO ON (CLICK TO DISABLE)';
                btnToggle.classList.add('active');
            }
        } catch (err) {
            console.warn('Webcam activation error:', err);
            isCameraActive = false;
            if (overlay) overlay.style.display = 'flex';
            if (reticle) reticle.style.display = 'none';
            if (camStatus) {
                camStatus.textContent = 'CAM: ERROR (' + (err.name || 'FAILED') + ')';
                camStatus.style.color = '#ff3366';
            }
            if (btnToggle) {
                btnToggle.textContent = '📷 VIDEO ON / OFF (CLICK TO ENABLE)';
                btnToggle.classList.remove('active');
            }
            if (window.addLiveLog) {
                window.addLiveLog('SYS', '카메라 켜기 실패: ' + (err.message || err.name));
            }
        } finally {
            isTogglingCamera = false;
        }
    } else {
        // FULL HARDWARE CAMERA RELEASE (TURNS OFF CAMERA GREEN LED INSTANTLY)
        try {
            if (webcamStream) {
                const tracks = webcamStream.getTracks();
                tracks.forEach(track => {
                    try { track.stop(); } catch(e){}
                });
                webcamStream = null;
            }
            if (video) {
                if (video.srcObject) {
                    const srcTracks = video.srcObject.getTracks ? video.srcObject.getTracks() : [];
                    srcTracks.forEach(t => { try { t.stop(); } catch(e){} });
                }
                video.pause();
                video.srcObject = null;
                // Note: video.load() intentionally omitted to avoid breaking WKWebView media element
            }
        } catch (e) {
            console.error('Error releasing camera hardware:', e);
        } finally {
            isCameraActive = false;
            isTogglingCamera = false;
        }

        if (overlay) overlay.style.display = 'flex';
        if (reticle) reticle.style.display = 'none';

        if (camStatus) {
            camStatus.textContent = 'CAM: PRIVACY MODE (OFF)';
            camStatus.className = 'cam-off';
            camStatus.style.color = '#ff3366';
        }

        if (fpsTag) {
            fpsTag.textContent = 'PRIVACY MODE';
            fpsTag.style.color = '#ff3366';
        }

        if (presenceVal) {
            presenceVal.textContent = 'DISABLED (OFF)';
            presenceVal.style.color = '#ff3366';
        }

        if (btnToggle) {
            btnToggle.textContent = '📷 VIDEO ON / OFF (CLICK TO ENABLE)';
            btnToggle.classList.remove('active');
        }
    }
}

// 3. Multi-Color 3D Glowing Particle AI Core Sphere Canvas
function initCore3DCanvas() {
    const canvas = document.getElementById('core-canvas');
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    function resize() {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
    }
    resize();
    window.addEventListener('resize', resize);

    const particles = [];
    const numParticles = 320;
    const baseRadius = 100;
    const palette = ['#00f3ff', '#ff00b7', '#9d00ff', '#ffb700', '#0077ff', '#00ff88'];

    for (let i = 0; i < numParticles; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos((Math.random() * 2) - 1);
        particles.push({
            x: baseRadius * Math.sin(phi) * Math.cos(theta),
            y: baseRadius * Math.sin(phi) * Math.sin(theta),
            z: baseRadius * Math.cos(phi),
            baseX: baseRadius * Math.sin(phi) * Math.cos(theta),
            baseY: baseRadius * Math.sin(phi) * Math.sin(theta),
            baseZ: baseRadius * Math.cos(phi),
            color: palette[i % palette.length],
            size: Math.random() * 2.5 + 1.2,
            speed: (Math.random() - 0.5) * 0.02
        });
    }

    let angleX = 0;
    let angleY = 0;
    let ringAngle = 0;
    let isSpeaking = false;

    function render() {
        const width = canvas.width / dpr;
        const height = canvas.height / dpr;
        const centerX = width / 2;
        const centerY = height / 2;

        ctx.clearRect(0, 0, width, height);

        ringAngle += 0.015;
        const ringRadius = baseRadius + 18 + Math.sin(Date.now() * 0.004) * 6;

        // Ring 1 (Cyan)
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(ringAngle);
        ctx.beginPath();
        ctx.ellipse(0, 0, ringRadius, ringRadius * 0.35, 0, 0, Math.PI * 2);
        ctx.strokeStyle = isSpeaking ? 'rgba(255, 183, 0, 0.8)' : 'rgba(0, 243, 255, 0.6)';
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 20;
        ctx.shadowColor = isSpeaking ? '#ffb700' : '#00f3ff';
        ctx.stroke();
        ctx.restore();

        // Ring 2 (Magenta)
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(-ringAngle * 0.7);
        ctx.beginPath();
        ctx.ellipse(0, 0, ringRadius * 1.1, ringRadius * 0.4, Math.PI / 4, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(255, 0, 183, 0.5)';
        ctx.lineWidth = 2;
        ctx.shadowBlur = 15;
        ctx.shadowColor = '#ff00b7';
        ctx.stroke();
        ctx.restore();

        angleX += 0.006;
        angleY += 0.01;

        const cosX = Math.cos(angleX), sinX = Math.sin(angleX);
        const cosY = Math.cos(angleY), sinY = Math.sin(angleY);

        particles.forEach(p => {
            let y1 = p.baseY * cosX - p.baseZ * sinX;
            let z1 = p.baseY * sinX + p.baseZ * cosX;
            let x2 = p.baseX * cosY + z1 * sinY;
            let z2 = -p.baseX * sinY + z1 * cosY;

            const scale = 300 / (300 + z2);
            const projX = centerX + x2 * scale;
            const projY = centerY + y1 * scale;

            const alpha = Math.max(0.2, (z2 + baseRadius) / (2 * baseRadius));
            const pRadius = p.size * scale;

            ctx.beginPath();
            ctx.arc(projX, projY, pRadius, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = alpha;
            ctx.shadowBlur = 10;
            ctx.shadowColor = p.color;
            ctx.fill();
            ctx.globalAlpha = 1.0;
        });

        requestAnimationFrame(render);
    }
    render();

    window.setJarvisState = (state) => {
        const label = document.getElementById('core-state-label');
        if (state === 'speaking') {
            isSpeaking = true;
            label.textContent = '[AI CORE: SPEAKING EXECUTIVE BRIEFING]';
            label.style.color = '#ffb700';
        } else if (state === 'listening') {
            isSpeaking = false;
            label.textContent = '[AI CORE: LISTENING TO VOICE COMMAND]';
            label.style.color = '#00ff88';
        } else {
            isSpeaking = false;
            label.textContent = '[AI CORE: REALTIME LIVE AUTO-SYNC ACTIVE]';
            label.style.color = '#00f3ff';
        }
    };
}

// 4. Audio Spectrum Equalizer Waveform
function initAudioSpectrum() {
    const canvas = document.getElementById('spectrum-canvas');
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    function resize() {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);
    }
    resize();
    window.addEventListener('resize', resize);

    const bars = 80;

    function drawSpectrum() {
        const width = canvas.width / dpr;
        const height = canvas.height / dpr;
        ctx.clearRect(0, 0, width, height);

        const barWidth = width / bars;
        const time = Date.now() * 0.004;

        for (let i = 0; i < bars; i++) {
            const h = Math.abs(Math.sin(time + i * 0.12) * Math.cos(i * 0.08)) * (height * 0.85) + 4;
            const x = i * barWidth;
            const y = height - h;

            const gradient = ctx.createLinearGradient(0, height, 0, 0);
            gradient.addColorStop(0, '#0077ff');
            gradient.addColorStop(0.5, '#ff00b7');
            gradient.addColorStop(1, '#00f3ff');

            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, y, barWidth - 2, h);
        }
        requestAnimationFrame(drawSpectrum);
    }
    drawSpectrum();
}

// 5. Real-Time Continuous Auto-Sync Loop
function initRealtimeAutoSync() {
    const gestureVal = document.getElementById('gesture-value');
    const presenceVal = document.getElementById('presence-value');

    async function syncLiveData() {
        try {
            const res = await fetch('/api/data');
            if (res.ok) {
                const data = await res.json();
                if (data.gesture && gestureVal && isCameraActive) {
                    gestureVal.textContent = data.gesture;
                }
            }
        } catch (err) {
            // Silently ignore if offline
        }
    }

    setInterval(syncLiveData, 1000);
}

// 6. Controls & Video ON/OFF Toggle
function initControls() {
    const btnVideoToggle = document.getElementById('btn-toggle-video');
    const btnMic = document.getElementById('btn-toggle-mic');
    const btnBriefing = document.getElementById('btn-trigger-briefing');
    const btnStop = document.getElementById('btn-stop-audio');
    const transcript = document.getElementById('transcript-content');
    const subtitleText = document.getElementById('subtitle-text');

    // Global bindings for Python bridge
    window.toggleWebcam = toggleWebcam;
    window.addLiveLog = addLiveLog;
    window.updateGesture = (gesture) => {
        const gestureVal = document.getElementById('gesture-value');
        if (gestureVal) {
            gestureVal.textContent = gesture;
            gestureVal.style.color = '#00ff88';
        }
    };
    window.setCameraState = (active) => {
        toggleWebcam(active);
    };
    window.setVoiceState = (state) => {
        window.setJarvisState(state);
    };

    // Video Toggle Event Listener with Python Bridge
    btnVideoToggle.addEventListener('click', async () => {
        await toggleWebcam();
        if (window.pywebview && window.pywebview.api && window.pywebview.api.on_camera_toggled) {
            window.pywebview.api.on_camera_toggled(isCameraActive);
        }
    });

    function getTimeStamp() {
        const d = new Date();
        return d.toTimeString().split(' ')[0];
    }

    function addLiveLog(speaker, text) {
        subtitleText.textContent = `"${text}"`;
        const p = document.createElement('p');
        p.className = speaker === 'JARVIS' ? 'ai-msg' : (speaker === 'SYS' ? 'sys-msg' : 'user-msg');
        p.innerHTML = `<span class="ts">[${getTimeStamp()}]</span> <strong>${speaker}:</strong> ${text}`;
        transcript.appendChild(p);
        transcript.scrollTop = transcript.scrollHeight;
    }

    window.jarvisSpeakText = (text) => {
        window.setJarvisState('speaking');
        addLiveLog('JARVIS', text);

        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'ko-KR';
            utter.onend = () => window.setJarvisState('ready');
            window.speechSynthesis.speak(utter);
        } else {
            setTimeout(() => window.setJarvisState('ready'), 3500);
        }
    };

    btnBriefing.addEventListener('click', () => {
        window.jarvisSpeakText('오늘의 1분 업무 브리핑입니다. 서울 날씨는 대체로 맑고 최고 기온은 29도입니다.');
    });

    let isMicActive = true;
    btnMic.classList.add('active');
    btnMic.textContent = '🎙️ MIC ON';

    btnMic.addEventListener('click', () => {
        isMicActive = !isMicActive;
        if (isMicActive) {
            btnMic.classList.add('active');
            btnMic.textContent = '🎙️ MIC ON';
            window.setJarvisState('listening');
            addLiveLog('SYS', '음성 비서 마이크가 활성화되었습니다.');
        } else {
            btnMic.classList.remove('active');
            btnMic.textContent = '🎙️ MIC OFF';
            window.setJarvisState('ready');
            addLiveLog('SYS', '음성 비서 마이크가 일시정지되었습니다.');
        }
        if (window.pywebview && window.pywebview.api && window.pywebview.api.on_mic_toggled) {
            window.pywebview.api.on_mic_toggled(isMicActive);
        }
    });

    btnStop.addEventListener('click', () => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        window.setJarvisState('ready');
        addLiveLog('JARVIS', '음성 재생이 정지되었습니다.');
    });
}
