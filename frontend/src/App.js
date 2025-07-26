import React, { useState } from 'react';
import Spline from '@splinetool/react-spline';
import './App.css';

function App() {
  const [emailText, setEmailText] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Use the provided public Spline robot scene URL
  const splineUrl = 'https://prod.spline.design/abrrgNxKZjz-ycx5/scene.splinecode';

  const handleTextChange = (e) => {
    setEmailText(e.target.value);
    setFile(null);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setEmailText('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      let response;
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        response = await fetch('http://127.0.0.1:8000/classify_file', {
          method: 'POST',
          body: formData,
        });
      } else {
        response = await fetch('http://127.0.0.1:8000/classify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: emailText }),
        });
      }
      const data = await response.json();
      if (data.label) {
        setResult(data.label);
      } else {
        setError(data.error || 'Unknown error');
      }
    } catch (err) {
      setError('Failed to classify email.');
    }
    setLoading(false);
  };

  return (
    <div className="guardian-root">
      <div className="guardian-left">
        <h1 className="guardian-title">EMAIL<br/>GUARDIAN</h1>
        <Spline scene={splineUrl} />
      </div>
      <div className="guardian-right">
        <form className="guardian-form" onSubmit={handleSubmit}>
          <label className="guardian-label">
            Enter the text or upload the file of an email to classify:
          </label>
          <textarea
            className="guardian-textarea"
            value={emailText}
            onChange={handleTextChange}
            placeholder="Paste email text here..."
            rows={6}
            disabled={!!file}
          />
          <div className="guardian-or">or</div>
          <input
            className="guardian-file"
            type="file"
            accept=".txt,.eml"
            onChange={handleFileChange}
            disabled={!!emailText}
          />
          <button className="guardian-submit" type="submit" disabled={loading || (!emailText && !file)}>
            {loading ? 'Classifying...' : 'Submit'}
          </button>
        </form>
        {result && (
          <div className="guardian-result">Result: <b>{result.toUpperCase()}</b></div>
        )}
        {error && (
          <div className="guardian-error">{error}</div>
        )}
      </div>
    </div>
  );
}

export default App;
