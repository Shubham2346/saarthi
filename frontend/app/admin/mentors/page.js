'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Users, Plus } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function AdminMentors() {
  const [mentors, setMentors] = useState([])

  useEffect(() => {
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${API_BASE}/admin/mentors`, { headers: { Authorization: `Bearer ${token}` } })
        if (res.ok) setMentors(await res.json())
      } catch (e) { console.error(e) }
    }
    load()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Mentors</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Manage faculty mentors</p>
        </div>
        <Button size="sm"><Plus className="w-4 h-4 mr-1" /> Assign Mentor</Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {mentors.map((m) => (
          <Card key={m.id}>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-bold text-lg">
                  {(m.full_name || m.name || '?')[0]}
                </div>
                <div>
                  <p className="font-medium text-slate-900 dark:text-white">{m.full_name || m.name}</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">{m.email}</p>
                  {m.department && <Badge variant="secondary" className="mt-1 text-[10px]">{m.department}</Badge>}
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-500">Students</span>
                  <span className="font-semibold text-slate-900 dark:text-white">{m.student_count || 0}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
        {mentors.length === 0 && (
          <div className="col-span-full text-center py-12">
            <Users className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
            <p className="text-slate-500">No mentors found</p>
          </div>
        )}
      </div>
    </div>
  )
}
