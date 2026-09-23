import { render, screen, waitFor } from '@testing-library/react'
import SlotPicker from '../pages/SlotPicker.jsx'

beforeEach(() => {
  global.fetch = vi.fn(async () => ({
    ok: true,
    json: async () => ({
      slots: [
        { id: 1, date: '2026-09-24', start_time: '09:00', remaining: 5 },
        { id: 2, date: '2026-09-24', start_time: '10:00', remaining: 2 },
      ],
    }),
  }))
})

test('T-09 แสดงรายการช่วงเวลาว่างพร้อมจำนวนที่นั่งคงเหลือจาก mock API', async () => {
  render(<SlotPicker />)

  await waitFor(() => {
    expect(screen.getByText('09:00')).toBeTruthy()
    expect(screen.getByText('เหลือ 5 ที่')).toBeTruthy()
  })

  expect(screen.getByLabelText('แพ็กเกจ')).toBeTruthy()
  expect(screen.getByLabelText('วันที่เริ่มต้น')).toBeTruthy()
})
