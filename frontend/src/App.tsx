import { useState } from "react";
import { generatePoem } from "./api";
import "./styles.css";

export default function App() {
  const [title, setTitle] = useState("Sub cerul plin de stele");
  const [loading, setLoading] = useState(false);
  const [device, setDevice] = useState<string>("");
  const [text, setText] = useState<string>("");
  const [error, setError] = useState<string>("");

  // Minimal controls; expand later
  const [maxNewTokens, setMaxNewTokens] = useState(200);
  const [temperature, setTemperature] = useState(0.8);
  const [topP, setTopP] = useState(0.95);
  const [useTitleToken, setUseTitleToken] = useState(true);

  async function onGenerate() {
    setLoading(true);
    setError("");
    try {
      const resp = await generatePoem({
        title,
        max_new_tokens: maxNewTokens,
        do_sample: true,
        temperature,
        top_p: topP,
        top_k: 50,
        repetition_penalty: 1.1,
        no_repeat_ngram_size: 3,
        use_title_token: useTitleToken,
      });
      setText(resp.text);
      setDevice(resp.device);
    } catch (e: any) {
      setError(e?.message ?? String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="hero">
        <img
          src="/nichita.jpg"
          alt="Nichita Stănescu"
          className="hero-img"
        />
        <div>
          <h1>Nichita Stănescu's Poem Generator</h1>
          <p className="subtitle">
            A fine-tuned RoGPT-2 model inspired by the poetry of Nichita Stănescu
          </p>
        </div>
      </header>

      <div className="card">
        <label className="label">Title</label>
        <input
          className="input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g. Poetul si soldatul"
        />

        <div className="row">
          <div>
            <label className="label">max_new_tokens</label>
            <input
              className="input"
              type="number"
              value={maxNewTokens}
              min={16}
              max={512}
              onChange={(e) => setMaxNewTokens(Number(e.target.value))}
            />
          </div>

          <div>
            <label className="label">temperature</label>
            <input
              className="input"
              type="number"
              step="0.05"
              value={temperature}
              min={0.1}
              max={2.0}
              onChange={(e) => setTemperature(Number(e.target.value))}
            />
          </div>

          <div>
            <label className="label">top_p</label>
            <input
              className="input"
              type="number"
              step="0.01"
              value={topP}
              min={0.1}
              max={1.0}
              onChange={(e) => setTopP(Number(e.target.value))}
            />
          </div>
        </div>


        <button className="btn" onClick={onGenerate} disabled={loading || !title.trim()}>
          {loading ? "Generating..." : "Generate"}
        </button>

        {error && <pre className="error">{error}</pre>}
        {device && <div className="meta">Backend device: {device}</div>}
      </div>

      <div className="card">
        <label className="label">Output</label>
        <div className="paper">
          <div className="poem">
            {text ? text : <span className="placeholder">No poem generated yet.</span>}
          </div>
        </div>
      </div>
    </div>
  );
}
