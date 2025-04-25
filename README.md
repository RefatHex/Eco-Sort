# ♻️ Eco-Sort

**Eco-Sort** is a smart waste classification system that leverages AI to detect and categorize waste materials in real-time. It combines a YOLOv8 object detection model with a TypeScript-based web interface to enable intelligent, automated waste sorting.


🔗 **Live Demo:** [Visit Eco-Sort](https://ecosortbin.netlify.app/)

## 🧠 Key Features

- Real-time object detection using YOLOv8
- Live webcam integration for instant classification
- React-based interactive dashboard
- Flask backend with optimized inference API
- Modular design for IoT/robotic integration

## 🚀 Tech Stack

| Layer       | Technology                     |
|------------|---------------------------------|
| Frontend   | React (TypeScript), TailwindCSS |
| Backend    | Flask (Python), OpenCV, YOLOv8  |
| Model      | Ultralytics YOLOv8              |
| Dev Tools  | Vite, pipenv, npm               |

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RefatHex/Eco-Sort.git
cd Eco-Sort
```

### 2. Backend Setup

```bash
cd backend
pipenv install
pipenv run python main.py
```

> Flask server will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

> Frontend app will run on `http://localhost:5173`

## 📷 How It Works

1. User captures a waste item via webcam or uploads an image.
2. Image is sent to the backend for classification.
3. YOLOv8 detects the object(s) and returns category labels.
4. Frontend displays the result and triggers corresponding logic (e.g., sorting bin activation).

## 📡 API Usage

**Endpoint:** `/predict`  
**Method:** `POST`  
**Content-Type:** `multipart/form-data`  
**Field:** `file=<image>`

**Sample Response:**
```json
{
  "detected": ["plastic", "paper"],
  "confidence": [0.92, 0.78]
}
```

## 📈 Roadmap

- Add physical sorting arm control
- Dashboard analytics and history tracking
- Multi-language support
- Docker integration for deployment

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.

## 📄 License

Licensed under the [MIT License](LICENSE).
