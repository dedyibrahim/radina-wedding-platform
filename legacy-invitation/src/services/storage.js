const PREFIX = 'alya-rizky-v1:'
// Replace this adapter with API calls when a backend is available.
export const invitationRepository = {
  read(key, fallback = []) { try { const data = JSON.parse(localStorage.getItem(PREFIX + key)); return Array.isArray(data) ? data : fallback } catch { return fallback } },
  async add(key, entry) {
    const entries = this.read(key)
    const record = { ...entry, id: crypto.randomUUID?.() || `${Date.now()}-${Math.random()}`, createdAt: new Date().toISOString() }
    localStorage.setItem(PREFIX + key, JSON.stringify([record, ...entries].slice(0, 200)))
    return record
  }
}
