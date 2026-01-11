export type GenerateRequest = {
  title: string;
  max_new_tokens?: number;
  do_sample?: boolean;
  temperature?: number;
  top_p?: number;
  top_k?: number;
  repetition_penalty?: number;
  no_repeat_ngram_size?: number;
  use_title_token?: boolean;
};

export type GenerateResponse = {
  prompt: string;
  text: string;
  device: string;
};

const API_BASE = "http://localhost:8000";

export async function generatePoem(req: GenerateRequest): Promise<GenerateResponse> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || `HTTP ${res.status}`);
  }

  return res.json();
}
