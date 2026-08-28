import { useState } from 'react'
import { SelectField, NumberField } from './FormField.jsx'
import {
  AIRLINES,
  AIRPORTS,
  MONTHS,
  DAYS_OF_WEEK,
  HOURS,
} from '../constants/options.js'
import './PredictionForm.css'

const LIMITS = {
  distance: { min: 50, max: 6000 },
  temperature_f: { min: -40, max: 130 },
  wind_speed_mph: { min: 0, max: 120 },
  precipitation_in: { min: 0, max: 15 },
  visibility_miles: { min: 0, max: 10 },
}

function validate(form) {
  const errors = {}

  if (form.origin === form.dest) {
    errors.dest = 'Destination must differ from origin.'
  }

  for (const key of Object.keys(LIMITS)) {
    const { min, max } = LIMITS[key]
    const value = Number(form[key])
    if (Number.isNaN(value)) {
      errors[key] = 'Required.'
    } else if (value < min || value > max) {
      errors[key] = `Must be between ${min} and ${max}.`
    }
  }

  return errors
}

export default function PredictionForm({ formData, onChange, onSubmit, loading }) {
  const [errors, setErrors] = useState({})
  const [touched, setTouched] = useState(false)

  function handleField(name, rawValue) {
    onChange({ ...formData, [name]: rawValue })
    if (touched) {
      setErrors(validate({ ...formData, [name]: rawValue }))
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    setTouched(true)
    const validationErrors = validate(formData)
    setErrors(validationErrors)
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(formData)
    }
  }

  return (
    <form className="pred-form" onSubmit={handleSubmit} noValidate>
      <div className="pred-form__section">
        <span className="pred-form__section-label">FLIGHT</span>
        <div className="pred-form__grid pred-form__grid--2">
          <SelectField
            label="Airline"
            name="airline"
            value={formData.airline}
            onChange={(v) => handleField('airline', v)}
            options={AIRLINES}
          />
          <NumberField
            label="Distance"
            unit="miles"
            name="distance"
            value={formData.distance}
            min={LIMITS.distance.min}
            max={LIMITS.distance.max}
            onChange={(v) => handleField('distance', v)}
            error={errors.distance}
          />
        </div>
      </div>

      <div className="pred-form__section">
        <span className="pred-form__section-label">ROUTE</span>
        <div className="pred-form__grid pred-form__grid--2">
          <SelectField
            label="Origin"
            name="origin"
            value={formData.origin}
            onChange={(v) => handleField('origin', v)}
            options={AIRPORTS}
          />
          <SelectField
            label="Destination"
            name="dest"
            value={formData.dest}
            onChange={(v) => handleField('dest', v)}
            options={AIRPORTS}
            error={errors.dest}
          />
        </div>
      </div>

      <div className="pred-form__section">
        <span className="pred-form__section-label">SCHEDULE</span>
        <div className="pred-form__grid pred-form__grid--3">
          <SelectField
            label="Month"
            name="month"
            value={formData.month}
            onChange={(v) => handleField('month', Number(v))}
            options={MONTHS}
          />
          <SelectField
            label="Day of week"
            name="day_of_week"
            value={formData.day_of_week}
            onChange={(v) => handleField('day_of_week', Number(v))}
            options={DAYS_OF_WEEK}
          />
          <SelectField
            label="Departure time"
            name="sched_dep_hour"
            value={formData.sched_dep_hour}
            onChange={(v) => handleField('sched_dep_hour', Number(v))}
            options={HOURS}
          />
        </div>
      </div>

      <div className="pred-form__section">
        <span className="pred-form__section-label">WEATHER AT DEPARTURE</span>
        <div className="pred-form__grid pred-form__grid--4">
          <NumberField
            label="Temperature"
            unit="°F"
            name="temperature_f"
            value={formData.temperature_f}
            min={LIMITS.temperature_f.min}
            max={LIMITS.temperature_f.max}
            onChange={(v) => handleField('temperature_f', v)}
            error={errors.temperature_f}
          />
          <NumberField
            label="Wind speed"
            unit="mph"
            name="wind_speed_mph"
            value={formData.wind_speed_mph}
            min={LIMITS.wind_speed_mph.min}
            max={LIMITS.wind_speed_mph.max}
            onChange={(v) => handleField('wind_speed_mph', v)}
            error={errors.wind_speed_mph}
          />
          <NumberField
            label="Precipitation"
            unit="in"
            name="precipitation_in"
            value={formData.precipitation_in}
            min={LIMITS.precipitation_in.min}
            max={LIMITS.precipitation_in.max}
            step={0.01}
            onChange={(v) => handleField('precipitation_in', v)}
            error={errors.precipitation_in}
          />
          <NumberField
            label="Visibility"
            unit="miles"
            name="visibility_miles"
            value={formData.visibility_miles}
            min={LIMITS.visibility_miles.min}
            max={LIMITS.visibility_miles.max}
            step={0.1}
            onChange={(v) => handleField('visibility_miles', v)}
            error={errors.visibility_miles}
          />
        </div>
      </div>

      <button type="submit" className="pred-form__submit" disabled={loading}>
        {loading ? (
          <>
            <span className="pred-form__spinner" aria-hidden="true" />
            RUNNING MODEL&hellip;
          </>
        ) : (
          'PREDICT DELAY'
        )}
      </button>
    </form>
  )
}
