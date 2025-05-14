# 🔊 Remote Volume Control Project – PC ↔ Mobile App

## 📘 Project Objective

Design and implement a system that allows a user to control the **system volume on a Windows PC** from a **mobile Android device** over a local network, using Python for both server and client-side logic.

---

## ⚙️ System Architecture

### 🖥️ Server (Windows PC)
- **Language**: Python 3.10
- **Key Library**: `pycaw`
- **Features**:
  - Listens for TCP commands (`VOLUME_UP`, `VOLUME_DOWN`)
  - Responds to UDP discovery requests from clients
  - Controls the Windows system volume via `pycaw`

### 📱 Client (Mobile App)
- **Framework**: Kivy (Python)
- **Features**:
  - Sends TCP commands to the server
  - Uses UDP broadcast to auto-discover the server IP
  - Touch interface with volume up/down buttons

---

## 🐞 Challenges Encountered

- ❌ `distutils` module missing in Python 3.12 → resolved by using Python 3.10
- ❌ `cython` not found in `$PATH` during build process
- ⚠️ `pip` blocked under Debian-based systems due to "externally-managed-environment"
- ⚠️ WSL-mounted Windows directories (`/mnt/...`) caused incompatibility with virtual environments
- ⚠️ Android SDK/NDK partially downloaded, leading to `buildozer` errors

---

## ✅ Final Status

- ✅ Server fully functional and reacts to client commands
- ✅ Kivy client tested on desktop, network communication verified
- ❌ APK was **not compiled** due to `buildozer` environment issues
- ✅ Project architecture and logic fully documented and reproducible

---

## 💡 Lessons Learned

- Buildozer works best with **Python 3.10** and within **native Linux directories** (not `/mnt`)
- Avoid developing Android apps using **Debian 12+** or Python 3.12 due to tight `pip` restrictions
- Always isolate environments with `venv` and use dedicated folders for compilation
- A simple TCP/UDP client-server architecture is powerful enough for IoT-style volume control

---

## ✅ Conclusion

This project demonstrates that it is absolutely possible to build a **real-time, cross-device volume control system** using Python. While compilation to `.apk` was not completed, the logic, communication model, and codebase are solid, providing a strong foundation for future development or deployment.

---

