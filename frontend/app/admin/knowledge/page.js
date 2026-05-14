'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { knowledge } from '@/lib/api'

export default function AdminKnowledgePage() {
  const { user } = useAuth()
  const router = useRouter()
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)
  const [newEntry, setNewEntry] = useState({ question: '', answer: '', category: 'general' })

  useEffect(() => {
    if (user && user.role !== 'admin') {
      router.push('/dashboard')
    } else {
      loadEntries()
    }
  }, [user])

  const loadEntries = async () => {
    setLoading(true)
    try {
      const data = await knowledge.list()
      setEntries(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddEntry = async (e) => {
    e.preventDefault()
    try {
      const { knowledge: knowledgeApi } = await import('@/lib/api')
      await knowledgeApi.post('/entries', newEntry)
      setNewEntry({ question: '', answer: '', category: 'general' })
      loadEntries()
    } catch (err) {
      console.error(err)
    }
  }

  const ingestDefaults = async () => {
    try {
      await knowledge.ingestDefaults()
      loadEntries()
    } catch (err) {
      console.error(err)
    }
  }

  if (!user || (user.role !== 'admin' && user.role !== 'system_admin')) {
    return <div className="p-8 text-center text-gray-500 dark:text-slate-400">Unauthorized - Admin access required</div>
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Knowledge Base</h1>
          <button
            onClick={ingestDefaults}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Ingest Default FAQs
          </button>
        </div>

        {/* Add Entry Form */}
        <form onSubmit={handleAddEntry} className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 p-6 space-y-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Add FAQ Entry</h2>
          <div className="grid grid-cols-1 gap-4">
            <input
              type="text"
              placeholder="Question"
              value={newEntry.question}
              onChange={(e) => setNewEntry({ ...newEntry, question: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white"
              required
            />
            <textarea
              placeholder="Answer"
              value={newEntry.answer}
              onChange={(e) => setNewEntry({ ...newEntry, answer: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white"
              rows="3"
              required
            />
            <select
              value={newEntry.category}
              onChange={(e) => setNewEntry({ ...newEntry, category: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white"
            >
              <option value="admission">Admission</option>
              <option value="fee">Fee</option>
              <option value="hostel">Hostel</option>
              <option value="academic">Academic</option>
              <option value="lms">LMS</option>
              <option value="exam">Exam</option>
              <option value="placement">Placement</option>
              <option value="general">General</option>
            </select>
          </div>
          <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
            Add Entry
          </button>
        </form>

        {/* Entries List */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 overflow-hidden">
          {loading ? (
            <p className="p-6 text-gray-500 dark:text-slate-400">Loading...</p>
          ) : entries.length === 0 ? (
            <p className="p-6 text-gray-500 dark:text-slate-400">No entries yet. Add one or ingest defaults.</p>
          ) : (
            <table className="min-w-full divide-y divide-gray-200 dark:divide-slate-700">
              <thead className="bg-gray-50 dark:bg-slate-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-300 uppercase">Question</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-300 uppercase">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-300 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
                {entries.map((entry) => (
                  <tr key={entry.id}>
                    <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">{entry.question}</td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-slate-400">{entry.category}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        entry.is_active ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-slate-600 text-gray-800 dark:text-slate-200'
                      }`}>
                        {entry.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </AppShell>
  )
}
