import './Hero.css'

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero__radar" aria-hidden="true">
        <div className="hero__radar-rings" />
        <div className="hero__radar-sweep" />
      </div>
      <div className="hero__content">
        <span className="hero__eyebrow">MACHINE LEARNING &middot; PREDICTIVE ANALYTICS</span>
        <h1 className="hero__title">
          Will your flight <span className="hero__title-accent">depart on time?</span>
        </h1>
        <p className="hero__subtitle">
          Enter flight and weather conditions below. A Random Forest model trained on
          historical flight and weather data estimates the probability of delay in real time.
        </p>
      </div>
    </section>
  )
}
