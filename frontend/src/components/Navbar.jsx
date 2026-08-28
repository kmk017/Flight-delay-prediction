import './Navbar.css'

function PlaneMark() {
  return (
    <svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true">
      <path
        d="M16 3 L18.4 12.8 L28 15.5 L18.4 16.9 L17 25.5 L16 29.5 L15 25.5 L13.6 16.9 L4 15.5 L13.6 12.8 Z"
        fill="var(--amber)"
      />
    </svg>
  )
}

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar__inner">
        <div className="navbar__brand">
          <PlaneMark />
          <span className="navbar__title">FLIGHT&nbsp;DELAY&nbsp;PREDICTOR</span>
        </div>
        <div className="navbar__meta">
          <span className="navbar__badge">
            <span className="navbar__dot" aria-hidden="true" />
            ML MODEL ONLINE
          </span>
        </div>
      </div>
    </header>
  )
}
