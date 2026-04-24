import { useEffect, useState } from "react";
import "./App.css";
import DashboardView from "./components/DashboardView.jsx";

const API_BASE_URL = "http://127.0.0.1:8080";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [model, setModel] = useState("v8s");
  const [result, setResult] = useState(null);
  const [videoResult, setVideoResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [activeHistoryItem, setActiveHistoryItem] = useState(null);

  const fetchRecentHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/recent_history?limit=5`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load recent history.");
      }

      setHistory(data.items || []);
    } catch (err) {
      console.error("History error:", err);
    }
  };

  useEffect(() => {
    fetchRecentHistory();
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setActiveHistoryItem(null);
    setResult(null);
    setVideoResult(null);
    setError("");
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreviewUrl("");
    setActiveHistoryItem(null);
    setResult(null);
    setVideoResult(null);
    setError("");
  };

  const handleHistorySelect = (historyItem) => {
    setActiveHistoryItem(historyItem);
    setSelectedFile(null);
    setPreviewUrl("");
    setResult(null);
    setVideoResult(null);
    setError("");
  };

  const handleDetect = async () => {
    if (!selectedFile) {
      setError("Please upload an image or video first.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);
      setVideoResult(null);
      setActiveHistoryItem(null);

      const formData = new FormData();
      formData.append("file", selectedFile);

      const isVideo = selectedFile.type?.startsWith("video/");
      const url = isVideo
        ? `${API_BASE_URL}/predict_video`
        : `${API_BASE_URL}/predict?model=${model}`;

      if (isVideo) {
        formData.append("model", model);
      }

      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Detection failed.");
      }

      if (isVideo) {
        setVideoResult(data);
      } else {
        setResult(data);
      }

      await fetchRecentHistory();
    } catch (err) {
      console.error("Detect error:", err);
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardView
      apiBaseUrl={API_BASE_URL}
      selectedFile={selectedFile}
      previewUrl={previewUrl}
      activeHistoryItem={activeHistoryItem}
      model={model}
      setModel={setModel}
      result={result}
      videoResult={videoResult}
      loading={loading}
      error={error}
      history={history}
      handleFileChange={handleFileChange}
      handleDetect={handleDetect}
      handleClear={handleClear}
      handleHistorySelect={handleHistorySelect}
    />
  );
}

export default App;
