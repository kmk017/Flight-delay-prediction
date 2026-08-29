const API_URL = 'https://flight-delay-prediction-o1to.onrender.com/predict'

/**
 * Sends flight + weather details to the Flask backend and returns the
 * prediction. Throws a descriptive Error on network failure or non-OK
 * response so the UI can render a clear error state.
 */
export async function predictDelay(payload) {
  let response

  try {
    response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (err) {
    throw new Error(
      'Could not reach the prediction server. Please try again in a moment.'
    )
  }

  if (!response.ok) {
    let detail = ''

    try {
      const body = await response.json()
      detail = body?.error || body?.message || ''
    } catch {
      // response wasn't JSON — ignore
    }

    throw new Error(
      detail || `Prediction request failed (status ${response.status}).`
    )
  }

  return response.json()
}