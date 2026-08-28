// These values must match what the model was trained on. Do not add options
// here without also retraining/updating the backend — unknown categorical
// values will be silently one-hot-encoded to "unknown" and skew predictions.

export const AIRLINES = [
  { code: 'AA', name: 'American Airlines' },
  { code: 'DL', name: 'Delta Air Lines' },
  { code: 'UA', name: 'United Airlines' },
  { code: 'WN', name: 'Southwest Airlines' },
  { code: 'AS', name: 'Alaska Airlines' },
  { code: 'B6', name: 'JetBlue Airways' },
  { code: 'NK', name: 'Spirit Airlines' },
  { code: 'F9', name: 'Frontier Airlines' },
]

export const AIRPORTS = [
  { code: 'ATL', name: 'Atlanta' },
  { code: 'ORD', name: 'Chicago O\u2019Hare' },
  { code: 'DFW', name: 'Dallas\u2013Fort Worth' },
  { code: 'DEN', name: 'Denver' },
  { code: 'LAX', name: 'Los Angeles' },
  { code: 'JFK', name: 'New York JFK' },
  { code: 'SFO', name: 'San Francisco' },
  { code: 'SEA', name: 'Seattle\u2013Tacoma' },
  { code: 'LAS', name: 'Las Vegas' },
  { code: 'MCO', name: 'Orlando' },
]

export const MONTHS = [
  { value: 1, label: 'January' },
  { value: 2, label: 'February' },
  { value: 3, label: 'March' },
  { value: 4, label: 'April' },
  { value: 5, label: 'May' },
  { value: 6, label: 'June' },
  { value: 7, label: 'July' },
  { value: 8, label: 'August' },
  { value: 9, label: 'September' },
  { value: 10, label: 'October' },
  { value: 11, label: 'November' },
  { value: 12, label: 'December' },
]

// 0 = Monday ... 6 = Sunday, matching the training data generator
export const DAYS_OF_WEEK = [
  { value: 0, label: 'Monday' },
  { value: 1, label: 'Tuesday' },
  { value: 2, label: 'Wednesday' },
  { value: 3, label: 'Thursday' },
  { value: 4, label: 'Friday' },
  { value: 5, label: 'Saturday' },
  { value: 6, label: 'Sunday' },
]

export const HOURS = Array.from({ length: 24 }, (_, h) => {
  const label =
    h === 0 ? '12:00 AM' : h < 12 ? `${h}:00 AM` : h === 12 ? '12:00 PM' : `${h - 12}:00 PM`
  return { value: h, label }
})

export const DEFAULT_FORM = {
  airline: 'AA',
  origin: 'ATL',
  dest: 'ORD',
  month: new Date().getMonth() + 1,
  day_of_week: 0,
  sched_dep_hour: 17,
  distance: 600,
  temperature_f: 55,
  wind_speed_mph: 10,
  precipitation_in: 0,
  visibility_miles: 10,
}
