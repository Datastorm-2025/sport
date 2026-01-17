# Hướng dẫn Chạy trên Linux

## Mục lục

- [Cài đặt Docker](#cài-đặt-docker)
- [Cấu hình Docker](#cấu-hình-docker)
- [Build Image](#build-image)
- [Validate & Push](#validate--push)
- [Cách BTC chạy Image](#cách-btc-chạy-image)

---

## Cài đặt Docker

Tải và cài đặt Docker theo hướng dẫn tại: <https://docs.docker.com/get-started/get-docker/>

Kiểm tra phiên bản Docker đã cài đặt:

```bash
sudo docker --version
```

Kiểm tra trạng thái Docker service:

```bash
sudo systemctl status docker
```

Kiểm tra các container đang chạy:

```bash
docker ps
```

Khởi động Docker service (nếu chưa chạy):

```bash
sudo systemctl start docker
```

---

## Cấu hình Docker

### 1. Clone Repository

```bash
git clone <>

cd sport
```

### 2. Cấu hình Docker Daemon

Mở file cấu hình Docker:

```bash
sudo nano /etc/docker/daemon.json
```

Thêm nội dung sau vào file:

```json
{
  "runtimes": {
    "nvidia": {
      "args": [],
      "path": "nvidia-container-runtime"
    }
  },
  "insecure-registries": ["222.255.250.24:8002"], // Thêm domain vào
  "max-concurrent-uploads": 1
}
```

> **Lưu ý:**
> - `insecure-registries`: Thêm domain registry của BTC
> - `max-concurrent-uploads`: Đặt bằng 1 để tránh tràn RAM khi push

### 3. Khởi động lại Docker

```bash
sudo systemctl restart docker
```

### 4. Đăng nhập Registry

```bash
docker login DOMA222.255.250.24:8002 -u <team_id>
```

> **Lưu ý:** Sử dụng tài khoản được BTC cung cấp để đăng nhập.

---

## Build Image

Build Docker image với cache từ base image:

```bash
docker build   --cache-from 222.255.250.24:8001/data-storm/pytorch:2.8.0-cuda12.8-cudnn9-devel \
-t DOMAIN/TEAM_ID/submission .
```

> **Lưu ý:** Sử dụng thẻ `--cache-from` tối ưu hoá tốc độ push bài.

---

## Validate & Push

### Validate Submission

Chạy script kiểm tra bài nộp trước khi push:

```bash
bash validate_submission.sh
```

### Push Image

```bash
docker push 222.255.250.24:8002/<team_id>/submission
```

---

## Cách BTC Chạy Image

Đoạn code mà Ban tổ chức sẽ sử dụng để chạy image của thí sinh:

```bash
docker run --rm --network none --gpus '"device=1"' \
  -v /path/to/input:/data/input:ro \
  -v /path/to/results:/data/output \
  -e INPUT_PATH=/data/input \
  -e OUTPUT_PATH=/data/output \
  DOMAIN/your_team/submission
```

| Tham số | Mô tả |
|---------|-------|
| `--rm` | Tự động xóa container sau khi chạy xong |
| `--network none` | Tắt kết nối mạng |
| `--gpus '"device=1"'` | Sử dụng GPU device 1 |
| `-v /path/to/input:/data/input:ro` | Mount thư mục input (read-only) |
| `-v /path/to/results:/data/output` | Mount thư mục output |
| `-e INPUT_PATH` | Biến môi trường đường dẫn input |
| `-e OUTPUT_PATH` | Biến môi trường đường dẫn output |