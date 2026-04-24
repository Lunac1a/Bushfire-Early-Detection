import { useMemo } from "react";

function DashboardView({
  apiBaseUrl,
  selectedFile,
  previewUrl,
  activeHistoryItem,
  model,
  setModel,
  result,
  videoResult,
  loading,
  error,
  history,
  handleFileChange,
  handleDetect,
  handleClear,
  handleHistorySelect,
}) {
  const displayedResult = activeHistoryItem?.result_data || videoResult || result;

  const topLabel = (() => {
    if (!displayedResult?.summary) return "No detection";

    if (displayedResult.summary.fire_count > 0) return "fire";
    if (displayedResult.summary.smoke_count > 0) return "smoke";
    return "No detection";
  })();

  const topLabelClassName =
    topLabel === "fire"
      ? "top-label-fire"
      : topLabel === "smoke"
        ? "top-label-smoke"
        : "top-label-safe";

  const riskClassName = displayedResult?.risk_level ? `risk-${displayedResult.risk_level}` : "";

  const currentPreview = useMemo(() => {
    if (activeHistoryItem) {
      return {
        src: `${apiBaseUrl}${activeHistoryItem.url}`,
        mediaType: activeHistoryItem.media_type,
        isHistory: true,
        name: activeHistoryItem.filename,
      };
    }

    if (selectedFile?.type?.startsWith("video/")) {
      return {
        src: videoResult ? `${apiBaseUrl}${videoResult.output_video_url}` : previewUrl,
        mediaType: "video",
        isHistory: false,
        name: selectedFile.name,
      };
    }

    if (result?.output_image_url) {
      return {
        src: `${apiBaseUrl}${result.output_image_url}`,
        mediaType: "image",
        isHistory: false,
        name: selectedFile?.name || result.filename,
      };
    }

    if (previewUrl) {
      return {
        src: previewUrl,
        mediaType: "image",
        isHistory: false,
        name: selectedFile?.name || "Preview",
      };
    }

    return null;
  }, [activeHistoryItem, apiBaseUrl, previewUrl, result, selectedFile, videoResult]);

  return (
    <div className="app">
      <header className="header">
        <div className="header-copy">
          <h1>Bushfire Smoke Detection Dashboard</h1>
          <p>A CNN Based Bushfire Smoke Detection AI</p>
        </div>
      </header>

      <main className="main-layout">
        <aside className="card sidebar">
          <h2>Controls</h2>

          <label className="label">Model</label>
          <select value={model} onChange={(e) => setModel(e.target.value)}>
            <option value="v8n">YOLOv8n</option>
            <option value="v8s">YOLOv8s</option>
          </select>

          <label className="upload-box">
            <input
              type="file"
              accept="image/*, video/*"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />

            <div className="upload-content">
              {selectedFile ? (
                <span>{selectedFile.name}</span>
              ) : (
                <span>Click to upload image / video</span>
              )}
            </div>
          </label>

          <button className="primary-btn" onClick={handleDetect} disabled={loading}>
            {loading ? "Detecting..." : "Detect"}
          </button>

          <button className="secondary-btn" onClick={handleClear} disabled={loading}>
            Clear
          </button>

          {(selectedFile || activeHistoryItem) && (
            <div className="info-item">
              <span className="label">File</span>
            <span className="value">{selectedFile?.name || activeHistoryItem?.filename}</span>
          </div>
          )}

          {error && (
            <div className="info-item">
              <span className="label">Error</span>
              <span className="value">{error}</span>
            </div>
          )}
        </aside>

        <section className="card">
          <div className="panel-header">
            <h2>Preview</h2>
            {currentPreview && (
              <span className="preview-chip">
                {currentPreview.isHistory ? "Saved output" : "Current run"}
              </span>
            )}
          </div>

          <div className="image-box" style={{ position: "relative" }}>
            {currentPreview ? (
              currentPreview.mediaType === "video" ? (
                <video
                  key={currentPreview.src}
                  src={currentPreview.src}
                  controls
                  preload="metadata"
                  style={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    borderRadius: "12px",
                  }}
                />
              ) : (
                <img
                  key={currentPreview.src}
                  src={currentPreview.src}
                  alt="Preview"
                  style={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain",
                    borderRadius: "12px",
                  }}
                />
              )
            ) : (
              <span>Image or video goes here</span>
            )}
          </div>
        </section>

        <aside className="card info-panel">
          <h2>Detection Result</h2>

          <div className="info-item">
            <span className="label">Model</span>
            <span className="value">{displayedResult?.model_used || model}</span>
          </div>

          <div className="info-item">
            <span className="label">Top Label</span>
            <span className={`value ${topLabelClassName}`}>{topLabel}</span>
          </div>

          <div className="info-item">
            <span className="label">Smoke Count</span>
            <span className="value">{displayedResult?.summary?.smoke_count ?? "-"}</span>
          </div>

          <div className="info-item">
            <span className="label">Fire Count</span>
            <span className="value">{displayedResult?.summary?.fire_count ?? "-"}</span>
          </div>

          <div className="info-item">
            <span className="label">Max Confidence</span>
            <span className="value">{displayedResult?.summary?.max_confidence ?? displayedResult?.max_confidence ?? "-"}</span>
          </div>

          <div className="info-item">
            <span className="label">Risk</span>
            <span className={`value ${riskClassName}`}>{displayedResult?.risk_level || "-"}</span>
          </div>

          <div className="info-item">
            <span className="label">Detected Frames</span>
            <span className="value">{displayedResult?.detected_frames ?? "-"}</span>
          </div>
        </aside>
      </main>

      <section className="card history-card">
        <div className="panel-header">
          <h2>Recent History</h2>
          <span className="history-caption">Latest 5 files from static output</span>
        </div>

        {history.length > 0 ? (
          <div className="history-list">
            <div className="history-head">
              <span>Filename</span>
              <span>Type</span>
              <span>Risk</span>
            </div>
            {history.map((item) => {
              const isActive = activeHistoryItem?.url === item.url;
              return (
                <button
                  key={item.url}
                  type="button"
                  className={`history-row ${isActive ? "history-row-active" : ""}`}
                  onClick={() => handleHistorySelect(item)}
                >
                  <span>{item.filename}</span>
                  <span>{item.media_type}</span>
                  <span>{item.result_data?.risk_level || "Preview"}</span>
                </button>
              );
            })}
          </div>
        ) : (
          <div className="history-empty">No processed files yet.</div>
        )}
      </section>
    </div>
  );
}

export default DashboardView;
