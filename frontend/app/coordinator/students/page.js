'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function CoordinatorStudents() {
  const [students, setStudents] = useState([])

  useEffect(() => {
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${API_BASE}/coordinator/students`, { headers: { Authorization: `Bearer ${token}` } })
        if (res.ok) setStudents(await res.json())
      } catch (e) { console.error(e) }
    }
    load()
  }, [])

  const statusMap = { pending: 'warning', approved: 'success', rejected: 'destructive', enrolled: 'info' }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Department Students</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Students assigned to your department</p>
      </div>
      <Card>
        <CardHeader><CardTitle>All Students</CardTitle></CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-slate-50 dark:bg-slate-800/50">
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Name</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Email</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Stage</th>
                </tr>
              </thead>
              <tbody>
                {students.map((s) => (
                  <tr key={s.id} className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                    <td className="py-3 px-4 text-slate-900 dark:text-white font-medium">{s.full_name || s.name}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{s.email}</td>
                    <td className="py-3 px-4">
                      <Badge variant={statusMap[s.status] || 'secondary'}>{s.status}</Badge>
                    </td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400 capitalize">{s.stage || '-'}</td>
                  </tr>
                ))}
                {students.length === 0 && <tr><td colSpan={4} className="py-8 text-center text-slate-500">No students found</td></tr>}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
