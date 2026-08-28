import { useState } from 'react'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import PredictionForm from './components/PredictionForm.jsx'
import ResultCard from './components/ResultCard.jsx'
import { predictDelay } from './api/predict.js'
import { DEFAULT_FORM } from './constants/options.js'
import './App.css'

export default function App() {
  const [formData, setFormData] = useState(DEFAULT_FORM)
  const [status, setStatus] = useState('idle') // idle | loading | success | error
  const [result, setResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState('')

  async function handleSubmit(values) {
    setStatus('loading')
    setErrorMessage('')

    // Build the exact payload contract expected by the Flask API —
    // numeric fields are coerced since <input type="number"> can emit strings.
    const payload = {
      airline: values.airline,
      origin: values.origin,
      dest: values.dest,
      month: Number(values.month),
      sched_dep_hour: Number(values.sched_dep_hour),
      distance: Number(values.distance),
      temperature_f: Number(values.temperature_f),
      wind_speed_mph: Number(values.wind_speed_mph),
      precipitation_in: Number(values.precipitation_in),
      visibility_miles: Number(values.visibility_miles),
      day_of_week: Number(values.day_of_week),
    }

    try {
      const data = await predictDelay(payload)
      setResult(data)
      setStatus('success')
    } catch (err) {
      setErrorMessage(err.message)
      setStatus('error')
    }
  }

  return (
    <>
      <Navbar />
      <main className="app-main">
        <Hero />
        <section className="console">
          <div className="console__panel console__panel--form">
            <h2 className="console__heading">FLIGHT PLAN</h2>
            <PredictionForm
              formData={formData}
              onChange={setFormData}
              onSubmit={handleSubmit}
              loading={status === 'loading'}
            />
          </div>
          <div className="console__panel console__panel--result">
            <h2 className="console__heading">PREDICTION</h2>
            <ResultCard status={status} result={result} errorMessage={errorMessage} />
          </div>
        </section>
      </main>
      <footer className="app-footer">
        <span>Flight Delay Predictor &mdash; ML portfolio project</span>
        <span className="app-footer__dim">Final model: Tuned Logistic Regression</span>
      </footer>
    </>
  )
}
