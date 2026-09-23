import { useEffect, useState } from 'react'
import { api } from '../api/client.js'

// รองรับ: FR-BKG-01, FR-BKG-06
export default function SlotPicker() {
  const today = new Date().toISOString().slice(0, 10)
  const [packageCode, setPackageCode] = useState('general')
  const [dateFrom, setDateFrom] = useState(today)
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true

    async function loadSlots() {
      setLoading(true)
      setError('')

      try {
        const data = await api.getSlots({ dateFrom, packageCode })
        const list = Array.isArray(data) ? data : data.slots ?? []
        if (active) setSlots(list)
      } catch (err) {
        if (active) {
          setError('ไม่สามารถโหลดช่วงเวลาว่างได้ในขณะนี้')
          setSlots([])
        }
      } finally {
        if (active) setLoading(false)
      }
    }

    loadSlots()
    return () => {
      active = false
    }
  }, [dateFrom, packageCode])

  return (
    <section className="mt-6 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">แพ็กเกจ</p>
          <select
            aria-label="แพ็กเกจ"
            value={packageCode}
            onChange={(event) => setPackageCode(event.target.value)}
            className="mt-1 rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-800"
          >
            <option value="general">ทั่วไป</option>
            <option value="premium">พรีเมี่ยม</option>
            <option value="elder">ผู้สูงอายุ</option>
          </select>
        </div>

        <div>
          <p className="text-sm font-medium text-slate-500">วันที่เริ่มต้น</p>
          <input
            aria-label="วันที่เริ่มต้น"
            type="date"
            value={dateFrom}
            onChange={(event) => setDateFrom(event.target.value)}
            className="mt-1 rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-800"
          />
        </div>
      </div>

      {error && <p className="mt-4 text-sm text-red-600">{error}</p>}

      <div className="mt-5 space-y-3">
        {loading ? (
          <p className="text-sm text-slate-500">กำลังโหลดช่วงเวลา...</p>
        ) : slots.length === 0 ? (
          <p className="text-sm text-slate-500">ไม่มีช่วงเวลาที่ว่างในวันและแพ็กเกจที่เลือก</p>
        ) : (
          slots.map((slot) => (
            <div
              key={slot.id ?? `${slot.date}-${slot.start_time}`}
              className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <div>
                <p className="font-medium text-slate-800">{slot.date ?? slot.slot_date}</p>
                <p className="text-sm text-slate-600">{slot.start_time ?? slot.startTime}</p>
              </div>
              <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-sm font-medium text-emerald-800">
                เหลือ {slot.remaining ?? 0} ที่
              </span>
            </div>
          ))
        )}
      </div>
    </section>
  )
}
