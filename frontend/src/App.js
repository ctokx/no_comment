import React, { useState } from "react";
import "./App.css";
import ThreeDBackground from "./ThreeDBackground";
function App() {
  const [file, setFile] = useState(null);
  const [language, setLanguage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file || !language) {
      alert("Please select a file and a language.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = downloadUrl;
        link.setAttribute("download", "processed.zip");
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
      } else {
        alert("Upload failed.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error sending file.");
    }
  };

  return (
    <div className="App">
      <ThreeDBackground isRunning={false} />
      <h1
        style={{
          zIndex: 999,
          position: "absolute",
          top: "20px",
          color: "white",
        }}
      >
        &lt;h1&gt; no_comment &lt;/h1&gt;
      </h1>
      <div className="content">
        <form onSubmit={handleSubmit} className="upload-form">
          <div>
            <input type="file" onChange={handleFileChange} />
          </div>
          <div>
            <select value={language} onChange={handleLanguageChange}>
              <option value="">Select Language</option>
              <option value="c">C</option>
              <option value="c++">C++</option>
              <option value="java">Java</option>
              <option value="javascript">JavaScript</option>
              <option value="python">Python</option>
            </select>
          </div>
          <button type="submit">Remove Comments</button>
        </form>
      </div>
    </div>
  );
}

export default App;
