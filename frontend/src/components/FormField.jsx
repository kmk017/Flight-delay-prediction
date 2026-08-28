import './FormField.css'

export function SelectField({ label, unit, value, onChange, options, error, name }) {
  return (
    <label className="field">
      <span className="field__label">
        {label} {unit && <span className="field__unit">({unit})</span>}
      </span>
      <select
        name={name}
        className={`field__control ${error ? 'field__control--error' : ''}`}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {options.map((opt) => (
          <option key={opt.value ?? opt.code} value={opt.value ?? opt.code}>
            {opt.label ?? `${opt.code} — ${opt.name}`}
          </option>
        ))}
      </select>
      {error && <span className="field__error">{error}</span>}
    </label>
  )
}

export function NumberField({
  label,
  unit,
  value,
  onChange,
  min,
  max,
  step = 1,
  error,
  name,
}) {
  return (
    <label className="field">
      <span className="field__label">
        {label} {unit && <span className="field__unit">({unit})</span>}
      </span>
      <input
        type="number"
        name={name}
        className={`field__control ${error ? 'field__control--error' : ''}`}
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={(e) => onChange(e.target.value)}
      />
      {error && <span className="field__error">{error}</span>}
    </label>
  )
}
