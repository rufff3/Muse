// photo-geolocator-01 entry: place each of an instance's 25 street-level photos.
//
// For every photo it asks a vision model once (claude-sonnet-5-5 through the
// trial's gateway) where the photo was taken, with a GeoGuessr-style reasoning
// prompt, reads the latitude/longitude out of the answer, and posts every answer
// to the env at the end. Improvements over the kit starter: a clue-by-clue
// reasoning prompt, a cheap-model fallback when the trial budget runs out, an
// OpenAI fallback when no Anthropic key is present, and a fixed prior guess for
// any photo no model call could place (a guess beats leaving it unanswered,
// which counts the maximum 20,015 km).
//
// It runs as the grader runs an entry, `node /bot/main.ts` on Node 22 (erasable
// TypeScript, the standard library only), with the trial's variables:
// MAKEFUN_ENV_URL (the env), ANTHROPIC_BASE_URL and ANTHROPIC_API_KEY (the
// gateway and the dummy key it swaps for the real one), OPENAI_BASE_URL and
// OPENAI_API_KEY (same for gpt models).
//
// Whose key pays: every call runs on the Anthropic/OpenAI key pushed to the
// competition before submitting (the house pays for none). With no key pushed
// every call is refused and every photo gets the prior guess instead.
//
// Deterministic given the model's answers: every request is a function of the
// photo's bytes and the fixed prompt, the calls run four at a time and their
// answers are posted in photo order, so a replay sends the same calls and
// leaves the same answers. No wall clock and no unseeded randomness anywhere.

const MODEL_PRIMARY = 'claude-sonnet-5-5';
const MODEL_CHEAP = 'claude-haiku-5-5';
const MODEL_OPENAI = 'gpt-6-sol';
const MAX_TOKENS = 1024;
const CONCURRENCY = 4;
const RETRIES = 3;
/** Retried with a fixed backoff: a provider's transient errors. A gateway refusal (4xx) is final. */
const RETRY_STATUSES = [408, 429, 500, 502, 503, 504, 529];
// The trial's $1.00 budget is shared by all 25 photos. A refused call is final.
const GATEWAY_REFUSALS = ['budget_exhausted', 'request_cap', 'model_not_allowed', 'max_tokens_required'];
// Prior guess for a photo no model call could place: near the median of the
// practice pool's places (a single constant, not a table of photos).
const FALLBACK_LAT = 30.0;
const FALLBACK_LON = 20.0;

const PROMPT =
  'You are an expert GeoGuessr player. Work out where this street-level photo was taken. ' +
  'Reason briefly, clue by clue, in a few short lines: (1) language and script on signs, shop names ' +
  'and license plates; (2) which side of the road traffic drives on, road markings and sign shapes ' +
  'and colours; (3) architecture, vegetation, climate and terrain; (4) anything country-specific ' +
  'such as phone codes, domains, flags or plate colours. Then give your best estimate as one line ' +
  'of JSON: {"lat": <degrees north>, "lon": <degrees east>}. Be as precise as the clues allow: ' +
  'prefer a specific town or road over a country centre when you can.';

interface Photo {
  id: string;
  url: string;
  answered: boolean;
}

interface Guess {
  id: string;
  lat: number;
  lon: number;
}

function need(name: string): string {
  const v = process.env[name];
  if (v === undefined || v === '') throw new Error(`${name} is not set`);
  return v;
}

const envUrl = need('MAKEFUN_ENV_URL').replace(/\/+$/, '');
const anthropicUrl = (process.env['ANTHROPIC_BASE_URL'] ?? 'https://api.anthropic.com').replace(/\/+$/, '');
const anthropicKey = process.env['ANTHROPIC_API_KEY'] ?? '';
const openaiUrl = (process.env['OPENAI_BASE_URL'] ?? 'https://api.openai.com/v1').replace(/\/+$/, '');
const openaiKey = process.env['OPENAI_API_KEY'] ?? '';

