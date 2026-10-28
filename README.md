# Cosmos 🌌

**Cosmos** is an open-source, cinematic 3D universe visualizer for Linux. It shows a luminous primordial core, an expanding field of cosmic particles, and a deep starfield. Low, mid, and high frequencies from your system audio influence the expansion, motion, and glow in real time.

Cosmos is an artistic visualization inspired by the Big Bang, not a scientific cosmology simulator.

## Features in the MVP

- Real-time 3D particle field and animated central glow
- Best-effort capture of desktop output through the default PulseAudio/PipeWire monitor
- Responsive low-, mid-, and high-frequency bands
- Runs in an idle animated mode if audio loopback is unavailable
- Fullscreen, pause, and quit controls

## Requirements

- Linux Mint (other Linux desktops may work)
- Python 3.10 or newer (developed with Python 3.12)
- A working OpenGL-capable graphics driver
- PulseAudio or PipeWire with PulseAudio compatibility for system-audio capture

## Install and run

Open a terminal in this directory and install the system packages needed for a Python virtual environment and audio bindings:

```bash
sudo apt update
sudo apt install python3-venv python3-dev libpulse0 libasound2
```

Create an isolated environment, install Cosmos, and launch it:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
cosmos
```

Use `cosmos --fullscreen` to start fullscreen. You can also run `python -m cosmos.app` from the activated environment.

### Controls

- **Space** — pause/resume animation
- **F** — toggle fullscreen
- **Esc** — quit

### Audio capture

Cosmos listens to the default system output monitor; you do not need to select a music file. Start playing audio before or after launching the visualizer. The capture backend depends on your Linux audio setup and permissions. If the status line reports that loopback audio is unavailable, the visual animation still runs; check that PulseAudio/PipeWire is active and exposes an output monitor.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m cosmos.app
```

Contributions are welcome. Please open an issue to discuss large changes, then submit a focused pull request with a clear description, reproduction steps for bug fixes, and screenshots or a short recording for visual changes. Keep dependencies minimal and document Linux audio compatibility changes.

## License

Cosmos is licensed under the [MIT License](LICENSE). MIT is a permissive choice that lets people use, modify, and redistribute the project, including in commercial projects, while retaining the copyright and license notice. Choose a different license before the first public release if you want stronger copyleft requirements.

---

# Cosmos (Türkçe)

**Cosmos**, Linux için açık kaynaklı, sinematik bir 3B evren görselleştiricisidir. Parlak bir başlangıç noktası, genişleyen kozmik parçacıklar ve yıldızlarla dolu bir uzay gösterir. Sistem sesindeki bas, orta ve tiz frekanslar genişlemeyi, parçacık hareketini ve parıltıyı gerçek zamanlı etkiler.

Cosmos, Büyük Patlama'dan esinlenen sanatsal bir görselleştirmedir; bilimsel bir kozmoloji simülatörü değildir.

## MVP özellikleri

- Gerçek zamanlı 3B parçacık alanı ve animasyonlu merkezî ışık
- Masaüstü sesini varsayılan PulseAudio/PipeWire monitöründen yakalama denemesi
- Bas, orta ve tiz frekanslara duyarlı görsel tepki
- Ses yakalama kullanılamazsa animasyon sessiz modda devam eder
- Tam ekran, duraklatma ve çıkış kontrolleri

## Gereksinimler

- Linux Mint (diğer Linux masaüstlerinde de çalışabilir)
- Python 3.10 veya üzeri (Python 3.12 ile geliştiriliyor)
- OpenGL destekli grafik sürücüsü
- Sistem sesini yakalamak için PulseAudio veya PulseAudio uyumluluk katmanına sahip PipeWire

## Kurulum ve çalıştırma

Bu klasörde terminal açıp sanal ortam ve ses bağlantıları için gerekli sistem paketlerini kurun:

```bash
sudo apt update
sudo apt install python3-venv python3-dev libpulse0 libasound2
```

Sanal ortam oluşturun, Cosmos'u yükleyin ve başlatın:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
cosmos
```

Tam ekran başlatmak için `cosmos --fullscreen` komutunu kullanın. Uygulamayı çalıştırmadan önce veya sonra müzik açabilirsiniz; Cosmos sistem çıkışını dinlemeyi dener.

### Kontroller

- **Boşluk** — animasyonu duraklat/devam ettir
- **F** — tam ekranı aç/kapat
- **Esc** — çıkış

Ses durum satırında döngüsel yakalamanın kullanılamadığı yazarsa görsel animasyon çalışmaya devam eder. PulseAudio/PipeWire servisinin açık ve çıkış monitörünün görünür olduğunu kontrol edin.

## Katkı

Katkılarınızı memnuniyetle karşılıyoruz. Büyük değişiklikleri önce bir issue üzerinden konuşun; ardından kapsamı net bir pull request açın. Hata düzeltmelerinde yeniden üretme adımlarını, görsel değişikliklerde ekran görüntüsü veya kısa kayıt ekleyin. Bağımlılıkları sınırlı tutun ve Linux ses uyumluluğu değişikliklerini belgeleyin.

## Lisans

Cosmos [MIT Lisansı](LICENSE) ile lisanslanmıştır. MIT; kullanım, değiştirme ve yeniden dağıtım için geniş izin verir ve telif/lisans bildirimlerinin korunmasını şart koşar. Daha güçlü copyleft koşulları isteniyorsa ilk herkese açık yayından önce lisans tercihini değiştirin.
