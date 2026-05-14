'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Ticket, CheckCircle } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function AdminTickets() {
  const [tickets, setTickets] = useState([])

  useEffect(() => {
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${API_BASE}/tickets/stats/summary`, { headers: { Authorization: `Bearer ${token}` } })
        if (res.ok) setTickets(await res.json())
      } catch (e) { console.error(e) }
    }
    load()
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Support Tickets</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Manage student support requests</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-6 text-center">
            <p className="text-3xl font-bold text-amber-600 dark:text-amber-400">12</p>
            <p className="text-sm text-slate-500 mt-1">Open</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">8</p>
            <p className="text-sm text-slate-500 mt-1">In Progress</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">45</p>
            <p className="text-sm text-slate-500 mt-1">Resolved</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Tickets</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
                  <th className="text-left py-3 px-4 font-medium text-slate-500">ID</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Subject</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Department</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Priority</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Status</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { id: 'TKT-1024', subject: 'Document upload issue', dept: 'Technical', priority: 'high', status: 'open' },
                  { id: 'TKT-1023', subject: 'Fee payment query', dept: 'Accounts', priority: 'medium', status: 'in_progress' },
                  { id: 'TKT-1022', subject: 'Change of branch request', dept: 'Admissions', priority: 'low', status: 'resolved' },
                ].map((t) => (
                  <tr key={t.id} className="border-b border-slate-100 dark:border-slate-800">
                    <td className="py-3 px-4 text-slate-900 dark:text-white font-medium">{t.id}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{t.subject}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{t.dept}</td>
                    <td className="py-3 px-4">
                      <Badge variant={t.priority === 'high' ? 'destructive' : t.priority === 'medium' ? 'warning' : 'secondary'}>
                        {t.priority}
                      </Badge>
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant={t.status === 'resolved' ? 'success' : t.status === 'in_progress' ? 'info' : 'warning'}>
                        {t.status.replace('_', ' ')}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