const sleep = (ms: number): Promise<void> => new Promise((r) => setTimeout(r, ms));

/** The vendor error type of a refused call, when the body names one. */
function errorType(text: string): string | null {
  try {
    const body = JSON.parse(text) as { error?: { type?: unknown; code?: unknown } };
    const e = body.error;
    if (e && typeof e === 'object') {
      if (typeof e.type === 'string') return e.type;
      if (typeof e.code === 'string') return e.code;
    }
  } catch {
    // Not JSON: no type to read.
  }
  return null;
}

class BudgetOut extends Error {}

/** One Anthropic Messages call; the model's answer text, or null. Throws BudgetOut when the gateway refuses for the trial budget. */
async function askAnthropic(jpeg: Buffer, model: string): Promise<string | null> {
  const body = JSON.stringify({
    model,
    max_tokens: MAX_TOKENS,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: jpeg.toString('base64') } },
          { type: 'text', text: PROMPT },
        ],
      },
    ],
  });
  for (let attempt = 0; ; attempt += 1) {
    let res: Response;
    try {
      res = await fetch(`${anthropicUrl}/v1/messages`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-api-key': anthropicKey, 'anthropic-version': '2023-06-01' },
        body,
      });
    } catch {
      if (attempt < RETRIES) {
        await sleep(2000 * (attempt + 1));
        continue;
      }
      return null;
    }
    if (res.ok) {
      const msg = (await res.json()) as { content?: { type: string; text?: string }[] };
      return (msg.content ?? [])
        .filter((b) => b.type === 'text')
        .map((b) => b.text ?? '')
        .join('\n');
    }
    const text = await res.text();
    if (errorType(text) === 'budget_exhausted') throw new BudgetOut('anthropic budget exhausted');
    if (RETRY_STATUSES.includes(res.status) && res.headers.get('x-should-retry') !== 'false' && attempt < RETRIES) {
      await sleep(2000 * (attempt + 1));
      continue;
    }
    process.stderr.write(`geolocator: model call refused (HTTP ${res.status}): ${text.slice(0, 300)}\n`);
    return null;
  }
}

