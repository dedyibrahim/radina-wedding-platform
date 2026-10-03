import { wedding } from '../data/wedding'
const escape = value => String(value).replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;')
export function downloadCalendar() {
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//AlyaRizky//Wedding//ID', 'CALSCALE:GREGORIAN']
  for (const [index, event] of [wedding.akad, wedding.reception].entries()) {
    lines.push('BEGIN:VEVENT', `UID:alya-rizky-${index}-20261212@wedding.local`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')}`, `DTSTART:${event.start}`, `DTEND:${event.end}`, `SUMMARY:${escape(`${event.title} — ${wedding.bride.shortName} & ${wedding.groom.shortName}`)}`, `LOCATION:${escape(`${wedding.location.name}, ${wedding.location.address}`)}`, `DESCRIPTION:${escape('Dengan penuh cinta kami mengundang Anda untuk hadir dan memberikan doa restu.')}`, 'END:VEVENT')
  }
  lines.push('END:VCALENDAR')
  const url = URL.createObjectURL(new Blob([lines.join('\r\n') + '\r\n'], { type: 'text/calendar;charset=utf-8' }))
  const a = document.createElement('a'); a.href = url; a.download = 'Alya-Rizky-Wedding.ics'; a.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
