'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function CoordinatorApplications() {
  const [applications, setApplications] = useState([])

  useEffect(() => {
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${API_BASE}/coordinator/students`, { headers: { Authorization: `Bearer ${token}` } })
        if (res.ok) setApplications(await res.json())
      } catch (e) { console.error(e) }
    }
    load()
  }, [])

  const handleStatus = async (id, status) => {
    try {
      const token = localStorage.getItem('token')
      await fetch(`${API_BASE}/coordinator/students/${id}/status`, {
        method: 'PATCH',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      })
    } catch (e) { console.error(e) }
  }

  const statusMap = { pending: 'warning', approved: 'success', rejected: 'destructive', enrolled: 'info' }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Pending Approvals</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Review and approve applications</p>
      </div>
      <Card>
        <CardHeader><CardTitle>Applications</CardTitle></CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-slate-50 dark:bg-slate-800/50">
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Name</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Email</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Status</th>
                  <th className="text-right py-3 px-4 font-medium text-slate-500">Actions</th>
                </tr>
              </thead>
              <tbody>
                {applications.filter(a => a.status === 'pending').map((app) => (
                  <tr key={app.id} className="border-b border-slate-100 dark:border-slate-800">
                    <td className="py-3 px-4 text-slate-900 dark:text-white font-medium">{app.full_name || app.name}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{app.email}</td>
                    <td className="py-3 px-4">
                      <Badge variant={statusMap[app.status] || 'secondary'}>{app.status}</Badge>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex justify-end gap-2">
                        <Button size="sm" variant="outline" className="text-emerald-600" onClick={() => handleStatus(app.id, 'approved')}>Approve</Button>
                        <Button size="sm" variant="outline" className="text-red-600" onClick={() => handleStatus(app.id, 'rejected')}>Reject</Button>
                      </div>
                    </td>
                  </tr>
                ))}
                {applications.filter(a => a.status === 'pending').length === 0 && (
                  <tr><td colSpan={4} className="py-8 text-center text-slate-500">No pending applications</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
