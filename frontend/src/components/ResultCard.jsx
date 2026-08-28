import { useEffect, useRef, useState } from 'react'
import './ResultCard.css'

function useCountUp(target, active) {
  const [value, setValue] = useState(0)
  const frame = useRef(null)

  useEffect(() => {
    if (!active) {
      setValue(0)
      return
    }
    const duration = 700
    const start = performance.now()

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(target * eased)
      if (progress < 1) {
        frame.current = requestAnimationFrame(tick)
      } else {
        setValue(target)
      }
    }

    frame.current = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame.current)
  }, [target, active])

  return value
}

export default function ResultCard({ status, result, errorMessage }) {
  const isDelayed = result?.delayed === 1
  const probability = result?.delay_probability ?? 0
  const animatedProbability = useCountUp(probability, status === 'success')

  return (
    <div className="result-card" data-status={status}>
      {status === 'idle' && (
        <div className="result-card__idle">
          <span className="result-card__idle-glyph" aria-hidden="true">
            ✈
          </span>
          <p>Fill in the flight details and run the model to see a prediction.</p>
        </div>
      )}

      {status === 'loading' && (
        <div className="result-card__loading">
          <div className="result-card__bars" aria-hidden="true">
            <span />
            <span />
            <span />
            <span />
          </div>
          <p>Scoring flight against the trained model&hellip;</p>
        </div>
      )}

      {status === 'error' && (
        <div className="result-card__error" role="alert">
          <span className="result-card__error-title">PREDICTION UNAVAILABLE</span>
          <p>{errorMessage}</p>
        </div>
      )}

      {status === 'success' && result && (
        <div className={`result-card__board ${isDelayed ? 'is-delayed' : 'is-ontime'}`}>
          <div className="result-card__flap">
            <span className="result-card__flap-label">STATUS</span>
            <span className="result-card__flap-value">
              {isDelayed ? 'DELAYED' : 'ON TIME'}
            </span>
          </div>
          <div className="result-card__divider" aria-hidden="true" />
          <div className="result-card__probability">
            <span className="result-card__flap-label">DELAY PROBABILITY</span>
            <span className="result-card__probability-value">
              {animatedProbability.toFixed(1)}
              <span className="result-card__percent">%</span>
            </span>
            <div className="result-card__track">
              <div
                className="result-card__fill"
                style={{ width: `${Math.min(animatedProbability, 100)}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