/** One OpenAI Chat Completions call; the model's answer text, or null. */
async function askOpenai(jpeg: Buffer): Promise<string | null> {
  const body = JSON.stringify({
    model: MODEL_OPENAI,
    max_completion_tokens: MAX_TOKENS,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${jpeg.toString('base64')}` } },
          { type: 'text', text: PROMPT },
        ],
      },
    ],
  });
  for (let attempt = 0; ; attempt += 1) {
    let res: Response;
    try {
      res = await fetch(`${openaiUrl}/chat/completions`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'authorization': `Bearer ${openaiKey}` },
        body,
      });
    } catch {
      if (attempt < RETRIES) {
        await sleep(2000 * (attempt + 1));
        continue;
      }
      return null;
    }
    if (res.ok) {
      const msg = (await res.json()) as { choices?: { message?: { content?: unknown } }[] };
      const content = msg.choices?.[0]?.message?.content;
      return typeof content === 'string' ? content : '';
    }
    const text = await res.text();
    if (errorType(text) === 'budget_exhausted') throw new BudgetOut('openai budget exhausted');
    if (RETRY_STATUSES.includes(res.status) && res.headers.get('x-should-retry') !== 'false' && attempt < RETRIES) {
      await sleep(2000 * (attempt + 1));
      continue;
    }
    process.stderr.write(`geolocator: model call refused (HTTP ${res.status}): ${text.slice(0, 300)}\n`);
    return null;
  }
}

const isLat = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v) && v >= -90 && v <= 90;
const isLon = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v) && v >= -180 && v <= 180;

/** The latitude and longitude an answer gives: its first JSON object with lat and lon, else its first two numbers in range. */
function coordinates(text: string): { lat: number; lon: number } | null {
  for (const m of text.matchAll(/\{[^{}]*\}/g)) {
    try {
      const o = JSON.parse(m[0]) as Record<string, unknown>;
      const lat = o.lat ?? o.latitude;
      const lon = o.lon ?? o.lng ?? o.longitude;
      if (isLat(lat) && isLon(lon)) return { lat, lon };
    } catch {
      // Not JSON: the next one, or the numbers below.
    }
  }
  const nums = [...text.matchAll(/-?\d+(?:\.\d+)?/g)].map((m) => Number(m[0]));
  for (let i = 0; i + 1 < nums.length; i += 1) {
    if (isLat(nums[i]) && isLon(nums[i + 1])) return { lat: nums[i]!, lon: nums[i + 1]! };
  }
  return null;
}

// Set once the trial budget is spent, so the remaining photos use the cheap
// model instead of repeating a call the gateway will refuse.
let budgetOut = false;

/** One photo's (lat, lon): the model, or the prior guess when no model call could place it. */
async function placePhoto(photo: Photo): Promise<{ lat: number; lon: number }> {
  let jpeg: Buffer;
  try {
    const res = await fetch(`${envUrl}${photo.url}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    jpeg = Buffer.from(await res.arrayBuffer());
  } catch {
    process.stderr.write(`geolocator: could not fetch ${photo.id}\n`);
    return { lat: FALLBACK_LAT, lon: FALLBACK_LON };
  }
  if (anthropicKey !== '') {
    const model = budgetOut ? MODEL_CHEAP : MODEL_PRIMARY;
    let text: string | null = null;
    try {
      text = await askAnthropic(jpeg, model);
    } catch (err) {
      if (err instanceof BudgetOut) {
        budgetOut = true;
        process.stderr.write(`geolocator: budget out on ${photo.id}; cheap model for the rest\n`);
        text = await askAnthropic(jpeg, MODEL_CHEAP);
      } else {
        throw err;
      }
    }
    if (text !== null) {
      const c = coordinates(text);
      if (c !== null) return c;
      process.stderr.write(`geolocator: no coordinates in the answer for ${photo.id}\n`);
    }
  } else if (openaiKey !== '') {
    // Only when no Anthropic key is present at all: trying the second vendor
    // after the first one failed would double the trial's requests.
    let text: string | null = null;
    try {
      text = await askOpenai(jpeg);
    } catch (err) {
      if (!(err instanceof BudgetOut)) throw err;
    }
    if (text !== null) {
      const c = coordinates(text);
      if (c !== null) return c;
      process.stderr.write(`geolocator: no coordinates in the OpenAI answer for ${photo.id}\n`);
    }
  }
  return { lat: FALLBACK_LAT, lon: FALLBACK_LON };
}

async function main(): Promise<number> {
  const listed = (await (await fetch(`${envUrl}/photos`)).json()) as { photos: Photo[] };
  const photos = listed.photos.filter((p) => !p.answered);
  if (photos.length === 0) return 0;
  const guesses: ({ lat: number; lon: number } | null)[] = new Array(photos.length).fill(null);
  let next = 0;
  const worker = async (): Promise<void> => {
    while (next < photos.length) {
      const i = next;
      next += 1;
      const p = photos[i]!;
      guesses[i] = await placePhoto(p);
    }
  };
  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, photos.length) }, () => worker()));
  const answers: Guess[] = photos.map((p, i) => {
    const g = guesses[i]!;
    return { id: p.id, lat: Math.round(g.lat * 1e6) / 1e6, lon: Math.round(g.lon * 1e6) / 1e6 };
  });
  const res = await fetch(`${envUrl}/answers`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ answers }) });
  process.stdout.write(`geolocator: ${answers.length} of ${photos.length} photos answered: HTTP ${res.status} ${await res.text()}`);
  return res.ok ? 0 : 1;
}

try {
  process.exitCode = await main();
} catch (err) {
  process.stderr.write(`geolocator: ${(err as Error).stack ?? String(err)}\n`);
  process.exitCode = 1;
}
